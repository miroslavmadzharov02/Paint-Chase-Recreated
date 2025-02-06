import random
from src.misc import get_surrounding_tiles, is_paintable_tile, is_empty_tile

def get_next_direction(enemy, board, center_x, center_y):
        if enemy.turns_allowed[enemy.previous_direction]:
            if random.random() > 0.01:
                return enemy.previous_direction

        priority_directions = []
        empty_space_directions = []
        surrounding_tiles = get_surrounding_tiles(board, enemy, center_x, center_y)
        for direction, tile in surrounding_tiles:
            if is_paintable_tile(tile, enemy):
                priority_directions.append(direction)
            if is_empty_tile(tile):
                 empty_space_directions.append(direction)

        if priority_directions:
            return random.choice(priority_directions)
        elif empty_space_directions:
            return random.choice(empty_space_directions)
        
        allowed_directions = [i for i in range(len(enemy.Direction)) if enemy.turns_allowed[i]]
        if allowed_directions:
            return random.choice(allowed_directions)