from collections import namedtuple

class Point(namedtuple('Point', 'row col')):
    
    @property
    def neighbors(self):
        return [
            Point(self.row-1, self.col),
            Point(self.row+1, self.col),
            Point(self.row, self.col - 1),
            Point(self.row, self.col + 1),
        ]
    
    def __eq__(self, other):
        return isinstance(other, Point) and self.row == other.row and self.col == other.col

    def __deepcopy__(self, memodict={}):
        # These are very immutable.
        return self
    
    def __hash__(self):
       
        # hash(custom_object)
        return hash((self.row, self.col))