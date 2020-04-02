from abc import ABCMeta, abstractmethod
from typing import List, Tuple
from wumpus.apps.core.model import GameBoard, Hunter, Wumpus, BoardElement


class IGameBoard(metaclass=ABCMeta):
    @staticmethod
    @abstractmethod
    def load_game(game_board: GameBoard) -> None:
        """
        Load configuration and initialize initial values
        :param game_board: GameBoard object
        :return: None
        """

    @staticmethod
    @abstractmethod
    def show_game_board(game_board: GameBoard) -> None:
        """
        Print game board
        :param game_board: GameBoard object
        :return: None
        """

    @staticmethod
    @abstractmethod
    def manage_option(choice: int, game_board: GameBoard) -> (bool, str):
        """
        Process the option chosen by the user
        :param choice: user choice
        :param game_board: GameBoard object
        :return: tuple (quit game, message)
        """

    @staticmethod
    @abstractmethod
    def is_hunter_hunted_by_wumpus(hunter: Hunter, wumpus: Wumpus) -> bool:
        """
        Is hunter hunted by wumpus?
        :param hunter: Hunter object
        :param wumpus: Wumpus object
        :return: boolean answer to the question
        """

    @staticmethod
    @abstractmethod
    def has_hunter_fallen_into_water_well(hunter: Hunter, water_well_list: List[BoardElement]) -> bool:
        """
        Has hunter fallen into water well?
        :param hunter: Hunter object
        :param water_well_list: list of water wells
        :return: boolean answer to the question
        """

    @staticmethod
    @abstractmethod
    def has_hunter_found_the_gold(hunter: Hunter, gold: BoardElement) -> bool:
        """
        Has hunter found the gold?
        :param hunter: Hunter object
        :param gold: BoardElement object representing gold
        :return: boolean answer to the question
        """

    @staticmethod
    @abstractmethod
    def can_hunter_escape(hunter: Hunter, outlet: BoardElement) -> bool:
        """
        Can hunter escape?
        :param hunter: Hunter object
        :param outlet: BoardElement object representing outlet
        :return: boolean answer to the question
        """


class IPerception(metaclass=ABCMeta):
    @staticmethod
    @abstractmethod
    def is_there_wumpus_stench(hunter: BoardElement, wumpus: Wumpus) -> bool:
        """
        Is there wumpus stench?
        :param hunter: Hunter object
        :param wumpus: Wumpus object
        :return: boolean answer to the question
        """

    @staticmethod
    @abstractmethod
    def is_there_well_breeze(hunter: BoardElement, water_well_list: List[BoardElement]) -> bool:
        """
        Is there well breeze?
        :param hunter: Hunter object
        :param water_well_list: list of water wells
        :return: boolean answer to the question
        """

    @staticmethod
    @abstractmethod
    def is_there_gold_shine(hunter: Hunter, gold: BoardElement) -> bool:
        """
        Is there gold shine?
        :param hunter: Hunter object
        :param gold: BoardElement object representing gold
        :return: boolean answer to the question
        """

    @staticmethod
    @abstractmethod
    def is_there_shock(hunter: Hunter) -> bool:
        """
        Is there shock?
        :param hunter: Hunter object
        :return: boolean answer to the question
        """

    @staticmethod
    @abstractmethod
    def is_there_wumpus_scream(hunter: Hunter, wumpus: Wumpus) -> bool:
        """
        Is there wumpus scream?
        :param hunter: Hunter object
        :param wumpus: Wumpus object
        :return: boolean answer to the question
        """

    @staticmethod
    @abstractmethod
    def get_perceptions(game_board: GameBoard) -> List[str]:
        """
        Get all perceptions
        :param game_board: GameBoard object
        :return: list of perceptions represented by strings
        """


class IHunter(metaclass=ABCMeta):
    @staticmethod
    @abstractmethod
    def move(hunter: Hunter) -> None:
        """
        Move hunter
        :param hunter: Hunter object
        :return: None
        """

    @staticmethod
    @abstractmethod
    def rotate_90_degrees_left(hunter: Hunter) -> None:
        """
        Hunter rotate 90º left
        :param hunter: Hunter object
        :return: None
        """

    @staticmethod
    @abstractmethod
    def rotate_90_degrees_right(hunter: Hunter) -> None:
        """
        Hunter rotate 90º right
        :param hunter: Hunter object
        :return: None
        """

    @staticmethod
    @abstractmethod
    def throw_arrow(hunter: Hunter) -> None:
        """
        Hunter throw arrow
        :param hunter: Hunter object
        :return: None
        """

    @staticmethod
    @abstractmethod
    def is_hunter_in_element_position(hunter: Hunter, board_element: BoardElement) -> bool:
        """
        Is hunter in element position?
        :param hunter: Hunter object
        :param board_element: BoardElement object
        :return: boolean answer to the question
        """

    @staticmethod
    @abstractmethod
    def get_ascii_direction(hunter: Hunter) -> str:
        """
        Get ascii representation of hunter direction
        :param hunter: Hunter object
        :return: string representing an ascii character
        """


class IBoardElement(metaclass=ABCMeta):
    @staticmethod
    @abstractmethod
    def get_position_tuple(board_element: BoardElement) -> (int, int):
        """
        Get position of board element
        :param board_element: BoardElement object
        :return: tuple (raw, column)
        """

    @staticmethod
    @abstractmethod
    def get_position_tuple_list(board_element_list: List[BoardElement]) -> List[Tuple]:
        """
        Get positions list of board elements list
        :param board_element_list: list of BoardElement objects
        :return: list of positions represented by tuples
        """