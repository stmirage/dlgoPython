import enum

class Player(enum.Enum):
    BLACK = 1
    WHITE = 2

    @property
    def opposite_color(self):
        return Player.BLACK if self == Player.WHITE else Player.WHITE