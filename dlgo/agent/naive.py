import random
from dlgo.agent.base import Agent
from dlgo.agent.board_helpers import is_point_an_eye
from dlgo.gamemodels.move import Move
from dlgo.gamemodels.point import Point

class RandomBot(Agent):
    def select_move(self, gamestate):
        candidates = []
        for r in range(1, gamestate.board.num_rows + 1):
            for c in range(1, gamestate.board.num_cols + 1):
                candidate = Point(row=r, col=c)
                if gamestate.is_valid_move(Move.play(candidate)) and \
                    not is_point_an_eye(gamestate.board, candidate, gamestate.next_player):
                    candidates.append(candidate)
        if not candidates:
            return Move.pass_turn()
        return Move.play(random.choice(candidates))
    