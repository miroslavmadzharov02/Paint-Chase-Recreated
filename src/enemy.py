from src.entity import Entity
from src.tile import Tile
import pygame
import random

ENEMY_SVG_PATH = 'assets/enemy_car.svg'

class Enemy(Entity):
    def __init__(self, square_size, x, y):
        image = pygame.transform.scale(pygame.image.load(ENEMY_SVG_PATH), (square_size, square_size))
        super().__init__(square_size, image, x, y)

        self.previous_direction = self.direction

    def set_tile_attributes(self):
        self.friendly_tile = Tile.ENEMY
        self.enemy_tile = Tile.PLAYER
    
    def pick_direction(self, level, center_x, center_y):
        if self.turns_allowed[self.previous_direction]:
            if random.random() > 0.01:
                self.direction = self.previous_direction
                return


        def get_next_tile(level, center_x, center_y, direction):
            fudge = 15
            if direction == self.Direction.UP:
                return level[(center_y - fudge) // self.square_size][center_x // self.square_size]
            elif direction == self.Direction.DOWN:
                return level[(center_y + fudge) // self.square_size][center_x // self.square_size]
            elif direction == self.Direction.LEFT:
                return level[center_y // self.square_size][(center_x - fudge) // self.square_size]
            elif direction == self.Direction.RIGHT:
                return level[center_y // self.square_size][(center_x + fudge) // self.square_size]
            return None

        valid_directions = []
        for i in range(len(self.Direction)):
            if self.turns_allowed[i]:
                next_tile = get_next_tile(level, center_x, center_y, i)
                if next_tile == self.enemy_tile.board_index or next_tile == Tile.EMPTY.board_index:
                    valid_directions.append(i)

        if valid_directions:
            self.direction = random.choice(valid_directions)
            self.previous_direction = self.direction
        else:
            allowed_directions = [i for i in range(len(self.Direction)) if self.turns_allowed[i]]
            if allowed_directions:
                self.direction = random.choice(allowed_directions)
                self.previous_direction = self.direction

    def move(self, level, center_x, center_y):
        self.check_position(level, center_x, center_y)
        self.pick_direction(level, center_x, center_y)
        super().move()