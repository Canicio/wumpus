

class Constants:
    DIRECTION_LEFT = 0
    DIRECTION_UP = 1
    DIRECTION_RIGHT = 2
    DIRECTION_DOWN = 3

    DRAW_ASCII_LEFT = u'\u2190'
    DRAW_ASCII_UP = u'\u2191'
    DRAW_ASCII_RIGHT = u'\u2192'
    DRAW_ASCII_DOWN = u'\u2193'

    PERCEPTION_WUMPUS_STENCH = 0
    PERCEPTION_WATER_WELL_BREEZE = 1
    PERCEPTION_GOLD_SHINE = 2
    PERCEPTION_SHOCK = 3
    PERCEPTION_WUMPUS_SCREAM = 4

    OPTION_MENU_GO = 1
    OPTION_MENU_ROTATE_90_DEGREES_LEFT = 2
    OPTION_MENU_ROTATE_90_DEGREES_RIGHT = 3
    OPTION_MENU_THROW_ARROW = 4
    OPTION_MENU_OUT_WIN = 5
    OPTION_MENU_QUIT_GAME = 6

    MSG_EXCEPTION_LOAD_BOARD_ELEMENT = "Too many attempts to load element on the board"


class InfoException(Exception):
    pass