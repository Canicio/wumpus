from random import randint
from typing import List, Set, Tuple
import wumpus.config as config
from wumpus.apps.core.models import BoardElement, GameBoard, Hunter, Wumpus
from wumpus.apps.common.util import InfoException, Constants


class GameBoardService:
    @classmethod
    def load_game(cls, game_board: GameBoard):
        game_board.size = config.N_BOARD_CELLS
        positions_occupied: Set[Tuple] = set()
        # outlet
        game_board.outlet.row = game_board.size-1
        game_board.outlet.column = 0
        positions_occupied.add((game_board.outlet.row, game_board.outlet.column))
        # load hunter
        game_board.hunter.row = game_board.outlet.row
        game_board.hunter.column = game_board.outlet.column
        game_board.hunter.direction = Constants.DIRECTION_RIGHT
        game_board.hunter.n_arrows = config.N_ARROWS
        positions_occupied.add((game_board.hunter.row, game_board.hunter.column))
        # load water wells
        game_board.water_well_list = cls.__load_water_wells(positions_occupied)
        # load wumpus
        game_board.wumpus.row, game_board.wumpus.column = cls.__load_random_position(positions_occupied)
        # load gold
        game_board.gold.row, game_board.gold.column = cls.__load_random_position(positions_occupied)

    @staticmethod
    def __load_random_position(positions_occupied: Set[Tuple]) -> Tuple:
        position = None
        attempts = 0
        while attempts < 5 and not position:
            position = (randint(0, config.N_BOARD_CELLS - 1), randint(0, config.N_BOARD_CELLS - 1))
            if position in positions_occupied:
                position = None
                attempts += 1
        if position:
            positions_occupied.add(position)
        else:
            raise InfoException(Constants.MSG_EXCEPTION_LOAD_BOARD_ELEMENT)
        return position

    @classmethod
    def __load_water_wells(cls, positions_occupied: Set[Tuple]) -> List[BoardElement]:
        water_well_list: List[BoardElement] = list()
        for _ in range(config.N_WATER_WELL):
            water_well = BoardElement()
            water_well.row, water_well.column = cls.__load_random_position(positions_occupied)
            water_well_list.append(water_well)
        return water_well_list

    @classmethod
    def show_game_board(cls, game_board: GameBoard):
        for row in range(game_board.size):
            draw_row = '   '
            for column in range(game_board.size):
                if (row, column) in BoardElementService.get_posicion_tuple_list(game_board.water_well_list):
                    draw_row = draw_row + 'O '
                elif not game_board.wumpus.is_dead and (row, column) == BoardElementService.get_posicion_tuple(
                        game_board.wumpus):
                    draw_row = draw_row + 'W '
                elif not game_board.hunter.is_dead and (row, column) == BoardElementService.get_posicion_tuple(
                        game_board.hunter):
                    ascii_direction = HunterService.get_ascii_direction(game_board.hunter)
                    draw_row = draw_row + '%s ' % ascii_direction
                elif not game_board.hunter.gold_caught and (row, column) == BoardElementService.get_posicion_tuple(
                        game_board.gold):
                    draw_row = draw_row + 'X '
                elif (row, column) == BoardElementService.get_posicion_tuple(game_board.outlet):
                    draw_row = draw_row + 'S '
                else:
                    draw_row = draw_row + '- '
            print(draw_row)

    @classmethod
    def manage_option(cls, choice: int, game_board: GameBoard) -> (bool, str):
        quit_game = False
        message = None
        if choice == Constants.OPTION_MENU_GO:
            HunterService.move(game_board.hunter)
            if GameBoardService.is_hunter_hunted_by_wumpus(game_board.hunter, game_board.wumpus):
                message = Constants.MSG_INFO_HUNTER_HUNTED_BY_WUMPUS
                quit_game = True
                game_board.hunter.is_dead = True
            if GameBoardService.has_hunter_fallen_into_water_well(game_board.hunter,
                                                                  game_board.water_well_list):
                message = Constants.MSG_INFO_HUNTER_FALLEN_INTO_WATER_WELL
                quit_game = True
            if not quit_game:
                if GameBoardService.has_hunter_found_the_gold(game_board.hunter,
                                                              game_board.gold):
                    message = Constants.MSG_INFO_HUNTER_FOUND_GOLD
                    game_board.hunter.gold_caught = True
        elif choice == Constants.OPTION_MENU_ROTATE_90_DEGREES_LEFT:
            HunterService.rotate_90_degrees_left(game_board.hunter)
        elif choice == Constants.OPTION_MENU_ROTATE_90_DEGREES_RIGHT:
            HunterService.rotate_90_degrees_right(game_board.hunter)
        elif choice == Constants.OPTION_MENU_THROW_ARROW:
            if game_board.hunter.n_arrows > 0:
                HunterService.throw_arrow(game_board.hunter)
                if not game_board.wumpus.is_dead:
                    if PerceptionService.is_there_wumpus_scream(game_board.hunter, game_board.wumpus):
                        message = Constants.MSG_INFO_HUNTER_KILL_WUMPUS
                        game_board.wumpus.is_dead = True
            else:
                message = Constants.MSG_INFO_HUNTER_NO_ARROWS
        elif choice == Constants.OPTION_MENU_OUT_WIN:
            if game_board.hunter.gold_caught:
                if GameBoardService.can_hunter_escape(game_board.hunter, game_board.outlet):
                    message = Constants.MSG_INFO_WIN
                    quit_game = True
                else:
                    message = Constants.MSG_INFO_HUNTER_OUT_WRONG_CELL
            else:
                message = Constants.MSG_INFO_HUNTER_OUT_WIHTOUT_GOLD
        elif choice == Constants.OPTION_MENU_QUIT_GAME:
            message = Constants.MSG_INFO_QUIT_GAME
            quit_game = True
        else:
            message = Constants.MSG_INFO_WRONG_CHOICE
        return quit_game, message

    @classmethod
    def is_hunter_hunted_by_wumpus(cls, hunter: Hunter, wumpus: Wumpus):
        if wumpus.is_dead:
            return False
        else:
            return PerceptionService.is_hunter_in_element_position(hunter, wumpus)

    @classmethod
    def has_hunter_fallen_into_water_well(cls, hunter: Hunter, water_well_list: List[BoardElement]):
        fallen = False
        for water_well in water_well_list:
            if PerceptionService.is_hunter_in_element_position(hunter, water_well):
                fallen = True
                break
        return fallen

    @classmethod
    def has_hunter_found_the_gold(cls, hunter: Hunter, gold: BoardElement):
        return PerceptionService.is_hunter_in_element_position(hunter, gold)

    @classmethod
    def can_hunter_escape(cls, hunter: Hunter, outlet: BoardElement):
        if hunter.gold_caught:
            return PerceptionService.is_hunter_in_element_position(hunter, outlet)
        else:
            return False


class PerceptionService:
    @classmethod
    def is_there_wumpus_stench(cls, hunter: BoardElement, wumpus: Wumpus) -> bool:
        return cls.__is_hunter_adjacent_to_element(hunter, wumpus)

    @classmethod
    def is_there_well_breeze(cls, hunter: BoardElement, water_well_list: List[BoardElement]) -> bool:
        breeze = False
        for water_well in water_well_list:
            if cls.__is_hunter_adjacent_to_element(hunter, water_well):
                breeze = True
                break
        return breeze

    @classmethod
    def is_there_gold_shine(cls, hunter: Hunter, gold: BoardElement) -> bool:
        gold_shine = False
        if hunter.direction == Constants.DIRECTION_UP:
            if gold.column == hunter.column and hunter.row == gold.row + 1:
                gold_shine = True
        elif hunter.direction == Constants.DIRECTION_DOWN:
            if gold.column == hunter.column and hunter.row == gold.row - 1:
                gold_shine = True
        elif hunter.direction == Constants.DIRECTION_LEFT:
            if gold.row == hunter.row and hunter.column == gold.column + 1:
                gold_shine = True
        elif hunter.direction == Constants.DIRECTION_RIGHT:
            if gold.row == hunter.row and hunter.column == gold.column - 1:
                gold_shine = True
        return gold_shine

    @staticmethod
    def is_there_shock(hunter: Hunter) -> bool:
        shock = False
        if hunter.direction == Constants.DIRECTION_UP and hunter.row == 0:
            shock = True
        elif hunter.direction == Constants.DIRECTION_DOWN and hunter.row == config.N_BOARD_CELLS-1:
            shock = True
        elif hunter.direction == Constants.DIRECTION_LEFT and hunter.column == 0:
            shock = True
        elif hunter.direction == Constants.DIRECTION_RIGHT and hunter.column == config.N_BOARD_CELLS-1:
            shock = True
        return shock

    @staticmethod
    def is_there_wumpus_scream(hunter: Hunter, wumpus: Wumpus):
        wumpus_scream = False
        if hunter.direction == Constants.DIRECTION_UP:
            if wumpus.column == hunter.column and hunter.row > wumpus.row:
                wumpus_scream = True
        elif hunter.direction == Constants.DIRECTION_DOWN:
            if wumpus.column == hunter.column and hunter.row < wumpus.row:
                wumpus_scream = True
        elif hunter.direction == Constants.DIRECTION_LEFT:
            if wumpus.row == hunter.row and hunter.column > wumpus.column:
                wumpus_scream = True
        elif hunter.direction == Constants.DIRECTION_RIGHT and hunter.row == config.N_BOARD_CELLS-1:
            if wumpus.row == hunter.row and hunter.column < wumpus.column:
                wumpus_scream = True
        return wumpus_scream

    @staticmethod
    def __is_hunter_adjacent_to_element(hunter: BoardElement, element: BoardElement) -> bool:
        element_row_adjacent = [element.row-1, element.row, element.row+1]
        element_column_adjacent = [element.column-1, element.column, element.column+1]
        if hunter.row in element_row_adjacent and hunter.column in element_column_adjacent:
            return True
        else:
            return False

    @staticmethod
    def is_hunter_in_element_position(hunter: Hunter, board_element: BoardElement) -> bool:
        if board_element.row == hunter.row and board_element.column == hunter.column:
            return True
        else:
            return False

    @classmethod
    def get_perceptions(cls, game_board: GameBoard):
        perception_list: List[str] = list()
        if not game_board.wumpus.is_dead and cls.is_there_wumpus_stench(game_board.hunter, game_board.wumpus):
            perception_list.append(Constants.PERCEPTION_WUMPUS_STENCH)
        if cls.is_there_well_breeze(game_board.hunter, game_board.water_well_list):
            perception_list.append(Constants.PERCEPTION_WATER_WELL_BREEZE)
        if not game_board.hunter.gold_caught and cls.is_there_gold_shine(game_board.hunter, game_board.gold):
            perception_list.append(Constants.PERCEPTION_GOLD_SHINE)
        if cls.is_there_shock(game_board.hunter):
            perception_list.append(Constants.PERCEPTION_SHOCK)
        return perception_list


class HunterService:

    @classmethod
    def move(cls, hunter: Hunter):
        if hunter.direction == Constants.DIRECTION_UP:
            if hunter.row > 0:
                hunter.row -= 1
        elif hunter.direction == Constants.DIRECTION_DOWN:
            if hunter.row < config.N_BOARD_CELLS-1:
                hunter.row += 1
        elif hunter.direction == Constants.DIRECTION_LEFT:
            if hunter.column > 0:
                hunter.column -= 1
        elif hunter.direction == Constants.DIRECTION_RIGHT:
            if hunter.column < config.N_BOARD_CELLS-1:
                hunter.column += 1

    @staticmethod
    def rotate_90_degrees_left(hunter: Hunter):
        if hunter.direction == Constants.DIRECTION_UP:
            hunter.direction = Constants.DIRECTION_LEFT
        elif hunter.direction == Constants.DIRECTION_DOWN:
            hunter.direction = Constants.DIRECTION_RIGHT
        elif hunter.direction == Constants.DIRECTION_LEFT:
            hunter.direction = Constants.DIRECTION_DOWN
        elif hunter.direction == Constants.DIRECTION_RIGHT:
            hunter.direction = Constants.DIRECTION_UP

    @staticmethod
    def rotate_90_degrees_right(hunter: Hunter):
        if hunter.direction == Constants.DIRECTION_UP:
            hunter.direction = Constants.DIRECTION_RIGHT
        elif hunter.direction == Constants.DIRECTION_DOWN:
            hunter.direction = Constants.DIRECTION_LEFT
        elif hunter.direction == Constants.DIRECTION_LEFT:
            hunter.direction = Constants.DIRECTION_UP
        elif hunter.direction == Constants.DIRECTION_RIGHT:
            hunter.direction = Constants.DIRECTION_DOWN

    @staticmethod
    def throw_arrow(hunter: Hunter):
        if hunter.n_arrows > 0:
            hunter.n_arrows -= 1

    @staticmethod
    def get_ascii_direction(hunter: Hunter):
        if hunter.direction == Constants.DIRECTION_UP:
            return Constants.DRAW_ASCII_UP
        elif hunter.direction == Constants.DIRECTION_DOWN:
            return Constants.DRAW_ASCII_DOWN
        elif hunter.direction == Constants.DIRECTION_LEFT:
            return Constants.DRAW_ASCII_LEFT
        elif hunter.direction == Constants.DIRECTION_RIGHT:
            return Constants.DRAW_ASCII_RIGHT


class BoardElementService:
    @staticmethod
    def get_posicion_tuple(board_element: BoardElement) -> Tuple:
        return board_element.row, board_element.column

    @classmethod
    def get_posicion_tuple_list(cls, board_element_list: List[BoardElement]) -> List[Tuple]:
        tuple_list: List[Tuple] = list()
        for board_element in board_element_list:
            tuple_list.append(cls.get_posicion_tuple(board_element))
        return tuple_list
