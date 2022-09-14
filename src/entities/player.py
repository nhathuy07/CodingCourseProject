
from time import time
from typing import Any, List, Optional
from common.config import DISPLAY_SCALING, BulletConfig, PlayerConfig, get_window_size
from common.events import EMIT_TRAIL_PARTICLE, ITEM_COLLECTED, PLAYER_DIED, SHOOT
from common.types import Collectibles, Ground, PlayerState
from entities import bullet
from entities.collectible import Collectible
from session import Session
from pygame import (
    Surface,
    Rect,
    event,
    MOUSEBUTTONDOWN,
    KEYDOWN,
    KEYUP,
    K_LSHIFT,
    K_RSHIFT,
    K_a,
    K_d,
    K_f,
    K_LEFT,
    K_RIGHT,
    K_SPACE,
    KMOD_SHIFT,
    transform,
)


class Player:
    def __init__(
        self,
        session: Session,
        x=PlayerConfig.InitX,
        y=PlayerConfig.InitY,
        movingSpd=PlayerConfig.MovingSpd,
        jumpingSpd=PlayerConfig.JumpingSpd,
        gravity=PlayerConfig.Gravity,
        acceleration=PlayerConfig.Acceleration,
        deceleration=PlayerConfig.Deceleration,
        hp=PlayerConfig.HP,
        soft_edge=PlayerConfig.SoftEdge,
    ) -> None:
        # init position
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0
        # player inventory
        self.inventory = {}
        self.hp = hp

        self.sprites = session.player_sprite
        self.state: PlayerState = PlayerState.Idle
        self.gravity = gravity
        self.rect = Rect(self.x, self.y, 94 * 0.7, 170 * 0.7)
        self.current_jumping_spd = 0
        self.y_offset = 0
        self.floating_effect_direction = "up"
        self.acceleration = acceleration
        self.deceleration = deceleration
        # default speed values
        self.moving_speed = movingSpd
        self.jumping_speed = jumpingSpd
        # max fall speed
        self.terminal_velocity = 35

        # moving directions
        self.moving_left = False
        self.moving_right = False
        self.jumping = False
        self.landed = True
        # set flip
        self.image_flipped = False
        self.clear_event()

        # particle settings
        self.last_particle_spawn_time = 0
        self.particle_interval = 0.04
        self.particle_relative_position = [48 * 0.7, 135 * 0.7]

        # damage effect settings
        self.last_damaged_time = 0

        # shooting settings
        self.damage = BulletConfig.Damage
        self.cooldown = 0.3
        self.last_shoot_time = 0

        self.soft_edge = soft_edge

        self.destroyed = False

        self.gun_perk_expire_time = 0
        self.gun_perk_timer_pane = None

    def clear_event(self):
        # clear events to prevent undesirable behaviors caused by clicking A/D or Left/Right on preload screen
        event.clear()

    def jump(self):
        if self.landed:
            self.landed = False
            self.dy = -self.jumping_speed

    def collect_item(self, entities: List[Collectible]):
        for c in entities:
            # grab all entities of type ground
            if c.rect.colliderect(self.rect) and type(c).__name__ == "Collectible":
                if c.collectible_type in (Collectibles.GREY, Collectibles.GREEN, Collectibles.PURPLE, Collectibles.YELLOW):
                    if c.collectible_type.name in self.inventory:
                        self.inventory[c.collectible_type.name] += 1
                    else:
                        self.inventory[c.collectible_type.name] = 1
                    entities.remove(c)
                    event.post(event.Event(ITEM_COLLECTED))
                elif c.collectible_type == Collectibles.WEAPON_SUPERCHARGER:
                    self.gun_perk_expire_time = time() + PlayerConfig.PerkDuration
                    entities.remove(c)

    def shoot(self, entities, session):
        if time() < self.gun_perk_expire_time:
            self.damage = BulletConfig.Damage * 1.5
        else:
            self.damage = BulletConfig.Damage
        

        if time() - self.last_shoot_time >= self.cooldown:
            if not self.image_flipped:
                bullet_init_pos = (
                    self.rect.x + self.rect.width + 40 * DISPLAY_SCALING,
                    self.rect.y + 50 * DISPLAY_SCALING + self.y_offset,
                )
                entities.append(
                    bullet.PlayerBullet(
                        session,
                        bullet_init_pos[0],
                        bullet_init_pos[1],
                        dx=BulletConfig.Dx,
                        damage=self.damage
                    )
                )
            else:
                bullet_init_pos = (
                    self.rect.x - 40 * DISPLAY_SCALING,
                    self.rect.y + 50 * DISPLAY_SCALING + self.y_offset,
                )
                entities.append(
                    bullet.PlayerBullet(
                        session,
                        bullet_init_pos[0],
                        bullet_init_pos[1],
                        dx=-BulletConfig.Dx,
                    )
                )
            self.last_shoot_time = time()

    def check_collision_with_liquid(self, entities: List[Any], display):
        for c in entities:
            if (
                c.rect.colliderect(
                    Rect(
                        self.rect.x,
                        self.rect.y,
                        self.rect.width,
                        self.rect.height * 0.6,
                    )
                )
                and type(c).__name__ == "Liquid"
            ):
                self.inflict_damage(40, 0.1, entities=entities, display=display)
                self.terminal_velocity = 3

    def update_speed_based_on_collision(self, terrain: List[Ground]):
        self.landed = False
        # predict moving speed
        if self.dy < self.terminal_velocity:
            self.dy += self.gravity
        else:
            self.dy = self.terminal_velocity

        # calculate actual moving speed based on collisions
        for t in terrain:
            if t.rect.colliderect(
                self.rect.x, self.rect.y + self.dy, self.rect.width, self.rect.height
            ):
                # prevent character from falling / rising through ground
                if self.dy < 0:
                    self.dy = t.rect.bottom - self.rect.top
                else:
                    self.landed = True
                    self.dy = t.rect.top - self.rect.bottom

            # prevent character from moving forward if ground blocks his way
            if self.dx > 0:
                if t.rect.colliderect(
                    self.rect.x + round(self.dx) + 1,
                    self.rect.y,
                    self.rect.width,
                    self.rect.height,
                ):
                    self.dx = 0
            elif self.dx < 0:
                if t.rect.colliderect(
                    self.rect.x + int(self.dx) - 1,
                    self.rect.y,
                    self.rect.width,
                    self.rect.height,
                ):
                    self.dx = 0

        self.rect.x += self.dx
        self.rect.y += self.dy

    def update_world_offset(self, world):
        # update world offset
        # code adopted from S4V - CS102 - Lesson 6 - Milestone 3
        if world != None:
            delta_world_offset = 0
            at_right_edge = self.rect.right >= get_window_size()[0]
            at_right_soft_edge = (
                self.rect.right > get_window_size()[0] - PlayerConfig.SoftEdge
            )
            at_left_edge = self.rect.left <= 0
            at_left_soft_edge = self.rect.left < PlayerConfig.SoftEdge
            if (
                at_left_edge
                or at_right_edge
                or (at_left_soft_edge and not world.at_left_most())
                or (at_right_soft_edge and not world.at_right_most())
            ):
                self.rect.x -= self.dx
                delta_world_offset = -self.dx
            world.update_world_offset(delta_world_offset)

    def floating_effect(self):
        if self.y_offset < -7:
            self.floating_effect_direction = "down"
        elif self.y_offset > 7:
            self.floating_effect_direction = "up"

        if self.floating_effect_direction == "up":
            self.y_offset -= 0.2
        else:
            self.y_offset += 0.2

    def particle_effect(self):
        if (
            time() - self.last_particle_spawn_time
            > self.particle_interval * PlayerConfig.MovingSpd / abs(self.dx)
        ):
            event.post(event.Event(EMIT_TRAIL_PARTICLE))
            self.last_particle_spawn_time = time()

    def inflict_damage(
        self,
        hp: float,
        interval: float,
        knockback: float = 0,
        entities=None,
        display=None,
    ):
        if time() - self.last_damaged_time >= interval:
            if not self.image_flipped:
                self.dx = -knockback
            else:
                self.dx = knockback

            # prevent player from clipping through walls
            self.update_speed_based_on_collision(
                [x for x in entities if type(x).__name__ == "Ground"]
            )
            self.hp -= hp
            self.last_damaged_time = time()
        if self.hp < 0:
            self.state = PlayerState.Destroyed
            self.rect.y -= 90 * DISPLAY_SCALING
            self.destroyed = True

    def update(self, display: Surface, entities, session: Session, world):

        # grab user input
        for e in event.get((KEYUP, KEYDOWN)):
            if e.type == KEYDOWN:
                if e.key == K_a or e.key == K_LEFT:
                    self.moving_left = True
                    self.moving_right = False
                    self.image_flipped = True
                elif e.key == K_d or e.key == K_RIGHT:
                    self.moving_left = False
                    self.moving_right = True
                    self.image_flipped = False
                elif e.key == K_SPACE:
                    self.jump()
                elif e.key == K_f:
                    self.shoot(entities, session)

            elif e.type == KEYUP:
                if e.key == K_LEFT or e.key == K_a:
                    self.moving_left = False
                elif e.key == K_RIGHT or e.key == K_d:
                    self.moving_right = False

        if self.landed:
            self.dy = 0
        self.dy += self.gravity
        # predict speed based on player input
        if self.moving_left:
            self.dx -= self.acceleration
            # accelerate by self.acceleration until speed reaches self.dx
            if self.dx < -self.moving_speed:
                self.dx = -self.moving_speed

        elif self.moving_right:
            self.dx += self.acceleration
            if self.dx > self.moving_speed:
                self.dx = self.moving_speed

        else:
            if self.dx < 0 and self.image_flipped:
                self.dx += self.deceleration
            elif self.dx > 0 and not self.image_flipped:
                self.dx -= self.deceleration
            else:
                self.dx = 0

        self.update_speed_based_on_collision(
            [x for x in entities if type(x).__name__ == "Ground"]
        )
        self.update_world_offset(world)
        # update player state:
        if self.dx != 0:
            if time() - self.last_damaged_time < 0.2:
                self.state = PlayerState.AttackedWhileMoving
            else:
                self.state = PlayerState.Moving

        else:
            if time() - self.last_damaged_time < 0.2:
                self.state = PlayerState.Attacked
            elif time() - self.last_shoot_time < 0.1:
                self.state = PlayerState.Shooting
            else:
                self.state = PlayerState.Idle

        if self.state == PlayerState.Idle or self.state == PlayerState.Attacked:
            self.floating_effect()
            self.last_particle_spawn_time = 0
        elif self.state == PlayerState.Moving:
            self.particle_effect()

        self.collect_item(entities)
        self.check_collision_with_liquid(entities, display)
        self.particle_relative_position = [27, self.rect.height - 15 + self.y_offset]

    def render(self, display):
        display.blit(
            transform.flip(self.sprites[self.state.name], True, False)
            if self.image_flipped
            else self.sprites[self.state.name],
            (
                self.rect.x - self.rect.width if self.image_flipped else self.rect.x,
                int(self.rect.y + self.y_offset),
            ),
        )
        if self.destroyed:
            event.post(event.Event(PLAYER_DIED))
