from dlgo.agent.board_helpers import is_point_an_eye
from dlgo.gamemodels.point import Point
from dlgo.gamemodels.player import Player
from dlgo.agent.naive import RandomBot
import pytest


@pytest.mark.parametrize("bot_1, bot_2",[(RandomBot, RandomBot)] )
@pytest.mark.parametrize("move_count",[1, 3] )
def test_first_random_moves(new_game, move_count, bot_1, bot_2):
    current_game = new_game
    player_1 = bot_1()
    player_2 = bot_1()
    for round in range(1, move_count+1):
        player_1_move = player_1.select_move(current_game)
        current_game = current_game.apply_move(player_1_move)
        player_2_move = player_2.select_move(current_game)
        current_game = current_game.apply_move(player_2_move)

        assert len(current_game.board._grid.keys()) == round * 2