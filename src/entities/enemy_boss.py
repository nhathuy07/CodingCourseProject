from random import randint, random
from secrets import choice
from time import time
from common.config import BossConfig, get_window_size
from common.types import BossState
from src import session
from world import World
class EnemyBoss():
    def __init__(self, session: session.Session, config = BossConfig) -> None:
        self.x = get_window_size()[0] / 2
        self.y = get_window_size()[1] / 2
        self.sprites = session.boss_sprite
        self.dx = config.Dx
        self.dy = config.Dy
        self.damage = 25
        self.simultaneous_bullet_spawn = config.SimultaneousBulletSpawn
        self.simultaneous_meteorite_spawn = config.SimultaneousMeteoriteSpawn
        self.instakill_possibility = config.InstakillPosibilities
        self.growl_knockback_distance = config.GrowlKnockbackDistance

        # attack time settings
        self.attack_duration = 0.2
        self.last_attack = time()
        self.last_attack_expire_time = 0

        self.state = BossState.Idle

    def update(self, world: World):
        # choose an attack method randomly
        self.attack_interval = randint(2, 4)
        
        if time() - self.last_attack >= self.attack_interval and self.state == BossState.Idle:
            self.state = choice(BossState.Growling, BossState.SpittingBullet, BossState.DroppingBomb)
            self.last_attack_expire_time = time() + self.attack_duration
        
        # attack player using the chosen method
        if time() <= self.last_attack_expire_time:
            if self.state == BossState.Growling:
                world.player.inflict_damage(4, 0.1, knockback = 22, entities = world.entities)
        