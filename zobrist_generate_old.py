# tag::generate_zobrist[]
import random

from dlgo.gamemodels.player import Player
from dlgo.gamemodels.point import Point


def to_python(player_state):
    if player_state is None:
        return 'None'
    if player_state == Player.BLACK:
        return Player.BLACK
    return Player.WHITE


MAX63 = 0x7fffffffffffffff

table = {}
empty_board = 0
for row in range(1, 20):
    for col in range(1, 20):
        for state in (Player.BLACK, Player.WHITE):
            code = random.randint(0, MAX63)
            table[Point(row, col), state] = code

print('from dlgo.gamemodels.player import Player')
print('from dlgo.gamemodels.point import Point')
print('')
print("__all__ = ['HASH_CODE', 'EMPTY_BOARD']")
print('')
print('HASH_CODE = {')
for (pt, state), hash_code in table.items():
    print('    (%r, %s): %r,' % (pt, to_python(state), hash_code))
print('}')
print('')
print('EMPTY_BOARD = %d' % (empty_board,))
# end::generate_zobrist[]