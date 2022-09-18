from random import choice, randint
from time import time
from common.config import BossConfig, BulletConfig, get_window_size
from common.events import OUTRO
from common.extra_types import BossState
from entities.bullet import EnemyBullet
from session import Session
from world import World
from pygame import draw, rect,event
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
        #self.instakill_possibility = config.InstakillPosibilities --> coming soon
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
        self.meteorite_spawned= False

        self.last_shot = 0

        self.alive = True

        # death animation
        self.frames = session.BOSS_DEATH
        self.current_frame = 0
        self.last_frame_switch = 0
        self.anim_interval = 0.13
        self.death_sound_played = False

    def update(self, world: World, session: Session):
        if self.alive:
            # choose an attack method randomly
            self.attack_interval = randint(3, 5)
            self.sound_played = False
            self.wandering_dy = randint(self.dy - 6, self.dy + 4)
            
            self.check_collision_with_bullet(world)

            # locate player every 400 ms
            if time() - self.last_location_call > self.location_delay:
                self.player_loc = [world.player.rect.centerx, world.player.rect.centery]
                self.last_location_call = time()
            
            error = randint(-200, 0)

            if self.rect.y < 0 or self.rect.centery < self.player_loc[1] + error:
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
            
            
                
            
            # boss attacks player once it reaches him
            if (
                abs(self.rect.centery - world.player.rect.centery - error) < self.attack_range
                and abs(self.rect.centerx - world.player.rect.centerx) < self.attack_range
                and time() - self.last_attack_time > self.attack_interval
            ):
                attack_method = choice((BossState.DroppingBomb, BossState.Growling, BossState.SpittingBullet))
                if attack_method == BossState.Growling:
                    self.state = BossState.Growling
                    self.current_sound = session.sfx["monster_growling.wav"]
                    self.current_sound.play()
                    world.player.inflict_damage(0, 0.4, knockback=self.growl_knockback_distance, entities=world.entities, world=world)
                    
                elif attack_method == BossState.SpittingBullet:
                    if not self.bullet_spitted:
                        bullet_num = randint(self.simultaneous_bullet_spawn[0], self.simultaneous_bullet_spawn[1])
                        for _ in range(bullet_num):
                            world.entities.append(EnemyBullet(session, self.rect.centerx, self.rect.centery + 40, dx = choice((-BulletConfig.Dx, BulletConfig.Dx)), dy = randint(-20, 20), gravity=0.2, damage=self.damage))
                        self.bullet_spitted = True

                elif attack_method == BossState.DroppingBomb:
                    self.state = BossState.DroppingBomb
                    if not self.meteorite_spawned:
                        for _ in range(self.simultaneous_meteorite_spawn):
                            world.entities.append(EnemyBullet(session, randint(0, int(get_window_size()[0])), 0, 0, 7, 0.3, 30, True))
                            self.meteorite_spawned = True

                self.last_attack_time = time()
            self.init_coord = [self.rect.x, self.rect.y]

            if time() - self.last_attack_time > 1.5:
                if self.current_sound != None:
                    self.current_sound.stop()
                self.state = BossState.Idle
                self.bullet_spitted = False
                self.meteorite_spawned = False
            
            if time() - self.last_hp_deplete_time > 0.4:
                self.hurt = False

        else:
            # execute these functions when boss is dead
            if not self.death_sound_played:
                self.current_sound = session.sfx["boss_defeated.wav"]
                self.current_sound.play()
                self.death_sound_played = True
            if self.current_frame < len(self.frames) - 1:
                if time() - self.last_frame_switch > self.anim_interval:
                    self.current_frame += 1
                    self.last_frame_switch = time()
            else:
                event.post(event.Event(OUTRO))
                
        


    def render(self, display, world, session):
        self.update(world, session)
        if self.alive:
            if not self.hurt:
                display.blit(self.sprites[self.state.name]["Original"], self.rect.topleft)
            else:
                display.blit(self.sprites[self.state.name]["Hurt"], self.rect.topleft)
        else:
            display.blit(self.frames[self.current_frame], self.rect.topleft)
        
        self.draw_boss_hp_bar(display)

    def check_collision_with_bullet(self, world: World):
        for e in world.entities:
            if type(e).__name__ == "PlayerBullet" and e.rect.colliderect(self.rect) and not e.exploded:
                if time() - self.last_shot > 0.3:
                    if world.player.gun_perk_expire_time > time():
                        self.hp -= int(BulletConfig.Damage / 1.5)
                    else:
                        self.hp -= int(BulletConfig.Damage / 3)
                    self.hurt = True
                    self.last_hp_deplete_time = time()
                    self.last_shot = time()
                    if self.hp <= 0:
                        self.alive = False
    
    def draw_boss_hp_bar(self, display):
        
        self.hp_bar_rect = rect.Rect(0, 20, 300, 60)
        self.hp_bar_rect.centerx = int(get_window_size()[0] / 2) 
        draw.rect(display, (231, 172, 251), self.hp_bar_rect, 4, 10)
        draw.rect(display, (231, 172, 251), rect.Rect(self.hp_bar_rect.left + 10, self.hp_bar_rect.top + 10, (self.hp_bar_rect.width - 20) *  self.hp / BossConfig.Hp, self.hp_bar_rect.height - 20), 0, 10)