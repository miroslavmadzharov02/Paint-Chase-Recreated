import random
from src.tile import Tile

def is_empty_tile(tile):
            return tile in [Tile.EMPTY.board_index, Tile.ENEMY.board_index, 
                            Tile.PLAYER.board_index, Tile.RESPAWN.board_index,
                            Tile.BOOST.board_index]

def is_paintable_tile(tile):
       return tile in [Tile.EMPTY.board_index, Tile.ENEMY.board_index, 
                       Tile.PLAYER.board_index]

def is_boost_tile(tile):
      return tile in [Tile.BOOST.board_index]

def get_next_tile(direction, board, entity, center_x, center_y):
            fudge = 15
            if direction == entity.Direction.UP:
                return board[(center_y - fudge) // entity.square_size][center_x // entity.square_size]
            elif direction == entity.Direction.DOWN:
                return board[(center_y + fudge) // entity.square_size][center_x // entity.square_size]
            elif direction == entity.Direction.LEFT:
                return board[center_y // entity.square_size][(center_x - fudge) // entity.square_size]
            elif direction == entity.Direction.RIGHT:
                return board[center_y // entity.square_size][(center_x + fudge) // entity.square_size]
            return None

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