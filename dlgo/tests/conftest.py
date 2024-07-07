import sys
print(sys.path)
import pytest
from dlgo.gamemodels.board.board_v1 import Board, GameState
from dlgo.gamemodels.board.board_zobrist import Board as zBoard, GameState as zGameState
from dlgo.gamemodels.player import Player

@pytest.fixture(scope="function", params=[
    {"size":9, "board": Board},
    {"size":19, "board": zBoard}
])
def new_board(request):
    board = Board(request.param["size"], request.param["size"])
    assert board.num_rows == request.param["size"]
    assert board.num_cols == request.param["size"]
    assert isinstance(board._grid, dict)
    return board

@pytest.fixture(scope="function", params=[
    {"size":19,"gamestate":zGameState},
    {"size":19,"gamestate":GameState}
    ])
def new_game(request):
    new_game = request.param["gamestate"].new_game(request.param["size"])
    assert len(new_game.board._grid)==0
    assert new_game.next_player is Player.BLACK
    assert new_game.previous_state is None
    assert new_game.last_move is None

    return new_game