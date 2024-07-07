from typing import TypedDict
from dlgo.gamemodels.point import Point
from dlgo.gamemodels.player import Player
from dlgo.gamemodels.board.gostring_frozen import GoString
from dlgo.zobrist import *
import copy

class Board():
    def __init__(self, num_rows, num_cols):
        self.num_rows = num_rows
        self.num_cols = num_cols
        self._grid: dict[Point, GoString] = {}
        self._hash = EMPTY_BOARD

    def place_stone(self, player: Player, point: Point): # Документирую изыбточно каждую строку, потому что это одно из самых сложных мест кода
        assert self.is_on_grid(point) # Проверяем, что ход, вообще, влазит на карту
        assert self._grid.get(point) is None # Проверяем, что поле пустое
        adjacement_same_color = [] # Примыкающие камни того же цвета
        adjacement_opposite_color = [] # Примыкающие камни другого цвета
        liberties = [] # Свободные пункты
        for neighbor in point.neighbors: # Идем по всем соседним точкам после установки камня
            if not self.is_on_grid(neighbor): # Если соседняя точка за пределами доски - ничего не делаем
                continue
            neighbor_string = self._grid.get(neighbor) # проверяем принадлежность камня к группе
            if neighbor_string is None: # если нет группы, прибавим камню 1 степень свободы
                liberties.append(neighbor)
            elif neighbor_string.color == player: # если там свой цвет - присоединим группу в список тех, которые есть в группах своих цветов
                if neighbor_string not in adjacement_same_color:
                    adjacement_same_color.append(neighbor_string)
            else:# если там чужой цвет - присоединим группу в список тех, которые есть в группах своих цветов
                if neighbor_string not in adjacement_opposite_color: 
                    adjacement_opposite_color.append(neighbor_string)
        new_string = GoString(player, [point], liberties)

        new_string = GoString(player, [point], liberties)  # <1>

        for same_color_string in adjacement_same_color:  # <2>
            new_string = new_string.merged_with(same_color_string)
        for new_string_point in new_string.stones:
            self._grid[new_string_point] = new_string

        self._hash ^= HASH_CODE[point, player]  # <3>

        for other_color_string in adjacement_opposite_color:
            replacement = other_color_string.without_liberties(point)  # <4>
            if replacement.num_liberties:
                self._replace_string(other_color_string.without_liberties(point))
            else:
                self._remove_string(other_color_string)  # <5>
        
        
    
    def is_on_grid(self, point):
        return 1 <= point.row <= self.num_rows and \
            1 <= point.col <= self.num_cols

    def get(self, point):
        string = self._grid.get(point)
        if string is None:
            return None
        return string.color

    def get_go_string(self, point):
        string = self._grid.get(point)
        if string is None:
            return None
        return string

    def _replace_string(self, new_string):  # <1>
        for point in new_string.stones:
            self._grid[point] = new_string
        
    def _remove_string(self, string):
        for point in string.stones:
            for neighbor in point.neighbors:  # <2>
                neighbor_string = self._grid.get(neighbor)
                if neighbor_string is None:
                    continue
                if neighbor_string is not string:
                    self._replace_string(neighbor_string.without_liberties(point))
            self._grid[point] = None

            self._hash ^= HASH_CODE[point, string.color]  # <3>
        
    def __eq__(self, other):
        asserts_general = isinstance(other, Board) and \
            (self.num_rows == other.num_rows) and \
            (self.num_cols == other.num_cols)
        temp_grid_1 = {k:v for k,v in self._grid.items() if v is not None}
        temp_grid_2 = {k:v for k,v in other._grid.items() if v is not None}
        asserts_grid = temp_grid_1 == temp_grid_2
        #asserts_grid = self._grid == other._grid
        return asserts_general and asserts_grid

    def __deepcopy__(self, memodict={}):
        copied = Board(self.num_rows, self.num_cols)
        # Can do a shallow copy b/c the dictionary maps tuples
        # (immutable) to GoStrings (also immutable)
        copied._grid = copy.copy(self._grid)
        copied._hash = self._hash
        return copied      
      
    def zobrist_hash(self):
        return self._hash
    
class GameState():

    def __init__(self, board, next_player, previous, move):
        self.board = board
        self.next_player = next_player
        self.previous_state = previous
        if self.previous_state is None:
            self.previous_states = frozenset()
        else:
            self.previous_states = frozenset(
                previous.previous_states |
                {(previous.next_player, previous.board.zobrist_hash())})
        self.last_move = move
    
    def apply_move(self, move):

        if move.is_play:
            next_board = copy.deepcopy(self.board)
            next_board.place_stone(self.next_player, move.point)
        else:
            next_board = self.board
        return GameState(next_board, self.next_player.opposite_color, self, move)
    
    def is_over(self):
        if self.last_move is None:
            return False
        if self.last_move.is_resign:
            return True
        second_last_move = self.previous_state.last_move
        if second_last_move is None:
            return False
        return self.last_move.is_pass and second_last_move.is_pass

    @classmethod
    def new_game(cls, board_size: int):
        if isinstance(board_size, int):
            board_size = (board_size, board_size)
        else:
            raise AssertionError("Board size cannot be non integer")
        board = Board(*board_size)
        return GameState(board, Player.BLACK, None, None)
    
    def is_move_self_capture(self, player, move):
        if not move.is_play:
            return False
        next_board = copy.deepcopy(self.board)
        next_board.place_stone(player, move.point)
        new_string = next_board.get_go_string(move.point)
        return new_string.num_liberties == 0
    
    @property
    def situation(self):
        return (self.next_player, self.board)
    
    def does_move_violate_ko(self, player, move):
        if not move.is_play:
            return False
        next_board = copy.deepcopy(self.board)
        next_board.place_stone(player, move.point)
        next_situation = (player.opposite_color, next_board.zobrist_hash())
        return next_situation in self.previous_states

    def is_valid_move(self, move):
        if self.is_over():
            return False
        if move.is_pass or move.is_resign:
            return True
        return (
            self.board.get(move.point) is None and
            not self.is_move_self_capture(self.next_player, move) and
            not self.does_move_violate_ko(self.next_player, move)
        )
    
    