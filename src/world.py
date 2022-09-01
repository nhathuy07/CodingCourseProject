from common.types import Items
from session import Session


class World:
    def __init__(self, session: Session, item: Items) -> None:
        self.entities = []
        self.goal = {}
