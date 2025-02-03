import pygame
from enum import Enum

PLAYER_SVG_PATH = 'assets/player_car.svg'

class Player:
    class Direction(int, Enum):
        RIGHT = 0
        LEFT = 1
        UP = 2
        DOWN = 3

    def __init__(self, square_size):
        self.image = pygame.transform.scale(pygame.image.load(PLAYER_SVG_PATH), (square_size, square_size))
        self.square_size = square_size
        self.x = 0
        self.y = 0
        self.direction = Player.Direction.RIGHT
        self.direction_command = Player.Direction.RIGHT
        self.turns_allowed = [False, False, False, False]
        self.speed = 2

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

    def face(self, direction):
        self.direction = direction

    def set_command(self, direction_command):
        self.direction_command = direction_command

    def get_centered_coords(self):
        center_x = self.x + (self.square_size // 2)
        center_y = self.y + (self.square_size // 2)

        return center_x, center_y