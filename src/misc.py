from src.tile import Tile

def is_empty_tile(tile):
            return tile == Tile.EMPTY.board_index or tile == Tile.PLAYER.board_index or tile == Tile.ENEMY.board_index

def get_next_tile(direction, level, entity, center_x, center_y):
            fudge = 15
            if direction == entity.Direction.UP:
                return level[(center_y - fudge) // entity.square_size][center_x // entity.square_size]
            elif direction == entity.Direction.DOWN:
                return level[(center_y + fudge) // entity.square_size][center_x // entity.square_size]
            elif direction == entity.Direction.LEFT:
                return level[center_y // entity.square_size][(center_x - fudge) // entity.square_size]
            elif direction == entity.Direction.RIGHT:
                return level[center_y // entity.square_size][(center_x + fudge) // entity.square_size]
            return None