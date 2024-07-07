from __future__ import print_function

import os
import sys
path = os.path.join(os.path.dirname(__file__), os.pardir)
sys.path.append(path)


from agent.naive import RandomBot

from gamemodels.board.board_zobrist import GameState
from dlgo.gamemodels.player import Player
from dlgo.utils.utils import print_board, print_move
import time


def main():
    board_size = 9
    game = GameState.new_game(board_size)
    bots = {
        Player.BLACK: RandomBot(),
        Player.WHITE: RandomBot(),
    }
    while not game.is_over():
        time.sleep(0.3)

        print(chr(27) + "[2J") 
        print_board(game.board)
        for player in bots.values():
            print(player is game.next_player)
            
        bot = bots[game.next_player]
        bot_move = bot.select_move(game)
        print_move(game.next_player, bot_move)
        game = game.apply_move(bot_move)


if __name__ == '__main__':
    main()

# <1> We set a sleep timer to 0.3 seconds so that bot moves aren't printed too fast to observe
# <2> Before each move we clear the screen. This way the board is always printed to the same position on the command line.
# end::bot_vs_bot[]