import random
from typing import TYPE_CHECKING
from src.tile import Tile

if TYPE_CHECKING:
    from src.entity import Entity

def is_empty_tile(tile: int) -> bool:
    return tile in {Tile.EMPTY.board_index, Tile.ENEMY.board_index, 
                    Tile.PLAYER.board_index, Tile.RESPAWN.board_index,
                    Tile.BOOST.board_index}

def is_paintable_tile(tile: int, entity: "Entity") -> bool:
    return tile in {Tile.EMPTY.board_index, entity.enemy_tile.board_index}

def is_boost_tile(tile: int) -> bool:
    return tile in {Tile.BOOST.board_index}

def get_surrounding_tiles(board: list[list[int]], entity: "Entity", center_x: int, center_y: int) -> list[tuple[Tile, int]]:
    fudge = entity.square_size - (entity.square_size // 10)
    rows = len(board)
    cols = len(board[0])

    directions = [
        (entity.Direction.RIGHT, fudge, 0),
        (entity.Direction.LEFT, -fudge, 0),
        (entity.Direction.UP, 0, -fudge),
        (entity.Direction.DOWN, 0, fudge),
    ]
    
    def in_bounds(x: int, y:int ) -> bool:
        return 0 <= x < cols and 0 <= y < rows

    result = []
    for direction, offset_x, offset_y in directions:
        tile_x = (center_x + offset_x) // entity.square_size
        tile_y = (center_y + offset_y) // entity.square_size
        
        if in_bounds(tile_x, tile_y):
            current_tile = board[tile_y][tile_x]
            result.append((direction, current_tile))
    
    return result

def get_tile_coordinates(board: list[list[int]], tile_type: int, square_size: int) -> list[tuple[int, int]]:
    coordinates = []
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == tile_type:
                coordinates.append((col * square_size, row * square_size))
    return coordinates

def get_random_tile_coordinate(board, tile_type: int, square_size: int) -> tuple[int, int]:
    coordinates = get_tile_coordinates(board, tile_type, square_size)
    if not coordinates:
        raise ValueError("Could not get coordinates of given tile type.")
    return random.choice(coordinates)