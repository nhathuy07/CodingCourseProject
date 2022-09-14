from time import time
from common.config import DISPLAY_SCALING, FONT, PlayerConfig
from entities import player
from session import Session
from pygame import font


class GunPerkTimerPane:
    def __init__(self, x, y, session: Session, player: player.Player) -> None:
        self.x = x
        self.y = y
        self.image = session.WEAPON_PERK_TIMER_PANE
        self.font = font.Font(FONT[0], 24)
        self.timer = round(time() - player.gun_perk_expire_time, 1)

    def update(self, player: player.Player):
        self.timer = round(player.gun_perk_expire_time - time(), 1)
        self.disp = self.font.render(str(self.timer), True, (255, 255, 255))

    def render(self, player: player.Player, display):
        if time() <  player.gun_perk_expire_time:
            self.update(player)
            display.blit(self.image, (self.x, self.y))
            display.blit(
                self.disp,
                (
                    self.x + 80 * DISPLAY_SCALING,
                    self.y + (self.image.get_height() - self.font.get_height()) / 2,
                ),
            )