from typing import TypedDict
from dlgo.gamemodels.point import Point
from dlgo.gamemodels.player import Player
from dlgo.gamemodels.board.gostring import GoString
import copy

class Board():
    def __init__(self, num_rows, num_cols):
        self.num_rows = num_rows
        self.num_cols = num_cols
        self._grid: dict[Point, GoString] = {}

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

        for same_color_string in adjacement_same_color:
            new_string = new_string.merged_with(same_color_string) # соединяем группы в одну строку
        for new_string_point in new_string.stones: # Обновляем принадлежность всех камней к группе
            self._grid[new_string_point] = new_string
        for other_color_string in adjacement_opposite_color:
            other_color_string.remove_liberty(point)
        for other_color_string in adjacement_opposite_color:
            if other_color_string.num_liberties == 0:
                self._remove_string(other_color_string)
        
        
    
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
    
    def _remove_string(self, string):
        for point in string.stones:
            for neigbor in point.neighbors:
                neighbor_string = self._grid.get(neigbor)
                if neighbor_string is None:
                    continue
                if neighbor_string is not string: # себе не добавляем свобод
                    neighbor_string.add_liberty(point)
            self._grid[point] = None
        
    def __eq__(self, other):
        asserts_general = isinstance(other, Board) and \
            (self.num_rows == other.num_rows) and \
            (self.num_cols == other.num_cols)
        temp_grid_1 = {k:v for k,v in self._grid.items() if v is not None}
        temp_grid_2 = {k:v for k,v in other._grid.items() if v is not None}
        asserts_grid = temp_grid_1 == temp_grid_2
        #asserts_grid = self._grid == other._grid
        return asserts_general and asserts_grid
"""         print("self_grid")
        for point, go_string in self._grid.items():
            color = None if go_string is None else go_string.color
            print(f"p:{point.col} {point.row} {color}")
        print("other grid")
        for point, go_string in other._grid.items():
            color = None if go_string is None else go_string.color
            print(f"p:{point.col} {point.row} {color}") """
        

class GameState():

    def __init__(self, board, next_player: Player, previous, move):
        self.board = board
        self.next_player = next_player
        self.previous_state = previous
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
        next_situation = (player.opposite_color, next_board)
        past_state = self.previous_state
        #print(f"check ko {move.point}")
        #print(f"current board {next_situation[0]}")
        #print(f"current board {next_situation[1]._grid.keys()}")
        #print(f"current board {next_situation[1]._grid.values()}")
        while past_state is not None:
            #print(past_state.situation[0])
            #print(past_state.situation[1]._grid.keys())
            #print(past_state.situation[1]._grid.values())
            if past_state.situation == next_situation:
                #print("ko!")
                return True
            past_state = past_state.previous_state
            #print("not ko!")
        return False

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