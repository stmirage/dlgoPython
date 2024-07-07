from dlgo.gamemodels.board.board_v1 import Board
from dlgo.gamemodels.point import Point
from dlgo.gamemodels.player import Player
import pytest

def count_groups(board: Board):
    groups = list(board._grid.values())
    return len([e for e in groups if groups.count(e) == 1]) # Ищем уникальные группы


@pytest.mark.parametrize("stone_coords", [ 
    {"row":1, "col":1, "expected_liberties" : 2},
    {"row":2, "col":1, "expected_liberties" : 3},
    {"row":2, "col":2, "expected_liberties" : 4},
    ])
def test_place_1_stone(new_board, stone_coords):
    point = Point(col=stone_coords["col"], row=stone_coords["row"])
    new_board.place_stone(Player.BLACK, point)
    assert len(new_board._grid) == 1
    single_string = new_board._grid.get(point)
    assert len(single_string.liberties) == stone_coords["expected_liberties"]
    assert len(single_string.stones) == 1

@pytest.mark.parametrize("color_for_eat", [Player.BLACK,Player.WHITE])
@pytest.mark.parametrize("stones", [ 
    {  "stones_to_eaten": 
        [{"row":1, "col":1}],
        "stones_attack": 
        [{"row":2, "col":1}, {"row":1, "col":2}]
    }
    ])
def test_eat_stone(new_board, color_for_eat,stones):
    attack_color = color_for_eat.opposite_color
    assert count_groups(new_board)==0

    for stone in stones["stones_to_eaten"]:
        point = Point(col=stone["col"], row=stone["row"])
        new_board.place_stone(color_for_eat, point)
    assert count_groups(new_board)==1

    for stone in stones["stones_attack"]:
        point = Point(col=stone["col"], row=stone["row"])
        new_board.place_stone(attack_color, point)
    count_groups(new_board)==1
