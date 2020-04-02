from typing import List


class GameBoard:
    def __init__(self):
        self.size: int = 0
        self.water_well_list: List[BoardElement] = list()
        self.wumpus: Wumpus = Wumpus()
        self.hunter: Hunter = Hunter()
        self.gold: BoardElement = BoardElement()
        self.outlet: BoardElement = BoardElement()


class BoardElement:
    def __init__(self):
        self.row: int = 0
        self.column: int = 0


class Hunter(BoardElement):
    def __init__(self):
        super().__init__()
        self.n_arrows: int = 0
        self.direction: int = 0
        self.gold_caught: bool = False
        self.is_dead: bool = False


class Wumpus(BoardElement):
    def __init__(self):
        super().__init__()
        self.is_dead: bool = False
