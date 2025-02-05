import random
from src.tile import Tile

def is_empty_tile(tile):
        return tile in [Tile.EMPTY.board_index, Tile.ENEMY.board_index, 
                        Tile.PLAYER.board_index, Tile.RESPAWN.board_index,
                        Tile.BOOST.board_index]

def is_paintable_tile(tile, entity):
        return tile in [Tile.EMPTY.board_index, entity.enemy_tile.board_index]

def is_boost_tile(tile):
        return tile in [Tile.BOOST.board_index]

def get_surrounding_tiles(board, entity, center_x, center_y):
        fudge = entity.square_size - (entity.square_size // 10)
        rows = len(board)
        cols = len(board[0]) if rows > 0 else 0

        result = []

        right_tile_row = center_y // entity.square_size
        right_tile_col = (center_x + fudge) // entity.square_size
        if right_tile_col < cols:
            current_tile = board[right_tile_row][right_tile_col]
            result.append((entity.Direction.RIGHT, current_tile))

        left_tile_row = center_y // entity.square_size
        left_tile_col = (center_x - fudge) // entity.square_size
        if left_tile_col >= 0:
            current_tile = board[left_tile_row][left_tile_col]
            result.append((entity.Direction.LEFT, current_tile))

        tile_above_row = (center_y - fudge) // entity.square_size
        tile_above_col = center_x // entity.square_size
        if tile_above_row >= 0:
            current_tile = board[tile_above_row][tile_above_col]
            result.append((entity.Direction.UP, current_tile))

        tile_below_row = (center_y + fudge) // entity.square_size
        tile_below_col = center_x // entity.square_size
        if tile_below_row < rows:
            current_tile = board[tile_below_row][tile_below_col]
            result.append((entity.Direction.DOWN, current_tile))
        
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