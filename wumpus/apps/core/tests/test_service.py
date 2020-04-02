import unittest
from unittest import mock
from unittest.mock import Mock
from wumpus.apps.common.util import Constants
from wumpus.apps.core.model import Hunter, Wumpus
from wumpus.apps.core.service import GameBoardService


class GameBoardServiceTest(unittest.TestCase):
    def setUp(self) -> None:
        # Input arguments to methods
        self.hunter = TestHelper.get_hunter()
        self.wumpus = TestHelper.get_wumpus()
        self.wumpus_dead = TestHelper.get_wumpus(dead=True)

    @mock.patch('wumpus.apps.core.service.PerceptionService.is_hunter_in_element_position')
    def test_is_hunter_hunted_by_wumpus_when_wumpus_is_dead(self, mocked_is_hunter_in_element_position_method: Mock) \
            -> None:

        # Unit test for the method: is_hunter_hunted_by_wumpus()

        # Mock methods called inside the method
        mocked_is_hunter_in_element_position_method.return_value = True

        # Asserts
        result = GameBoardService.is_hunter_hunted_by_wumpus(self.hunter, self.wumpus_dead)
        mocked_is_hunter_in_element_position_method.assert_not_called()
        self.assertEqual(False, result)

    @mock.patch('wumpus.apps.core.service.PerceptionService.is_hunter_in_element_position')
    def test_is_hunter_hunted_by_wumpus_when_they_both_same_position(
            self, mocked_is_hunter_in_element_position_method: Mock) -> None:

        # Unit test for the method: is_hunter_hunted_by_wumpus()

        # Mock methods called inside the method
        mocked_is_hunter_in_element_position_method.return_value = True

        # Asserts
        result = GameBoardService.is_hunter_hunted_by_wumpus(self.hunter, self.wumpus)
        mocked_is_hunter_in_element_position_method.assert_called_once()
        self.assertEqual(True, result)

    @mock.patch('wumpus.apps.core.service.PerceptionService.is_hunter_in_element_position')
    def test_is_hunter_hunted_by_wumpus_when_they_have_different_position(
            self, mocked_is_hunter_in_element_position_method: Mock) -> None:

        # Unit test for the method: is_hunter_hunted_by_wumpus()

        # Mock methods called inside the method
        mocked_is_hunter_in_element_position_method.return_value = False

        # Asserts
        result = GameBoardService.is_hunter_hunted_by_wumpus(self.hunter, self.wumpus)
        mocked_is_hunter_in_element_position_method.assert_called_once()
        self.assertEqual(False, result)

    # TODO: do more test...


class TestHelper(object):

    @staticmethod
    def get_hunter() -> Hunter:
        hunter: Hunter = Hunter()
        hunter.row = 5
        hunter.column = 5
        hunter.gold_caught = False
        hunter.is_dead = False
        hunter.n_arrows = 7
        hunter.direction = Constants.DIRECTION_RIGHT
        return hunter

    @staticmethod
    def get_wumpus(dead: bool = False) -> Wumpus:
        wumpus: Wumpus = Wumpus()
        wumpus.row = 5
        wumpus.column = 5
        wumpus.is_dead = dead
        return wumpus

