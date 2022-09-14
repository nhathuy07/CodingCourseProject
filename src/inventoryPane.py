from typing import Dict
from common.config import DISPLAY_SCALING, FONT, FONT2, get_window_size
from common.events import ITEM_COLLECTED

from session import Session
from pygame import transform, font, event
import time


class InventoryPane:
    def __init__(self, session: Session, inventory: Dict[str, int], x=0, y=20) -> None:
        self.x = x
        self.y = y
        self.image = session.INVENTORY_PANE
        self.image2 = session.INVENTORY_PANE_2
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)
        self.font = font.Font(FONT[0], 24)
        # load player's inventory
        self.inventory = inventory
        self.last_item_collection_time = 0

        self.auto_center_x()

    def auto_center_x(self):
        # automatically align InventoryPane horizontally
        self.x = (get_window_size()[0] - self.rect.width) / 2
        self.rect.x = self.x

    def update(self, inventory: Dict[str, int]):
        # update player's inventory
        self.inventory = inventory

    def render(self, session: Session, display, inventory):
        self.update(inventory)
        # calculate how many item types there are in player's inventory
        inventory_length = len(self.inventory)

        for e in event.get(ITEM_COLLECTED):
            if e.type == ITEM_COLLECTED:
                self.last_item_collection_time = time.time()

        # show inventory pane
        if (time.time() - self.last_item_collection_time) <= 0.2:
            # show effect for 0.2 secs after collecting item
            display.blit(self.image2, self.rect.topleft)
            self.rect = self.image2.get_rect()
            self.auto_center_x()
            self.rect.y = self.y - 3
        else:
            display.blit(self.image, self.rect.topleft)
            self.rect = self.image.get_rect()
            self.auto_center_x()
            self.rect.y = self.y

        # show items that are in player's inventory
        for i in range(len(self.inventory)):
            size = 80 * DISPLAY_SCALING
            current_item_img = transform.smoothscale(
                session.collectibles[list(self.inventory.keys())[i]]["Full"],
                (size, size),
            )

            # item counter
            text = self.font.render(
                str(inventory[list(self.inventory.keys())[i]]), True, (255, 255, 255)
            )
            # align items automatically
            current_item_pos = (
                ((self.rect.width / inventory_length) - size - text.get_width() - 10)
                / 2
                + (self.rect.width / inventory_length * i)
                + self.rect.x,
                (self.rect.height - size) / 2 + self.rect.y,
            )
            display.blit(current_item_img, current_item_pos)

            display.blit(
                text,
                (
                    current_item_pos[0] + size,
                    (self.rect.height - text.get_height()) / 2 + self.rect.y,
                ),
            )
