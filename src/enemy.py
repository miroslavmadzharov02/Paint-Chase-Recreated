import pygame
from src.entity import Entity
from src.tile import Tile
from src.enemy_movement import get_next_direction
from src.misc import get_random_tile_coordinate

ENEMY_SVG_PATH = 'assets/enemy_car.svg'

class Enemy(Entity):
    """Enemy class"""
    def __init__(self, square_size, x, y):
        image = pygame.transform.scale(pygame.image.load(ENEMY_SVG_PATH), (square_size, square_size))
        super().__init__(square_size, image, x, y)

        self.dead = False
        self.respawn_delay_ms = 2000
        self.respawn_time = 0
        
        self.previous_direction = self.direction

    def set_tile_attributes(self):
        self.friendly_tile = Tile.ENEMY
        self.enemy_tile = Tile.PLAYER

    def move(self, board, center_x, center_y):
        self.check_position(board, center_x, center_y)
        
        self.direction = get_next_direction(self, board, center_x, center_y)
        self.previous_direction = self.direction

        super().move()

    def die(self):
        self.dead = True
        self.respawn_time = pygame.time.get_ticks() + self.respawn_delay_ms

    def respawn(self, board):
        self.dead = False
        self.x, self.y = get_random_tile_coordinate(board, Tile.RESPAWN.board_index, self.square_size)