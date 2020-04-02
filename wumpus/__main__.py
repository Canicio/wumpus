from wumpus.apps.core.model import GameBoard
from wumpus.apps.core.service import GameBoardService, HunterService, PerceptionService
from wumpus.apps.common.util import InfoException
import wumpus.config as config


class App:

    def __init__(self) -> None:
        self.game_board: GameBoard = GameBoard()

    def __initialize(self) -> None:
        GameBoardService.load_game(self.game_board)

    def run_game(self) -> None:
        try:
            self.__initialize()
            quit_game = False
            message = None
            while not quit_game:
                print("##########################################")
                print("               · wumpus ·                 ")
                print("##########################################")
                if not config.HIDE_BOARD:
                    GameBoardService.show_game_board(self.game_board)
                print("------------------------------------------")
                print("Opciones:")
                print("1. Avanzar")
                print("2. Girar 90º izquierda")
                print("3. Girar 90º derecha")
                print("4. Lanzar flecha")
                print("5. Escapar con el oro (si estas en la casilla de salida)")
                print("6. Quitar")
                print("------------------------------------------")
                print("Posicion actual del cazador: (%s, %s)" % (self.game_board.hunter.row,
                                                                 self.game_board.hunter.column))
                print("Dirección actual del cazador: %s" % HunterService.get_ascii_direction(self.game_board.hunter))
                print("Nº flechas del cazador: %s" % self.game_board.hunter.n_arrows)
                print("Percepciones actuales: %s" % str(PerceptionService.get_perceptions(self.game_board)))
                if message:
                    print("-->   %s   <--" % message)
                current_input = input("### Elige opción: ").strip()
                if current_input:
                    choice = int(current_input)
                else:
                    choice = 1
                quit_game, message = GameBoardService.manage_option(choice, self.game_board)
            if message:
                print("-->   %s   <--" % message)
        except InfoException as e:
            print("ERROR: %s" % str(e))


if __name__ == '__main__':
    app = App()
    app.run_game()
