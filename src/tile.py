from enum import Enum
class Tile(Enum):
    def __init__(self, board_index, color):
        self.board_index = board_index
        self.color = color

    EMPTY = (0, 'purple')
    WALL = (1, 'green')
    ENEMY = (2, 'red')
    PLAYER = (3, 'blue')