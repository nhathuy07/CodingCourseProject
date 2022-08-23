
class Session:
    def __init__(self):
        self.section = None
        self.earnedItems = []
    def load_savefile(self):
        import json
        import pathlib
        from common import paths
        userSavefilePath = paths.DATA_PATH / "player_savefile.json"
        saveFile = open(userSavefilePath, "r")
        self.earnedItems = json.load(saveFile)["earned_items"]

s = Session()
s.load_savefile()
print(s.earnedItems)