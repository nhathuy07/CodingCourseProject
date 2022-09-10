from common import types
from common.config import (
    DISPLAY_SCALING,
    FONT,
    FONT2,
    TRANSISTION_SPEED,
    get_window_size,
)
from session import Session
from pygame import event as pg_event, font as pg_font, draw as pg_draw, rect as pg_rect


class PreLoadScr:
    def __init__(self, session: Session, objective: types.Items) -> None:
        self.objective = objective
        self.bg_offset_y = 0
        self.items_count = len(session.level_data[self.objective.name]["Items"])
        self.frame_size = (
            session.preloader_frame.get_width(),
            session.preloader_frame.get_height(),
        )
        self.step = 0
        self.FONT2 = pg_font.Font(FONT2[0], FONT2[1] * 2)

    def update(self, session: Session, display):
        self.step = 0
        display.fill((0, 0, 0))

        # display scrolling animation
        if self.bg_offset_y > -165:
            display.blit(session.preloader_bg, (0, self.bg_offset_y))
            self.bg_offset_y -= 0.5

            display.blit(
                session.preloader_frame,
                (
                    (get_window_size()[0] - session.preloader_frame.get_width()) / 2,
                    (get_window_size()[1] - session.preloader_frame.get_height()) / 2,
                ),
            )
            for key in session.level_data[self.objective.name]["Items"]:
                display.blit(
                    session.collectibles[key.upper()]["Full"],
                    (
                        (
                            (self.frame_size[0] / self.items_count)
                            - session.collectibles[key.upper()]["Full"].get_width()
                        )
                        / 2
                        + (self.frame_size[0] / self.items_count * self.step)
                        + (
                            (get_window_size()[0] - session.preloader_frame.get_width())
                            / 2
                        ),
                        280 * DISPLAY_SCALING,
                    ),
                )
                required_items_count = session.level_data[self.objective.name]["Items"][key]
                disp = self.FONT2.render(str(required_items_count), True, (0, 104, 170))
                disp_rect = disp.get_rect()

                disp_rect.topleft = (
                    (
                        (self.frame_size[0] / self.items_count)
                        - session.collectibles[key.upper()]["Full"].get_width()
                    )
                    / 2
                    + (self.frame_size[0] / self.items_count * self.step)
                    + (
                        (get_window_size()[0] - session.preloader_frame.get_width()) / 2
                    ),
                    480 * DISPLAY_SCALING,
                )
                # pg_draw.rect(display, (208, 237, 255), pg_rect.Rect(disp_rect.x + 30, disp_rect.y, session.collectibles[key.upper()].get_width() - 60, disp_rect.height), 5, 15)
                frame = pg_draw.rect(
                    display,
                    (208, 237, 255),
                    pg_rect.Rect(
                        disp_rect.x + 30,
                        disp_rect.y,
                        session.collectibles[key.upper()]["Full"].get_width() - 60,
                        disp_rect.height,
                    ),
                    0,
                    15,
                )
                disp_rect.center = frame.center

                display.blit(disp, disp_rect.topleft)
                self.step += 1

        else:
            event = types.Levels[self.objective.name].value
            pg_event.post(pg_event.Event(event))
