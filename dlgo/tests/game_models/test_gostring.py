from dlgo.gamemodels.player import Player
from dlgo.gamemodels.point import Point
from dlgo.gamemodels.move import Move
from dlgo.gamemodels.board.gostring import GoString 
from itertools import product
import pytest

TEST_DATA = [
    {
        "go_string_1":  GoString(
                        Player.BLACK, 
                        [Point(col=2, row=2)],
                        [Point(col=1, row=2), Point(col=3, row=2), Point(col=2, row=1), Point(col=2, row=3)]),
        "go_string_2":  GoString(
                        Player.BLACK, 
                        [Point(col=3, row=2)],
                        [Point(col=2, row=2), Point(col=4, row=2), Point(col=3, row=1), Point(col=3, row=3)]),
        "resulted_string": GoString(
                        Player.BLACK, 
                        [Point(col=3, row=2),   Point(col=2, row=2) ],
                        [Point(col=1, row=2),   Point(col=2, row=3), Point(col=2, row=1), 
                                                Point(col=3, row=3), Point(col=3, row=1),
                        Point(col=4, row=2)])
    }
]# Пока так, потом возможно генератор

@pytest.mark.parametrize("gostring_test_suite", TEST_DATA)
def test_gostring_merge(gostring_test_suite):

    result = gostring_test_suite["go_string_1"].merged_with(gostring_test_suite["go_string_2"])

    assert result == gostring_test_suite["resulted_string"]
    