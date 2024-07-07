from dlgo.gamemodels.player import Player
from dlgo.gamemodels.point import Point
from dlgo.gamemodels.move import Move
from itertools import product
import pytest

@pytest.mark.parametrize("player_color, opposite_color", [(Player.WHITE, Player.BLACK), (Player.BLACK, Player.WHITE)])
def test_player_other_property(player_color, opposite_color):
    player = Player(player_color)
    assert player.opposite_color == opposite_color

@pytest.mark.parametrize("x, y", [(0, 0), (5, 5), (19,19)])
def test_creating_point_positive(x,y):
    point = Point(x,y)
    neighbors = point.neighbors

    directions = [ 
        Point(row=x+1, col=y),
        Point(row=x+1, col=y),
        Point(row=x, col=y-1),
        Point(row=x, col=y-1)
        ]

    for direct in directions:
        assert direct in neighbors

@pytest.mark.parametrize("x, y", [(0, 0), (5, 5), (19,19)])
def test_move_play_created(x,y):
    point = Point(x,y)
    move = Move.play(point = point)
    assert move.is_resign == False
    assert move.is_pass == False
    assert move.point.col == x and move.point.row == y

@pytest.mark.parametrize("x, y", [(0, 0)])
def test_move_resign_created(x,y):
    point = Point(x,y)
    move = Move.resign()
    assert move.is_resign == True
    assert move.is_pass == False
    assert move.point == None

@pytest.mark.parametrize("x, y", [(0, 0)])
def test_move_pass_created(x,y):
    point = Point(x,y)
    move = Move.pass_turn()
    assert move.is_resign == False
    assert move.is_pass == True
    assert move.point == None