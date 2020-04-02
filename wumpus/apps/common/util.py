

class Constants:
    DIRECTION_LEFT = 0
    DIRECTION_UP = 1
    DIRECTION_RIGHT = 2
    DIRECTION_DOWN = 3

    DRAW_ASCII_LEFT = u'\u25C0'
    DRAW_ASCII_UP = u'\u25B2'
    DRAW_ASCII_RIGHT = u'\u25B6'
    DRAW_ASCII_DOWN = u'\u25bc'

    PERCEPTION_WUMPUS_STENCH = 'wumpus stench'
    PERCEPTION_WATER_WELL_BREEZE = 'water well breeze'
    PERCEPTION_GOLD_SHINE = 'gold shine'
    PERCEPTION_SHOCK = 'shock!'
    PERCEPTION_WUMPUS_SCREAM = 'wumpus scream'

    OPTION_MENU_GO = 1
    OPTION_MENU_ROTATE_90_DEGREES_LEFT = 2
    OPTION_MENU_ROTATE_90_DEGREES_RIGHT = 3
    OPTION_MENU_THROW_ARROW = 4
    OPTION_MENU_OUT_WIN = 5
    OPTION_MENU_QUIT_GAME = 6

    MSG_EXCEPTION_LOAD_BOARD_ELEMENT = "Too many attempts to load element on the board"

    MSG_INFO_HUNTER_HUNTED_BY_WUMPUS = "¡Has sido cazado por el Wumpus! FIN DEL JUEGO"
    MSG_INFO_HUNTER_KILL_WUMPUS = "¡Has matado al Wumpus! ¡bien hecho!"
    MSG_INFO_HUNTER_FALLEN_INTO_WATER_WELL = "¡Has caido en un pozo! FIN DEL JUEGO"
    MSG_INFO_HUNTER_FOUND_GOLD = "¡Has encontrado el oro! vuelve a la casilla de salida"
    MSG_INFO_HUNTER_NO_ARROWS = "No te quedan flechas para lanzar"
    MSG_INFO_HUNTER_OUT_WIHTOUT_GOLD = "Todavia no has cogido el oro para poder escapar"
    MSG_INFO_HUNTER_OUT_WRONG_CELL = "No estaś en la casilla de salida para poder escapar"
    MSG_INFO_QUIT_GAME = "FIN. Gracias por jugar"
    MSG_INFO_WIN = "¡Has GANADO! FIN DEL JUEGO"
    MSG_INFO_WRONG_CHOICE = "Elección incorrecta"


class InfoException(Exception):
    pass
