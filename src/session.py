import csv

import os

from typing import Dict


from pygame import Surface, rect, mixer

from common import paths
from common import utils
from common.config import DISPLAY_SCALING
from common.paths import ASSETS_PATH
#from common.types import BossState, Ground, Items, MobState, Mobs, PlayerState, Projectiles, Scheme
from common.utils import load_img
from common import extra_types
mixer.init()

class Session():
    def __init__(self):
        import json
        from pathlib import Path

        from pygame import display



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

        for item_index in range(len(extra_types.Items._member_names_)):
            item_name = extra_types.Items._member_names_[item_index]
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

        # load level data
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

        # load level menu background
        self.lv_selection_bg = utils.load_img(self.lv_selection_bg_dir)

        # load collectibles
        self.collectible_dir = paths.ASSETS_PATH / "items" / "collectibles"
        self.collectibles: Dict[str, Dict[str, Surface]] = {}
        for c in extra_types.Collectibles:
            self.collectibles[c.name] = {}
            self.collectibles[c.name]["Base"] = utils.load_img(
                self.collectible_dir / c.name.lower() / "Base.png"
            )
            if (self.collectible_dir / c.name.lower() / "GlowFx.png").exists():
                self.collectibles[c.name]["GlowFx"] = utils.load_img(
                    self.collectible_dir / c.name.lower() / "GlowFx.png"
                )
            else:
                self.collectibles[c.name]["GlowFx"] = None

            if (self.collectible_dir / c.name.lower() / "Full.png").exists():
                self.collectibles[c.name]["Full"] = utils.load_img(
                    self.collectible_dir / c.name.lower() / "Full.png"
                )
            else:
                self.collectibles[c.name]["Full"] = None

        # load ground textures
        self.ground_texture_dir = paths.ASSETS_PATH / "ground"
        self.ground_texture = {}
        for s in extra_types.Scheme:
            self.ground_texture[s.value] = {}
            for variation in extra_types.Ground._member_names_:
                if (self.ground_texture_dir / str(s.value) / f"{variation.lower()}.png").exists():
                    self.ground_texture[s.value][variation] = utils.load_img(
                        self.ground_texture_dir / str(s.value) / f"{variation.lower()}.png"
                    )
                else:
                    self.ground_texture[s.value][variation] = utils.load_img(
                        self.ground_texture_dir / str(s.value) / "Base.png"
                    )

        # load liquid textures
        self.liquid_texture_dir = paths.ASSETS_PATH / "liquid"
        self.liquid_texture = {}
        for l in self.liquid_texture_dir.glob("*.png"):
            self.liquid_texture[l.name.removesuffix(".png")] = load_img(l)

        # load level backgrounds
        self.level_bg_dir = paths.ASSETS_PATH / "background" / "levels"
        self.background = tuple(
            map(utils.load_img, Path(self.level_bg_dir).glob("*.png"))
        )

        # Load player sprite
        self.player_sprite = {}
        for sprite in extra_types.PlayerState:
            self.player_sprite[sprite.name] = load_img(
                self.character_sprite_dir / "Mark" / f"{sprite.name}.png", 0.7
            )

        # UI elements
        # Preloader UI
        self.preloader_bg_dir = paths.ASSETS_PATH / "background" / "LevelLoading.png"
        self.preloader_bg = utils.load_img(self.preloader_bg_dir)

        self.preloader_frame_dir = paths.ASSETS_PATH / "icons" / "goalScreen.png"
        self.preloader_frame = utils.load_img(self.preloader_frame_dir)

        self.CLICK_PROMPT = load_img(
            ASSETS_PATH / "icons" / "click-tap-svgrepo-com.png", 1.3
        )

        # Panes
        self.ITEM_PANE = load_img(ASSETS_PATH / "icons" / "itemPane.png")
        self.INVENTORY_PANE = load_img(ASSETS_PATH / "icons" / "inventoryPane.png")
        self.INVENTORY_PANE_2 = load_img(ASSETS_PATH / "icons" / "inventoryPane2.png")
        self.HP_PANE = load_img(ASSETS_PATH / "icons" / "hpPane.png")
        self.WEAPON_PERK_TIMER_PANE = load_img(ASSETS_PATH / "icons" / "weaponPerkTimer.png")

        # --VISUAL FX--
        # Propelling effect
        self.TRAIL_PARTICLE_FX = load_img(ASSETS_PATH / "fx" / "trail.png")

        # Bullet explosion effect
        self.BULLET_EXPLOSION = load_img(ASSETS_PATH / "fx" / "bullet_explosion.png")
        self.ENEMY_BULLET_EXPLOSION = load_img(ASSETS_PATH / "fx" / "enemy_bullet_explosion.png")
        # Dripstone dropping effect
        self.DRIPSTONE_FALLING = load_img(ASSETS_PATH / "fx" / "dripstone_falling.png")

        # Reduced sight effect
        self.REDUCED_SIGHT = load_img(ASSETS_PATH / "fx" / "reduced_sight.png")
        self.REDUCED_SIGHT_RECT = self.REDUCED_SIGHT.get_rect()
        
        # Mission Completed
        self.MISSION_COMPLETED_SCR = load_img(ASSETS_PATH / "icons" / "missionCompletedScreen.png")
        
        # Boss death effect
        self.BOSS_DEATH_DIR = ASSETS_PATH / "mobs" / "Boss" / "Dying"
        self.BOSS_DEATH = tuple(map(load_img, self.BOSS_DEATH_DIR.glob("*.png")))

        ## --LOAD PROJECTILES---
        self.projectile_dir = ASSETS_PATH / "projectiles"
        self.projectile = {}
        for p in extra_types.Projectiles._member_names_:
            self.projectile[p] = []
            for f in (self.projectile_dir / p).glob("*.png"):
                self.projectile[p].append(load_img(f))

        # load mobs
        self.mobs_dir = ASSETS_PATH / "mobs"
        self.mobs = {}
        for p in extra_types.Mobs._member_names_:
            self.mobs[p] = {}
            for d in (self.mobs_dir / p).glob("*"):
                for m in extra_types.MobState._member_names_:
                    self.mobs[p][m] = list(
                        map(load_img, Path(self.mobs_dir / p.lower() / m.lower()).glob("*"))
                    )

        # load boss
        self.boss_sprite_dir = self.mobs_dir / "Boss"
        self.boss_sprite = {}
        
        for p in extra_types.BossState._member_names_:
            self.boss_sprite[p] = {}
            for i in ("Original", "Hurt"):
                self.boss_sprite[p][i] = load_img(self.boss_sprite_dir / i / f"{p}.png") # syntax: self.boss_sprite[state][is_hurt]

        # Load outro
        self.OUTRO = load_img(ASSETS_PATH / "outro" / "0.png")

        ## AUDIO ##
        self.sfx_path = ASSETS_PATH / "sfx"
        self.sfx = {}
        for i in Path(self.sfx_path).glob("*.wav"):
            self.sfx[i.name] = mixer.Sound(i)

    def load_or_create_savefile(self):
        import json

        from common import paths

        self.userSavefilePath = paths.DATA_PATH / "player_savefile.json"
        if os.path.exists(str(self.userSavefilePath)):
            with open(self.userSavefilePath, "r") as saveFileIOWrapper:
                self.playerData = json.load(saveFileIOWrapper)
        else:
            self.override_savefile()

    def add_item(self, item: extra_types.Items):
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
        from common import extra_types

        if self.playerData["current_lvl"] == None:
            self.section = extra_types.GameSection.INTRO
        elif 1 <= self.playerData["current_lvl"] <= 4:
            self.section = extra_types.GameSection.value(self.playerData["current_lvl"])

    def set_lvl(self, new_lvl):
        self.playerData["current_lvl"] = new_lvl

    def get_lvl(self):
        return self.playerData["current_lvl"]

    def is_newgame(self):
        if len(self.playerData["earned_items"]) == 0:
            return True
        else:
            return False
    def base_level_completed(self):
        if len(self.playerData["earned_items"]) >= 4:
            return True
        else:
            return False