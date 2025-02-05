import random
from src.tile import Tile
from src.misc import get_next_tile

def pick_direction_generator(enemy, level, center_x, center_y):
        if enemy.turns_allowed[enemy.previous_direction]:
            if random.random() > 0.01:
                yield enemy.previous_direction
                return

        valid_directions = []
        for i in range(len(enemy.Direction)):
            if enemy.turns_allowed[i]:
                next_tile = get_next_tile(i, level, enemy, center_x, center_y)
                if next_tile == enemy.enemy_tile.board_index or next_tile == Tile.EMPTY.board_index:
                    valid_directions.append(i)

        if valid_directions:
            yield random.choice(valid_directions)
        else:
            allowed_directions = [i for i in range(len(enemy.Direction)) if enemy.turns_allowed[i]]
            if allowed_directions:
                yield random.choice(allowed_directions)