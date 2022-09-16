from random import randint
from time import time
from common.config import DISPLAY_SCALING, FONT, BulletConfig, get_window_size
from common.types import MobState, Mobs
from session import Session
from pygame import transform, draw, font
class Enemy:
    def __init__(
        self,
        session: Session,
        mob_type: Mobs,
        x,
        y,
        side: 0,
        init_dx,
        init_dy,
        damage,
        hp,
        locate_target_delay,
        locate_target_error,
        weapon_cooldown,
    ) -> None:
        self.side = side
        self.x = x
        self.y = randint(250, int(get_window_size()[1]) - 250)
        self.init_coord = [self.x, self.y]
        self.sprites = session.mobs[mob_type.name]
        self.state = MobState.Idle
        self.rect = self.sprites[self.state.name][0].get_rect()
        # enemy flies from x = -300
        if self.side == 0:
            self.rect.topleft = (self.x - 300, self.y)
            self.rect.width -= 70 * DISPLAY_SCALING
        # enemy files from x = window_width
        elif self.side == 1:
            self.rect.topleft = (self.x + 53 * DISPLAY_SCALING, self.y)
            self.rect.width -= 100 * DISPLAY_SCALING
        self.init_dx = init_dx if self.side == 0 else -init_dx
        self.init_dy = init_dy
        self.damage = damage
        self.hp = hp
        self.locate_target_delay = locate_target_delay
        self.locate_target_error = locate_target_error
        self.weapon_cooldown = weapon_cooldown

        self.last_player_location_call = 0
        self.player_location = [0, 0]

        self.last_attack_time = 0
        self.attack_anim_frame = 0
        self.attack_anim_finished = True
        self.killed = False
        self.current_loc_error = randint(-self.locate_target_error, self.locate_target_error)

        self.last_hurt_time = 0
        self.last_loc_change = 0

        self.target_delta_y = 0
    def update(self, world, display):
        # grab player's location every X seconds
        if time() - self.last_player_location_call >= self.locate_target_delay:
            
            self.player_location = (world.player.rect.x + self.current_loc_error, world.player.rect.y + self.current_loc_error)
            self.last_player_location_call = time()

        if time() - self.last_loc_change > 0.01:
            if self.rect.y > self.player_location[1]:
                self.rect.y -= randint(self.init_dy - 2, self.init_dy + 2)
            elif self.rect.y < self.player_location[1]:
                self.rect.y += randint(self.init_dy - 2, self.init_dy + 2)
            self.last_loc_change = time()


        self.rect.x += self.init_dx

        if self.rect.colliderect(world.player.rect):
            if time() - self.last_attack_time >= self.weapon_cooldown:
                self.attack_anim_finished = False
                self.attack(world, display)
                #self.last_attack_time = time()
                
        self.init_coord = [self.rect.x, self.rect.y]

        # if time() - self.last_hurt_time > 0.4 and self.state == MobState.Hurt:
        #     self.state = MobState.Idle

        if self.state == MobState.Attacking and not self.attack_anim_finished:
            if time() - self.last_attack_time >= 0.055 * self.attack_anim_frame:
                self.attack_anim_frame += 1
                if self.attack_anim_frame > 2:
                    self.state = MobState.Idle
                    self.attack_anim_frame = 0
                    self.attack_anim_finished = True
                    self.state = MobState.Idle

    def attack(self, world, display):
        self.state = MobState.Attacking
        world.player.inflict_damage(self.damage, self.weapon_cooldown, 0, world.entities, display)
        self.attack_anim_frame = 0
        self.last_attack_time = time()
        

    def render(self, display):
        if self.side == 0:
            current_img = transform.flip(self.sprites[self.state.name][self.attack_anim_frame % len(self.sprites[self.state.name])], True, False)
        else:
            current_img = self.sprites[self.state.name][self.attack_anim_frame % len(self.sprites[self.state.name])]
        display.blit(current_img, (self.rect.left - int(70 * DISPLAY_SCALING), self.rect.top))
        self.font = font.Font(FONT[0], 18)
        stateDisp = self.font.render(f"{self.state.name}, {self.attack_anim_frame}", True, (255, 255, 255))
        display.blit(stateDisp, (self.rect.left - int(70 * DISPLAY_SCALING), self.rect.top - 10))
        draw.rect(display, (255, 0, 0), self.rect, 5)
    def check_collision_with_bullet(self, bullets):
        for b in bullets:
            if b.rect.colliderect(self.rect) and time() - self.last_hurt_time > 0.1 and not b.exploded: # Enemy becomes temporarily invincible after being shot
                self.attack_anim_frame = 0
                self.hp -= b.damage
                self.state = MobState.Hurt
                self.last_hurt_time = time()
