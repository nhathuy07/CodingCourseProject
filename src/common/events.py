from pygame import MOUSEBUTTONDOWN, QUIT, USEREVENT

from common.extra_types import Levels, Items

ABOUT = USEREVENT + 1
MAIN_MENU = USEREVENT + 2
PLAY = USEREVENT + 3
HELP = USEREVENT + 4
RESUME = USEREVENT + 5
EXIT = USEREVENT + 6
NEXT_DIALOG_SECTION = USEREVENT + 7
GO_TO_LV_SELECTION = USEREVENT + 8
INTRODUCTION_DIALOGUE = USEREVENT + 9
NEXT_DLG_LINE = USEREVENT + 10
PRELOAD_SCREEN = USEREVENT + 11
ITEM_COLLECTED = USEREVENT + 12
EMIT_TRAIL_PARTICLE = USEREVENT + 13
SHOOT = USEREVENT + 14
PLAYER_DIED = USEREVENT + 15
MISSION_COMPLETED = USEREVENT + 16
PAUSE = USEREVENT + 17
PRE_BOSS_LVL_DIALOGUE = USEREVENT + 18
BOSS_LVL_INTRO = USEREVENT + 19
BOSS_LVL_DIALOGUE = USEREVENT + 20
OUTRO = USEREVENT + 21
# load event codes
commonEvents = (
    PLAY,
    RESUME,
    ABOUT,
    MOUSEBUTTONDOWN,
    QUIT,
    INTRODUCTION_DIALOGUE,
    GO_TO_LV_SELECTION,
    PRELOAD_SCREEN,
)
preloaderCode = (x.value for x in Items)
levelCode = (x.value for x in Levels)
