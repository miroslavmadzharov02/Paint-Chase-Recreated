import random
from src.tile import Tile

def is_empty_tile(tile):
        return tile in {Tile.EMPTY.board_index, Tile.ENEMY.board_index, 
                        Tile.PLAYER.board_index, Tile.RESPAWN.board_index,
                        Tile.BOOST.board_index}

def is_paintable_tile(tile, entity):
        return tile in {Tile.EMPTY.board_index, entity.enemy_tile.board_index}

def is_boost_tile(tile):
        return tile in {Tile.BOOST.board_index}

def get_surrounding_tiles(board, entity, center_x, center_y):
    fudge = entity.square_size - (entity.square_size // 10)
    rows = len(board)
    cols = len(board[0])

    directions = [
        (entity.Direction.RIGHT, fudge, 0),
        (entity.Direction.LEFT, -fudge, 0),
        (entity.Direction.UP, 0, -fudge),
        (entity.Direction.DOWN, 0, fudge),
    ]
    
    def in_bounds(x, y):
            return 0 <= x < cols and 0 <= y < rows

    result = []
    for direction, offset_x, offset_y in directions:
        tile_x = (center_x + offset_x) // entity.square_size
        tile_y = (center_y + offset_y) // entity.square_size
        
        if in_bounds(tile_x, tile_y):
            current_tile = board[tile_y][tile_x]
            result.append((direction, current_tile))
    
    return result

def get_tile_coordinates(board, tile_type, square_size):
        coordinates = []
        for row in range(len(board)):
            for col in range(len(board[row])):
                if board[row][col] == tile_type:
                    coordinates.append((col * square_size, row * square_size))
        return coordinates

def get_random_tile_coordinate(board, tile_type, square_size):
        coordinates = get_tile_coordinates(board, tile_type, square_size)
        return random.choice(coordinates) if coordinates else None