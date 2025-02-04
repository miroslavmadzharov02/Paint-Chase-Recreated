from enum import Enum
import pygame
from src.tile import Tile
from abc import abstractmethod

class Entity:
    class Direction(int, Enum):
        RIGHT = 0
        LEFT = 1
        UP = 2
        DOWN = 3

    def __init__(self, square_size, image, x, y):
        self.square_size = square_size
        self.image = image
        self.x = x
        self.y = y
        self.direction = Entity.Direction.RIGHT
        self.turns_allowed = [False, False, False, False]
        self.speed = 2

        self.friendly_tile = None
        self.enemy_tile = None
        self.set_tile_attributes()

    @abstractmethod
    def set_tile_attributes(self):
        pass

    def draw(self, screen):
        if self.direction == Entity.Direction.RIGHT:
            screen.blit(self.image, (self.x, self.y))
        elif self.direction == Entity.Direction.LEFT:
            flipped_image = pygame.transform.flip(self.image, True, False)
            screen.blit(flipped_image, (self.x, self.y))
        elif self.direction == Entity.Direction.UP:
            rotated_image = pygame.transform.rotate(self.image, 90)
            screen.blit(rotated_image, (self.x, self.y))
        elif self.direction == Entity.Direction.DOWN:
            rotated_image = pygame.transform.rotate(self.image, 270)
            screen.blit(rotated_image, (self.x, self.y))

    def check_position(self, level, center_x, center_y):
        fudge = 15
        self.turns_allowed = [False, False, False, False]
        
        def is_empty_tile(tile):
            return tile == Tile.EMPTY.board_index or tile == Tile.PLAYER.board_index or tile == Tile.ENEMY.board_index
      
        if is_empty_tile(level[(center_y + fudge) // self.square_size][center_x // self.square_size]):
            self.turns_allowed[self.Direction.DOWN] = True
        if is_empty_tile(level[(center_y - fudge) // self.square_size][center_x // self.square_size]):
            self.turns_allowed[self.Direction.UP] = True

        if is_empty_tile(level[center_y // self.square_size][(center_x - fudge) // self.square_size]):
            self.turns_allowed[self.Direction.LEFT] = True
        if is_empty_tile(level[center_y // self.square_size][(center_x + fudge) // self.square_size]):
            self.turns_allowed[self.Direction.RIGHT] = True 

    def move(self):
        if self.direction == self.Direction.RIGHT and self.turns_allowed[self.Direction.RIGHT]:
            self.x += self.speed
        elif self.direction == self.Direction.LEFT and self.turns_allowed[self.Direction.LEFT]:
            self.x -= self.speed
        if self.direction == self.Direction.UP and self.turns_allowed[self.Direction.UP]:
            self.y -= self.speed
        elif self.direction == self.Direction.DOWN and self.turns_allowed[self.Direction.DOWN]:
            self.y += self.speed

    def paint_tile(self, level, center_x, center_y, WINDOW_WIDTH):
        if 0 < self.x < WINDOW_WIDTH - self.square_size:
            current_tile = level[center_y // self.square_size][center_x // self.square_size]
            if current_tile == Tile.EMPTY.board_index or current_tile == self.enemy_tile.board_index:
                 level[center_y // self.square_size][center_x // self.square_size] = self.friendly_tile.board_index

    def face(self, direction):
        self.direction = direction

    def get_centered_coords(self):
        center_x = self.x + (self.square_size // 2)
        center_y = self.y + (self.square_size // 2)

        return center_x, center_y