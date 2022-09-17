from common.config import TRANSISTION_SPEED
from session import Session
from pygame import event, MOUSEBUTTONDOWN
from common.events import GO_TO_LV_SELECTION

class MissionCompletedScr():
    def __init__(self, session: Session):
        event.set_allowed((GO_TO_LV_SELECTION, MOUSEBUTTONDOWN))
        self.image = session.MISSION_COMPLETED_SCR
        self.alpha = 0
        self.sound = session.sfx["mission_completed.wav"]
        self.sound_played = False
    def update(self, display):
        if not self.sound_played:
            self.sound.play()
            self.sound_played = True
        for e in event.get(MOUSEBUTTONDOWN):
            if e.type == MOUSEBUTTONDOWN:
                event.post(event.Event(GO_TO_LV_SELECTION))
        if self.alpha < 255:
            self.alpha += TRANSISTION_SPEED
        else:
            self.alpha = 255
        self.image.set_alpha(self.alpha)
        display.blit(self.image, (0, 0))