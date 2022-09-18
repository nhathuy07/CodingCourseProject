from webbrowser import get
from common import events
from common.config import BossConfig, get_window_size
import entities
from entities.enemy_boss import EnemyBoss
from world import World
from session import Session
from common.extra_types import Levels
from pygame import event, draw, rect
class BossLevel(World):
    def __init__(self, session: Session, level: Levels) -> None:
        super().__init__(session, level)
        # remove inventory pane
        self.inventory_pane = None
    def load_entities(self, session: Session):
        super().load_entities(session)
        self.entities.append(EnemyBoss(session))
    def inventory_check(self, session: Session):
        """Override with blank function as there's no goals related to collectibles"""
    def spawn_mob(self, session: Session):
        """Override with blank function as there's no mobs"""
    def update(self, session: Session, display, fps):
        super().update(session, display, fps)
        for e in self.entities:
            if type(e).__name__ == "EnemyBullet":
                if self.player.rect.colliderect(e.rect):
                    self.player.inflict_damage(e.damage, 0.4, 0, None, self)
                if e.alpha <= 0:
                    self.entities.remove(e)
        
        if self.player.rect.top > get_window_size()[1]:
            self.player.inflict_damage(100, 0, 0)
            
    
    

            