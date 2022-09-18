from random import randint, random, choice
from time import time
from common.config import BossConfig, BulletConfig, get_window_size
from common.extra_types import BossState, MobState
import entities
from entities.bullet import EnemyBullet, PlayerBullet
from session import Session
from world import World
class EnemyBoss():
    def __init__(self, session: Session, config = BossConfig) -> None:
        self.x = get_window_size()[0] / 2
        self.y = get_window_size()[1] / 2
        self.sprites = session.boss_sprite
        self.dx = config.Dx
        self.dy = config.Dy
        self.damage = 10
        self.simultaneous_bullet_spawn = config.SimultaneousBulletSpawn
        self.simultaneous_meteorite_spawn = config.SimultaneousMeteoriteSpawn
        self.instakill_possibility = config.InstakillPosibilities
        self.growl_knockback_distance = config.GrowlKnockbackDistance
        self.current_sound = 0

        # attack time settings
        self.last_attack_time = time()
        self.attack_interval = 0

        self.state = BossState.Idle

        self.sound_played = False
        self.hurt = False

        self.rect = self.sprites[self.state.name]["Original"].get_rect()
        

        self.reached_target_x = False
        self.reached_target_y = False

        self.wandering_dy = randint(self.dy - 6, self.dy + 4)
        self.wandering_dx = self.dx
        self.init_coord = [self.rect.x, self.rect.y]

        self.horizontal_wandering_direction = "right"
        self.vertical_wandering_direction = "down"

        self.attack_range = 230

        self.current_sound = None
        
        self.bullet_spitted = False

        self.location_delay = 0.4
        self.last_location_call = 0
        
        self.player_loc = [0, 0]

        self.hp = BossConfig.Hp
        self.last_hp_deplete_time = 0

    def update(self, world: World, session: Session):
        # choose an attack method randomly
        self.attack_interval = randint(3, 5)
        self.sound_played = False
        self.wandering_dy = randint(self.dy - 6, self.dy + 4)
        
        self.check_collision_with_bullet(world)

        # locate player every 400 ms
        if time() - self.last_location_call > self.location_delay:
            self.player_loc = [world.player.rect.centerx, world.player.rect.centery]
            self.last_location_call = time()
        
        if self.rect.y < 0 or self.rect.centery < self.player_loc[1]:
            self.vertical_wandering_direction = "down"
        elif self.rect.y > get_window_size()[1] - 200 or self.rect.centery > self.player_loc[1]:
            self.vertical_wandering_direction = "up"
        
        if self.rect.x < 0:
            self.horizontal_wandering_direction = "right"
        elif self.rect.x > get_window_size()[0] - 200:
            self.horizontal_wandering_direction = "left"
        
        if self.vertical_wandering_direction == "down":
            self.rect.y += self.wandering_dy
        elif self.vertical_wandering_direction == "up":
            self.rect.y -= self.wandering_dy

        if self.horizontal_wandering_direction == "left":
            self.rect.x -= self.wandering_dx
        elif self.horizontal_wandering_direction == "right":
            self.rect.x += self.wandering_dx
        
        
            
        error = randint(-200, 0)
        # boss attacks player once it reaches him
        if (
            abs(self.rect.centery - world.player.rect.centery - error) < self.attack_range
            and abs(self.rect.centerx - world.player.rect.centerx) < self.attack_range
            and time() - self.last_attack_time > self.attack_interval
        ):
            attack_method = BossState.SpittingBullet
            if attack_method == BossState.Growling:
                self.state = BossState.Growling
                self.current_sound = session.sfx["monster_growling.wav"]
                self.current_sound.play()
                world.player.inflict_damage(10, 0.4, knockback=40, entities=world.entities, world=world)
                
            elif attack_method == BossState.SpittingBullet:
                if not self.bullet_spitted:
                    bullet_num = randint(self.simultaneous_bullet_spawn[0], self.simultaneous_bullet_spawn[1])
                    for _ in range(bullet_num):
                        world.entities.append(EnemyBullet(session, self.rect.centerx, self.rect.centery + 40, dy = randint(-20, 20), gravity=0, damage=self.damage))
                    self.bullet_spitted = True
            self.last_attack_time = time()
        self.init_coord = [self.rect.x, self.rect.y]


        if time() - self.last_attack_time > 1.5:
            if self.current_sound != None:
                self.current_sound.stop()
            self.state = BossState.Idle
            self.bullet_spitted = False
        
        if time() - self.last_hp_deplete_time > 0.4:
            self.hurt = False

    def render(self, display, world, session):
        self.update(world, session)
        if not self.hurt:
            display.blit(self.sprites[self.state.name]["Original"], self.rect.topleft)
        else:
            display.blit(self.sprites[self.state.name]["Hurt"], self.rect.topleft)

    def check_collision_with_bullet(self, world: World):
        for e in world.entities:
            if type(e).__name__ == "PlayerBullet" and e.rect.colliderect(self.rect):
                self.hp -= BulletConfig.Damage
                self.hurt = True
                self.last_hp_deplete_time = time()