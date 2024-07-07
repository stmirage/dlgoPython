from dlgo.gamemodels.board.board_v1 import Board, GameState
from dlgo.gamemodels.point import Point
from dlgo.gamemodels.player import Player
from dlgo.gamemodels.move import Move


import pytest


@pytest.mark.parametrize("board_size", [.1,"fff"])
@pytest.mark.xfail
def test_board_creation(board_size):
    board = Board(board_size,board_size)


def test_place_stone_on_new_game_state(new_game):
    game = new_game
    assert len(game.board._grid) == 0

    move = Move.play(Point(col=1, row=1))
    next_state = game.apply_move(move)

    assert len(next_state.board._grid) == 1

    
@pytest.mark.parametrize("is_pass_1_player, is_pass_2_player, expected_game_over", [
    (True, True, True),
    (False, True, False),
    (True, False, False),])
def test_finish_game_by_pass(new_game, is_pass_1_player, is_pass_2_player, expected_game_over):
    game = new_game
    move_1_player = Move.pass_turn() if is_pass_1_player else Move.play(Point(col=1, row=1))
    after_move_1 = game.apply_move(move_1_player)
    move_2_player = Move.pass_turn() if is_pass_2_player else Move.play(Point(col=2, row=1))
    after_move_2 = after_move_1.apply_move(move_2_player)
    assert after_move_2.is_over() == expected_game_over

@pytest.mark.parametrize("points_to_move, is_valid", [
    ([[1,2],[3,3],[2,1], [1,1]], False), # Самозахват
    ([[1,2],[3,3],[2,1], [4,4]], True)
    ])
def test_self_capture(new_game,points_to_move, is_valid):
    current_game = new_game
    for point in points_to_move[:-1]:
        move = Move.play(Point(row = point[0], col = point[1]))
        current_game = current_game.apply_move(move)
    last_point_coords = points_to_move[-1]
    last_point = Point(row = last_point_coords[0], col = last_point_coords[1])
    last_move = Move(point = last_point)

    assert current_game.is_valid_move(last_move) is is_valid

@pytest.mark.parametrize("points_to_move, is_valid", [
    ([[2,2],[3,2],[1,3], [2,3],[2,4], [3,4],[7,7], [4,3],[3,3], [2,3]], False), # Ко
    ([[2,2],[2,3],[3,1], [3,2],[4,2], [4,3],[7,7], [3,4],[3,3], [6,7]], True) # not Ко
    ])
def test_violate_ko(new_game,points_to_move, is_valid):
    current_game = new_game
    for point in points_to_move[:-1]:
        move = Move.play(Point(row = point[0], col = point[1]))
        current_game = current_game.apply_move(move)
    last_point_coords = points_to_move[-1]
    last_point = Point(row = last_point_coords[0], col = last_point_coords[1])
    last_move = Move(point = last_point)
    print(f"last move is {last_point_coords}")
    assert current_game.is_valid_move(last_move) is is_valid