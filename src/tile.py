from enum import Enum
from typing import TYPE_CHECKING

#used to avoid circular imports when type checking
if TYPE_CHECKING:
    from src.entity import Entity

class Tile(Enum):
    """Enum for supported tiles on the board"""
    def __init__(self, board_index: int, color: str) -> None:
        self.board_index: int = board_index
        self.color:str = color

    EMPTY = (0, 'darkslateblue')
    WALL = (1, 'forestgreen')
    ENEMY = (2, 'crimson')
    PLAYER = (3, 'royalblue')
    RESPAWN = (4, 'mediumaquamarine')
    BOOST = (5, 'goldenrod')

def is_empty_tile(tile: int) -> bool:
    return tile in {Tile.EMPTY.board_index, Tile.ENEMY.board_index, 
                    Tile.PLAYER.board_index, Tile.RESPAWN.board_index,
                    Tile.BOOST.board_index}

def is_paintable_tile(tile: int, entity: "Entity") -> bool:
    return tile in {Tile.EMPTY.board_index, entity.enemy_tile.board_index}

def is_boost_tile(tile: int) -> bool:
    return tile in {Tile.BOOST.board_index}