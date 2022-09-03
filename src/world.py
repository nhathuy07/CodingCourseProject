from math import floor
from common import types
from common.config import DISPLAY_SCALING
from common.types import Items, Levels, Scheme
from session import Session
from entities.ground import Ground

class World:
    def __init__(self, session: Session, level: Levels) -> None:
        self.level = level
        self.scheme = Scheme[session.level_data[self.level.name]["Scheme"]]
        self.entities_map = [
            [1, 1, 1, 1, 0, 0],
            [1, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 1, 0],
            [1, 1, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1]
        ]
        self.goal = {}
        self.collected = {}
        self.entities = []
        self.load_terrain(session)
        self.load_bg(session)
    def load_bg(self, session: Session):
        self.bg = session.background[self.scheme.value]
    def load_terrain(self, session: Session):
        for i in range(len(self.entities_map)):
            for j in range(len(self.entities_map[i])):
                if self.entities_map[i][j] == 1:
                    position = (floor(j * 59 * DISPLAY_SCALING), floor(i * 59 * DISPLAY_SCALING))

                    # check if faces are NOT covered
                    top_face = i > 0 and self.entities_map[i - 1][j] != 1
                    right_face = j < (len(self.entities_map[i]) - 1) and self.entities_map[i][j + 1] != 1
                    left_face = j > 0 and self.entities_map[i][j - 1] != 1
                    bottom_face = i < len(self.entities_map) - 1 and self.entities_map[i + 1][j] != 1

                    # No face
                    if not top_face and not right_face and not left_face and not bottom_face:
                        ground_type = types.Ground.NoFace
                    
                    # One face
                    if top_face and not right_face and not left_face and not bottom_face:
                        ground_type = types.Ground.UpFace
                    if right_face and not top_face and not left_face and not bottom_face:
                        ground_type = types.Ground.RightFace
                    if left_face and not top_face and not right_face and not bottom_face:
                        ground_type = types.Ground.LeftFace
                    if bottom_face and not top_face and not left_face and not right_face:
                        ground_type = types.Ground.DownFace
                    
                    # Two face
                    if left_face and right_face and not top_face and not bottom_face:
                        ground_type = types.Ground.FacingLeftRight
                    if top_face and bottom_face and not left_face and not right_face:
                        ground_type = types.Ground.FacingTopBottom
                    if left_face and top_face and not bottom_face and not right_face:
                        ground_type = types.Ground.LeftUpFace
                    if left_face and bottom_face and not top_face and not right_face:
                        ground_type = types.Ground.LeftDownFace
                    if right_face and bottom_face and not top_face and not left_face:
                        ground_type = types.Ground.RightDownFace
                    if right_face and top_face and not left_face and not bottom_face:
                        ground_type = types.Ground.RightUpFace

                    # Three face
                    if left_face and bottom_face and left_face and not right_face:
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
                    self.entities.append(Ground(session, ground_type, self.scheme, position[0], position[1]))

    def update(self, display):
        display.fill((0, 0, 0))
        display.blit(self.bg, (0, 0))
        for e in self.entities:
            display.blit(e.image, (e.x, e.y))
