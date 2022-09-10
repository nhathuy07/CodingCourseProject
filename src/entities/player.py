from math import ceil, floor
from typing import Any, List
from common.config import DISPLAY_SCALING, PlayerConfig
from common.events import ITEM_COLLECTED
from common.types import Ground, PlayerState
from entities.collectible import Collectible
from session import Session
from pygame import Surface, Rect, event, MOUSEBUTTONDOWN, KEYDOWN, KEYUP, K_ESCAPE, K_a, K_d, K_LEFT, K_RIGHT, K_SPACE, transform


class Player:
    def __init__(
        self,
        session: Session,
        x=PlayerConfig.InitX,
        y=PlayerConfig.InitY,
        movingSpd=PlayerConfig.MovingSpd,
        jumpingSpd=PlayerConfig.JumpingSpd,
        gravity=PlayerConfig.Gravity,
        acceleration=PlayerConfig.Acceleration
    ) -> None:
        # init position
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0
        # player inventory
        self.inventory = {}

        self.sprites = session.player_sprite
        self.state: PlayerState = PlayerState.Idle
        self.gravity = gravity
        self.rect = Rect(self.x, self.y, 94 * 0.7, 170 * 0.7)
        self.current_jumping_spd = 0
        self.y_offset = 0
        self.floating_effect_direction = "up"
        self.acceleration = acceleration

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
    def clear_event(self):
        # clear events to prevent undesirable behaviors caused by clicking A/D or Left/Right on preload screen
        event.clear()
    def jump(self):
        if self.landed:
            self.landed = False
            self.dy = -self.jumping_speed

    def collect_item(self, entities: List[Any]):
        for c in entities:
            # grab all entities of type ground
            if c.rect.colliderect(self.rect) and type(c).__name__ == "Collectible":
                if c.collectible_type.name in self.inventory:
                    self.inventory[c.collectible_type.name] += 1
                else:
                    self.inventory[c.collectible_type.name] = 1
                entities.remove(c)
                event.post(event.Event(ITEM_COLLECTED))
                

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
                    self.rect.x + round(self.dx) + 1, self.rect.y, self.rect.width, self.rect.height
                ):
                    self.dx = 0
            elif self.dx < 0:
                if t.rect.colliderect(
                    self.rect.x + int(self.dx) - 1, self.rect.y, self.rect.width, self.rect.height
                ):
                    self.dx = 0


        # update character's rect with calculated moving speed
        self.rect.y += self.dy
        self.rect.x += self.dx

    def floating_effect(self):
        if self.y_offset < -7:
            self.floating_effect_direction = "down"
        elif self.y_offset > 7:
            self.floating_effect_direction = "up"
        
        if self.floating_effect_direction == "up":
            self.y_offset -= 0.2
        else:
            self.y_offset += 0.2


    def update(self, display: Surface, entities):
        
        
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
            self.dx = 0
        
        self.update_speed_based_on_collision([x for x in entities if type(x).__name__ == "Ground"])

        # update player state:
        if self.dx != 0:
            self.state = PlayerState.Moving
        else:
            self.state = PlayerState.Idle

        if self.state == PlayerState.Idle:
            self.floating_effect()
        
        self.collect_item(entities)
        display.blit(
            transform.flip(self.sprites[self.state.name], True, False) if self.image_flipped else self.sprites[self.state.name],
            (self.rect.x - self.rect.width if self.image_flipped else self.rect.x, int(self.rect.y + self.y_offset))
        )
