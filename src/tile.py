from enum import Enum
class Tile(Enum):
    def __init__(self, board_index: int, color: str) -> None:
        self.board_index: int = board_index
        self.color:str = color

    EMPTY = (0, 'darkslateblue')
    WALL = (1, 'forestgreen')
    ENEMY = (2, 'crimson')
    PLAYER = (3, 'royalblue')
    RESPAWN = (4, 'mediumaquamarine')
    BOOST = (5, 'goldenrod')