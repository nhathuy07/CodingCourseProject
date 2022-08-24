
from typing import Optional, Dict
from common.types import Items
import os

class Session:
    def __init__(self):
        self.section = None
        self.world = None
        self.playerData = {
            "current_lvl" : None,
            "earned_items": [],
        }
    def load_or_create_savefile(self):
        import json
        from common import paths
        self.userSavefilePath = paths.DATA_PATH / "player_savefile.json"
        if os.path.exists(str(self.userSavefilePath)):
            with open(self.userSavefilePath, "r") as saveFileIOWrapper:
                self.playerData = json.load(saveFileIOWrapper)
        else:
            self.override_savefile()

    def add_item(self, item: Items):
        if self.playerData["earned_items"].count(item.name) == 0:
            self.playerData["earned_items"].append(item.name)
        
    def update_savefile(self):
        import json
        from common import paths
        self.userSavefilePath = paths.DATA_PATH / "player_savefile.json"
        with open(self.userSavefilePath, "w") as saveFileIOWrapper:
            saveFileIOWrapper.write(json.dumps(self.playerData))
    
    def override_savefile(self):
        import json
        from common import paths
        self.userSavefilePath = paths.DATA_PATH / "player_savefile.json"
        with open(self.userSavefilePath, "w") as saveFileIOWrapper:
            self.playerData["earned_items"] = []
            self.playerData["current_lvl"] = None
            saveFileIOWrapper.write(json.dumps(self.playerData))

    def update_section(self):
        from common import types
        if self.playerData['current_lvl'] == None:
            self.section = types.GameSection.INTRO
        elif 1 <= self.playerData['current_lvl'] <= 4:
            self.section = types.GameSection.value(self.playerData['current_lvl'])
    
    def set_lvl(self, new_lvl):
        self.playerData['current_lvl'] = new_lvl
    def get_lvl(self):
        return self.playerData['current_lvl']