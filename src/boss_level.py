from common.config import BossConfig
import entities
from entities.enemy_boss import EnemyBoss
from world import World
from session import Session
from common.extra_types import Levels
class BossLevel(World):
    def __init__(self, session: Session, level: Levels) -> None:
        super().__init__(session, level)
    def load_entities(self, session: Session):
        super().load_entities(session)
        self.entities.append(EnemyBoss(session))
    def inventory_check(self, session: Session):
        """Override with blank function as there's no collectibles"""
    def spawn_mob(self, session: Session):
        """Override with blank function as there's no mobs"""
    def update(self, session: Session, display, fps):
        super().update(session, display, fps)
        for e in self.entities:
            if type(e).__name__ == "EnemyBullet" and self.player.rect.colliderect(e.rect):
                self.player.inflict_damage(BossConfig.Damage, 0.4, 0, None, self)