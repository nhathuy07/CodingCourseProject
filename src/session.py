
from typing import Optional, Dict
from common.types import Items
import os

class Session:
    def __init__(self):
        import json
        from common import paths, utils
        from pathlib import Path
        from pygame import display, transform
        display.init()
        display.set_mode()
        self.section = None
        self.world = None
        self.playerData = {
            "current_lvl" : None,
            "earned_items": [],
        }
        self.dialogue_path = paths.DATA_PATH / "dialogues.json"
        self.character_sprite_dir = paths.ASSETS_PATH / "characters"
        with open(self.dialogue_path, "r") as dialogueFileIOWrapper:
            self.dialogue_data = json.load(dialogueFileIOWrapper)
        
        self.avatars = {}
        for x in Path(self.character_sprite_dir).glob("*"):
            self.avatars[os.path.basename(str(x))] = utils.image_scale(utils.load_img(str(os.path.join(x, "Avatar.png"))).convert_alpha(), 0.8)

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
