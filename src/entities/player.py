from common.config import DISPLAY_SCALING, PlayerConfig
from common.types import PlayerState
from session import Session
from pygame import Surface, Rect



class Player:
    def __init__(self, session: Session, x = PlayerConfig.InitX, y = PlayerConfig.InitY, dx = PlayerConfig.MovingSpd, dy = PlayerConfig.JumpingSpd, gravity = PlayerConfig.Gravity) -> None:
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = 0
        self.sprites = session.player_sprite
        self.state: PlayerState = PlayerState.Idle
        self.gravity = gravity
        self.rect = Rect(self.x, self.y, 94 * DISPLAY_SCALING, 170 * DISPLAY_SCALING)
        self.current_jumping_spd = 0
        self.y_offset = 0
        self.floating_effect_direction = "up"
    def update_collision(self, terrain):
        self.dy += self.gravity
        
        for t in terrain:
            if t.rect.colliderect(self.rect.x, self.rect.y + self.dy, self.rect.width, self.rect.height):
                if self.dy > 0:
                    self.dy = t.rect.top - self.rect.bottom
                elif self.dy < 0:
                    self.dy = t.rect.bottom - self.rect.top
        self.rect.y += self.dy
    def floating_effect(self):
        if self.y_offset < -7:
            self.floating_effect_direction = "down"
        elif self.y_offset > 7:
            self.floating_effect_direction = "up"
        if self.floating_effect_direction == "up":
            self.y_offset -= 0.2
        else:
            self.y_offset += 0.2
    def update(self, display: Surface, terrain):
        self.update_collision(terrain)
        if self.state == PlayerState.Idle:
            self.floating_effect()
        display.blit(self.sprites[self.state.name], (self.rect.x, self.rect.y + self.y_offset))