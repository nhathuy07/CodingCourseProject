import ctypes
from math import floor
from common import types
from common.config import DISPLAY_SCALING, FONT, PlayerConfig, get_window_size
from common.events import EMIT_TRAIL_PARTICLE, GO_TO_LV_SELECTION, ITEM_COLLECTED, PLAYER_DIED
from common.types import Collectibles, Items, Levels, Liquid, Scheme
from hpPane import HPPane
from inventoryPane import InventoryPane
from session import Session
from entities.ground import Ground
from entities import collectible, liquid, player
from pygame import font, event, MOUSEBUTTONDOWN, MOUSEBUTTONUP, QUIT, KEYDOWN, KEYUP

from trail_fx import TrailFx

class World:
    def __init__(self, session: Session, level: Levels) -> None:
        self.level = level
        self.scheme = Scheme[session.level_data[self.level.name]["Scheme"]]
        self.entities_map = session.level_data[self.level.name]["MapData"]
        self.goal = session.level_data[self.level.name]["Items"]
        self.entities = []
        self.effects = []
        self.player = player.Player(session)
        self.load_bg(session)
        self.load_entities(session)
        self.load_terrain(session)
        self.font = font.Font(FONT[0], 16)
        self.inventory_pane = InventoryPane(session, self.player.inventory)
        self.hp_pane = HPPane(get_window_size()[0] - 10 - session.HP_PANE.get_width(), self.inventory_pane.rect.y, session, self.player)
        
        self.delta_screen_offset = 0
        self.abs_screen_offset = 0
        self.min_abs_screen_offset = get_window_size()[0] - len(self.entities_map[0]) * 60 * DISPLAY_SCALING

        self.retry_prompt = False

        event.set_allowed((KEYUP, KEYDOWN, MOUSEBUTTONDOWN, ITEM_COLLECTED, PLAYER_DIED, GO_TO_LV_SELECTION, Items[self.level.name].value))

    def load_bg(self, session: Session):
        self.bg = session.background[self.scheme.value]

    def load_terrain(self, session: Session):
        for i in range(len(self.entities_map)):
            for j in range(len(self.entities_map[0])):
                if int(self.entities_map[i][j]) == 1:
                    position = (j * 60 * DISPLAY_SCALING, i * 60 * DISPLAY_SCALING)

                    # check if faces are NOT covered
                    top_face = i > 0 and self.entities_map[i - 1][j] != "1"
                    right_face = (
                        j < (len(self.entities_map[i]) - 1)
                        and self.entities_map[i][j + 1] != "1"
                    )
                    left_face = j > 0 and self.entities_map[i][j - 1] != "1"
                    bottom_face = (
                        i < len(self.entities_map) - 1
                        and self.entities_map[i + 1][j] != "1"
                    )

                    # No face
                    if (
                        not top_face
                        and not right_face
                        and not left_face
                        and not bottom_face
                    ):
                        ground_type = types.Ground.NoFace

                    # One face
                    if (
                        top_face
                        and not right_face
                        and not left_face
                        and not bottom_face
                    ):
                        ground_type = types.Ground.UpFace
                    if (
                        right_face
                        and not top_face
                        and not left_face
                        and not bottom_face
                    ):
                        ground_type = types.Ground.RightFace
                    if (
                        left_face
                        and not top_face
                        and not right_face
                        and not bottom_face
                    ):
                        ground_type = types.Ground.LeftFace
                    if (
                        bottom_face
                        and not top_face
                        and not left_face
                        and not right_face
                    ):
                        ground_type = types.Ground.DownFace

                    # Two face
                    if (left_face and right_face and not top_face and not bottom_face):
                        ground_type = types.Ground.FacingLeftRight
                    if (top_face and bottom_face and not left_face and not right_face):
                        ground_type = types.Ground.FacingTopBottom
                    if (left_face and top_face and not bottom_face and not right_face):
                        ground_type = types.Ground.LeftUpFace
                    if (left_face and bottom_face and not top_face and not right_face):
                        ground_type = types.Ground.LeftDownFace
                    if (right_face and bottom_face and not top_face and not left_face):
                        ground_type = types.Ground.RightDownFace
                    if (right_face and top_face and not left_face and not bottom_face):
                        ground_type = types.Ground.RightUpFace

                    # Three face
                    if left_face and bottom_face and right_face and not top_face:
                        ground_type = types.Ground.FacingBottomLeftRight
                    if top_face and left_face and bottom_face and not right_face:
                        ground_type = types.Ground.FacingTopLeftBottom
                    if top_face and right_face and bottom_face and not left_face:
                        ground_type = types.Ground.FacingTopRightBottom
                    if top_face and left_face and right_face and not bottom_face:
                        ground_type = types.Ground.FacingTopLeftRight

                    # All face
                    if top_face and right_face and left_face and bottom_face:
                        ground_type = types.Ground.FacingAll
                    self.entities.append(
                        Ground(
                            session, ground_type, self.scheme, position[0], position[1]
                        )
                    )

    def load_entities(self, session: Session):
        for i in range(len(self.entities_map)):
            for j in range(len(self.entities_map[i])):
                # load Liquid entity
                if int(self.entities_map[i][j]) in [v.value for v in Liquid]:
                    pos = (j * 60 * DISPLAY_SCALING, i * 60 * DISPLAY_SCALING)
                    entityNo = int(self.entities_map[i][j])
                    self.entities.append(
                        liquid.Liquid(session, pos[0], pos[1], Liquid(entityNo))
                    )
                elif int(self.entities_map[i][j]) in [v.value for v in Collectibles]:
                    pos = (j * 60 * DISPLAY_SCALING, (i * 60 * DISPLAY_SCALING) + 13)
                    entityNo = int(self.entities_map[i][j])
                    self.entities.append(
                        collectible.Collectible(Collectibles(entityNo), session, pos[0], pos[1])
                    )

    def update(self, session: Session, display, fps):
        display.fill((0, 0, 0))
        display.blit(self.bg, (0, 0))
        self.player.update(display, self.entities, session, self)
        for e in self.entities:
            
            if type(e).__name__ == "PlayerBullet":
                e.update(self.entities)
                if e.alpha <= 0:
                    self.entities.remove(e)
                else:
                    e.rect.x += self.delta_screen_offset
                    e.render(display, self.entities)
            else:
                e.rect.left = e.init_coord[0] + self.abs_screen_offset
                e.render(display)

        for e in event.get((EMIT_TRAIL_PARTICLE, PLAYER_DIED)):
            if e.type == EMIT_TRAIL_PARTICLE:
                self.effects.append(TrailFx(self.player.rect.x + self.player.particle_relative_position[0], self.player.rect.y + self.player.particle_relative_position[1], session, self.player.dx))
            elif e.type == PLAYER_DIED:
                
                if not self.retry_prompt:
                    ret_val = ctypes.windll.user32.MessageBoxW(0, "Your character is damaged. Retry?", "Mission failed", 0x04 | 0x10)
                    self.retry_prompt = True
                if ret_val == 6:
                    event.post(event.Event(Items[self.level.name].value))
                elif ret_val == 7:
                    event.post(event.Event(GO_TO_LV_SELECTION))

        for e in self.effects:
            e.update()
            e.x += self.delta_screen_offset
            e.render(display)
            if e.alpha <= 0:
                self.effects.remove(e)
        
        f = self.font.render(f"{self.delta_screen_offset}", True, (255, 255, 255))
        display.blit(f, (10, 10))
        
        self.inventory_pane.render(session, display, self.player.inventory)
        self.hp_pane.render(self.player, display)
    
        self.player.render(display)
    
    def update_world_offset(self, delta):
        # Code from S4V - CS102 - Lesson 6 - Milestone 3
        # do not let abs_screen_offset becomes > 0, to prevent overscroll to the left
        new_abs_screen_offset = min(0, self.abs_screen_offset + delta)
         # prevent overscroll to the right
        new_abs_screen_offset = max(new_abs_screen_offset, self.min_abs_screen_offset)
        self.delta_screen_offset = new_abs_screen_offset - self.abs_screen_offset
        self.abs_screen_offset = new_abs_screen_offset
    
    def at_left_most(self):
        # Code from S4V - CS102 - Lesson 6 - Milestone 3
        return self.abs_screen_offset >= 0
    
    def at_right_most(self):
        return self.abs_screen_offset <= self.min_abs_screen_offset