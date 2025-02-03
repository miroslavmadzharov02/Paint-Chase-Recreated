import pygame
from enum import Enum

PLAYER_SVG_PATH = 'assets/player_car.svg'

class Player:
    class Direction(Enum):
        RIGHT = 0
        LEFT = 1
        UP = 2
        DOWN = 3

    def __init__(self, square_size):
        self.image = pygame.transform.scale(pygame.image.load(PLAYER_SVG_PATH), (square_size * 1.5, square_size))
        self.x = 0
        self.y = 0
        self.direction = Player.Direction.RIGHT

    def draw(self, screen):
        if self.direction == Player.Direction.RIGHT:
            screen.blit(self.image, (self.x, self.y))
        elif self.direction == Player.Direction.LEFT:
            flipped_image = pygame.transform.flip(self.image, True, False)
            screen.blit(flipped_image, (self.x, self.y))
        elif self.direction == Player.Direction.UP:
            rotated_image = pygame.transform.rotate(self.image, 90)
            screen.blit(rotated_image, (self.x, self.y))
        elif self.direction == Player.Direction.DOWN:
            rotated_image = pygame.transform.rotate(self.image, 270)
            screen.blit(rotated_image, (self.x, self.y))