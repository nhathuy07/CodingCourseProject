from common.config import DISPLAY_SCALING, FONT
from entities import player
from session import Session
from pygame import font


class HPPane:
    def __init__(self, x, y, session: Session, player: player.Player) -> None:
        self.x = x
        self.y = y
        self.image = session.HP_PANE
        self.font = font.Font(FONT[0], 24)
        self.hp = player.hp

    def update(self, player: player.Player):
        self.hp = player.hp
        self.disp = self.font.render(str(self.hp), True, (255, 255, 255))

    def render(self, player: player.Player, display):
        self.update(player)
        display.blit(self.image, (self.x, self.y))
        display.blit(
            self.disp,
            (
                self.x + 80 * DISPLAY_SCALING,
                self.y + (self.image.get_height() - self.font.get_height()) / 2,
            ),
        )
