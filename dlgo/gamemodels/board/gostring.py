from dlgo.gamemodels.point import Point
from typing import Self

class GoString():

    def __init__(self, color, stones, liberties):
        self.color = color
        self.stones = set(stones)
        self.liberties = set(liberties)

    def remove_liberty(self, point: Point):
        self.liberties.remove(point)
    
    def add_liberty(self, point: Point):
        self.liberties.add(point)

    def merged_with(self, gostring : Self):
        assert gostring.color == self.color
        combined_stones = self.stones | gostring.stones
        combined_liberties = (self.liberties | gostring.liberties) - combined_stones
        return GoString(self.color, combined_stones, combined_liberties)

    @property
    def num_liberties(self):
        return len(self.liberties)

    def __eq__(self, other):
        return isinstance(other, GoString) and \
        self.color == other.color and \
        self.stones == other.stones and \
        self.liberties == other.liberties
