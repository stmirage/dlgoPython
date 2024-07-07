from dlgo.agent.board_helpers import is_point_an_eye
from dlgo.gamemodels.point import Point
from dlgo.gamemodels.player import Player
import pytest

@pytest.mark.parametrize("player", [Player.WHITE, Player.BLACK])
@pytest.mark.parametrize("coords_for_place, points_for_check", [
    (
        [[2,1], [1,2], [2,2]], {(1,1):True, (3,3):False, (2,2): False} # Угол
    ),
    (   [[2,1], [1,2]], {(1,1):False}),
    (
        [[2,1], [1,2], [2,2],[2,3],[2,4],[1,4]], {(1,1):True, (1,3):True} # Сторона
    ),
    (
        [[1,2], [2,2],[2,3],[1,4]], {(1,3):False}
    ),
    (
        [[2,2], [3,2], [4,2], [2,3], [4,3], [2,4], [3,4]], {(3,3):True} # Центр
    ),
])
def test_is_an_eye_helper(new_board, coords_for_place, points_for_check, player):
    current_board = new_board
    for coord in coords_for_place:
        current_board.place_stone(player, Point(row=coord[0], col=coord[1]))

    for eye_point, is_eye in points_for_check.items():
        assert is_point_an_eye(current_board, Point(row=eye_point[0], col=eye_point[1]), player) == is_eye
        #assert not is_point_an_eye(current_board, Point(row=eye_point[0], col=eye_point[1]), player.opposite_color)