from wumpus.apps.core.models import GameBoard
from wumpus.apps.core.services import GameBoardService
from wumpus.apps.common.util import InfoException, Constants


class App:
    def __init__(self):
        self.game_board: GameBoard = GameBoard()

    def __initialize(self):
        GameBoardService.load_board(self.game_board)

    def run_game(self):
        self.__initialize()
        quit_game = False
        while not quit_game:
            print("##########################################")
            print("               · wumpus ·                 ")
            print("##########################################")
            print("1. Avanzar")
            print("2. Girar 90º izquierda")
            print("3. Girar 90º derecha")
            print("4. Lanzar flecha")
            print("5. Escapar con el oro (si estas en la casilla de salida)")
            print("6. Quitar")
            print("7. Mostrar tablero (DEBUG)")
            print("------------------------------------------")
            print("Posicion actual del cazador: %s")
            print("Dirección actual del cazador: %s")
            print("Percepciones actuales: %s")
            choice = int(input("### Elige opción: "))
            if choice == Constants.OPTION_MENU_GO:
                pass
            elif choice == Constants.OPTION_MENU_ROTATE_90_DEGREES_LEFT:
                pass
            elif choice == Constants.OPTION_MENU_ROTATE_90_DEGREES_RIGHT:
                pass
            elif choice == Constants.OPTION_MENU_THROW_ARROW:
                pass
            elif choice == Constants.OPTION_MENU_OUT_WIN:
                pass
            elif choice == Constants.OPTION_MENU_QUIT_GAME:
                print("FIN. Gracias por jugar")
                quit_game = True
            elif choice == 7:
                GameBoardService.show_game_board(self.game_board)
            else:
                print("Elección incorrecta")


def second_menu():
    print("This is the second menu")


if __name__ == '__main__':
    app = App()
    app.run_game()
