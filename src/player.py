import pygame
from enum import Enum

class Direction(Enum):
    RIGHT = 0
    LEFT = 1
    UP = 2
    DOWN = 3

PLAYER_SVG_PATH = 'assets/player_car.svg'

class Player:
    def __init__(self, square_size):
        self.image = pygame.transform.scale(pygame.image.load(PLAYER_SVG_PATH), (square_size * 1.5, square_size))
        self.x = 0
        self.y = 0
        self.direction = Direction.RIGHT

    def draw(self, screen):
        if self.direction == Direction.RIGHT:
            screen.blit(self.image, (self.x, self.y))
        elif self.direction == Direction.LEFT:
            flipped_image = pygame.transform.flip(self.image, True, False)
            screen.blit(flipped_image, (self.x, self.y))
        elif self.direction == Direction.UP:
            rotated_image = pygame.transform.rotate(self.image, 90)
            screen.blit(rotated_image, (self.x, self.y))
        elif self.direction == Direction.DOWN:
            rotated_image = pygame.transform.rotate(self.image, 270)
            screen.blit(rotated_image, (self.x, self.y))