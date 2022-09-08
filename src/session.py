import csv
from typing import Optional, Dict
from common import types
from common.config import DISPLAY_SCALING, FONT
from common.types import Ground, Items, Levels, PlayerState, Scheme
import os
from pygame import rect, Surface

from common.utils import load_img


class Session:
    def __init__(self):
        import json
        from common import paths, utils
        from pathlib import Path
        from pygame import display, transform, font

        display.init()
        display.set_mode()
        
        self.section = None
        self.world = None
        self.playerData = {
            "current_lvl": None,
            "earned_items": [],
        }
        self.dialogue_path = paths.DATA_PATH / "dialogues.json"
        self.character_sprite_dir = paths.ASSETS_PATH / "characters"

        self.lv_selection_bg_dir = paths.ASSETS_PATH / "background" / "Menu.png"

        self.game_item_dirs = paths.ASSETS_PATH / "items"
        self.game_items = {
            "positions": (
                (363.74, 772.44),
                (569.87, 778.7),
                (882.44, 776.49),
                (1100.59, 779.52),
            ),
        }
        self.rects: Dict[str, rect.Rect] = {}

        for item_index in range(len(Items._member_names_)):
            item_name = Items._member_names_[item_index]
            item_dir = self.game_item_dirs / f"{item_name.lower()}.png"
            item_greyscale_dir = self.game_item_dirs / f"{item_name.lower()}_gs.png"
            self.game_items[item_name] = [
                utils.load_img(item_dir),
                utils.load_img(item_greyscale_dir),
            ]
            self.rects[item_name] = utils.load_img(item_dir).get_rect()
            self.rects[item_name].topleft = (
                self.game_items["positions"][item_index][0] * DISPLAY_SCALING,
                self.game_items["positions"][item_index][1] * DISPLAY_SCALING,
            )

        with open(self.dialogue_path, "r") as dialogueFileIOWrapper:
            self.dialogue_data = json.load(dialogueFileIOWrapper)

        self.avatars = {}
        for x in Path(self.character_sprite_dir).glob("*"):
            self.avatars[os.path.basename(str(x))] = utils.image_scale(
                utils.load_img(str(os.path.join(x, "Avatar.png"))).convert_alpha(), 0.8
            )

        self.dialogue_scenes_path = paths.ASSETS_PATH / "dialogue_scenes"
        self.dialogue_scenes = tuple(
            map(utils.load_img, Path(self.dialogue_scenes_path).glob("*.png"))
        )

        self.map_path = paths.DATA_PATH / "levels"
        self.level_data_dir = paths.DATA_PATH / "level_data.json"
        with open(self.level_data_dir, "r") as levelDataFileIOWrapper:
            self.level_data = json.load(levelDataFileIOWrapper)
        for key in self.level_data:
            level_path = self.map_path / f"{str(key)}.csv"
            if level_path.exists():
                with open(str(level_path)) as o:
                    csvreader = csv.reader(o)
                    self.level_data[key]["MapData"] = tuple(csvreader)


        self.lv_selection_bg = utils.load_img(self.lv_selection_bg_dir)

        self.preloader_bg_dir = paths.ASSETS_PATH / "background" / "LevelLoading.png"
        self.preloader_bg = utils.load_img(self.preloader_bg_dir)

        self.preloader_frame_dir = paths.ASSETS_PATH / "icons" / "goalScreen.png"
        self.preloader_frame = utils.load_img(self.preloader_frame_dir)

        self.collectible_dir = paths.ASSETS_PATH / "items" / "collectibles"
        self.collectibles: Dict[str, Surface] = {}
        for c in types.Collectibles:
            self.collectibles[c.name] = utils.load_img(
                self.collectible_dir / f"{c.name.lower()}.png"
            )

        self.ground_texture_dir = paths.ASSETS_PATH / "ground"
        self.ground_texture = {}
        for s in Scheme:
            self.ground_texture[s.value] = {}
            for variation in Ground._member_names_:
                self.ground_texture[s.value][variation] = utils.load_img(self.ground_texture_dir / str(s.value) / f"{variation.lower()}.png")

        self.liquid_texture_dir = paths.ASSETS_PATH / "liquid"
        self.liquid_texture = {}
        for l in self.liquid_texture_dir.glob("*.png"):
            self.liquid_texture[l.name.removesuffix(".png")] = load_img(l)
                
        self.level_bg_dir = paths.ASSETS_PATH / "background" / "levels"
        self.background = tuple(map(utils.load_img, Path(self.level_bg_dir).glob("*.png")))

        self.player_sprite = {}
        for sprite in PlayerState:
            self.player_sprite[sprite.name] = load_img(self.character_sprite_dir / "Mark" / f"{sprite.name}.png")

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

        if self.playerData["current_lvl"] == None:
            self.section = types.GameSection.INTRO
        elif 1 <= self.playerData["current_lvl"] <= 4:
            self.section = types.GameSection.value(self.playerData["current_lvl"])

    def set_lvl(self, new_lvl):
        self.playerData["current_lvl"] = new_lvl

    def get_lvl(self):
        return self.playerData["current_lvl"]
