from random import randint
from typing import List, Set, Tuple
import wumpus.config as config
from wumpus.apps.core.models import BoardElement, GameBoard, Hunter
from wumpus.apps.common.util import InfoException, Constants


class GameBoardService:
    @classmethod
    def load_board(cls, game_board: GameBoard):
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
            draw_row = ''
            for column in range(game_board.size):
                if (row, column) in BoardElementService.get_posicion_tuple_list(game_board.water_well_list):
                    draw_row = draw_row + 'O '
                elif (row, column) == BoardElementService.get_posicion_tuple(game_board.wumpus):
                    draw_row = draw_row + 'W '
                elif (row, column) == BoardElementService.get_posicion_tuple(game_board.hunter):
                    if game_board.hunter.direction == Constants.DIRECTION_UP:
                        draw_row = draw_row + '%s ' % Constants.DRAW_ASCII_UP
                    elif game_board.hunter.direction == Constants.DIRECTION_DOWN:
                        draw_row = draw_row + '%s ' % Constants.DRAW_ASCII_DOWN
                    elif game_board.hunter.direction == Constants.DIRECTION_LEFT:
                        draw_row = draw_row + '%s ' % Constants.DRAW_ASCII_LEFT
                    elif game_board.hunter.direction == Constants.DIRECTION_RIGHT:
                        draw_row = draw_row + '%s ' % Constants.DRAW_ASCII_RIGHT
                elif (row, column) == BoardElementService.get_posicion_tuple(game_board.gold):
                    draw_row = draw_row + 'X '
                elif (row, column) == BoardElementService.get_posicion_tuple(game_board.outlet):
                    draw_row = draw_row + 'S '
                else:
                    draw_row = draw_row + '- '
            print(draw_row)


class PerceptionService:
    @classmethod
    def is_there_wumpus_stench(cls, hunter: BoardElement, wumpus: BoardElement) -> bool:
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
        return cls.__is_hunter_in_element_position(hunter, gold)

    @staticmethod
    def is_there_shock(hunter: Hunter) -> bool:
        shock = False
        if hunter.direction == Constants.DIRECTION_UP and hunter.row == 0:
            shock = True
        elif hunter.direction == Constants.DIRECTION_DOWN and hunter.row == config.N_BOARD_CELLS-1:
            shock = True
        elif hunter.direction == Constants.DIRECTION_LEFT and hunter.column == 0:
            shock = True
        elif hunter.direction == Constants.DIRECTION_RIGHT and hunter.row == config.N_BOARD_CELLS-1:
            shock = True
        return shock

    @staticmethod
    def is_there_wumpus_scream(hunter: Hunter, wumpus: BoardElement):
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

    @classmethod
    def is_wumpus(cls, hunter: Hunter, wumpus: BoardElement):
        return cls.__is_hunter_in_element_position(hunter, wumpus)

    @staticmethod
    def __is_hunter_adjacent_to_element(hunter: BoardElement, element: BoardElement) -> bool:
        element_row_adjacent = [element.row-1, element.row, element.row+1]
        element_column_adjacent = [element.column-1, element.column, element.column+1]
        if hunter.row in element_row_adjacent and hunter.column in element_column_adjacent:
            return True
        else:
            return False

    @staticmethod
    def __is_hunter_in_element_position(hunter: Hunter, board_element: BoardElement) -> bool:
        if board_element.row == hunter.row and board_element.column == hunter.column:
            return True
        else:
            return False


class HunterService:

    @classmethod
    def move(cls, hunter: Hunter):
        perception_list: List[int] = list()
        # if PerceptionService.is_there_shock(hunter):
        #     perception_list.append(Constants.PERCEPTION_SHOCK)
        # else:
        #     # increment position
        #     pass
        # # TODO: if ...
        cls.__forward_position(hunter)
        # if PerceptionService.is_there_shock(hunter):
        #     perception_list.append(Constants.PERCEPTION_SHOCK)
        # if PerceptionService.is_there_gold_shine(hunter)

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
            hunter.n_arrows -= hunter.n_arrows

    @staticmethod
    def __forward_position(hunter: Hunter):
        if hunter.direction == Constants.DIRECTION_UP:
            if hunter.row > 0:
                hunter.row -= hunter.row
        elif hunter.direction == Constants.DIRECTION_DOWN:
            if hunter.row < config.N_BOARD_CELLS-1:
                hunter.row += hunter.row
        elif hunter.direction == Constants.DIRECTION_LEFT:
            if hunter.column > 0:
                hunter.column -= hunter.column
        elif hunter.direction == Constants.DIRECTION_RIGHT and hunter.row == config.N_BOARD_CELLS-1:
            if hunter.column < config.N_BOARD_CELLS-1:
                hunter.column -= hunter.column

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