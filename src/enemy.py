import pygame
from src.entity import Entity
from src.tile import Tile
from src.enemy_movement import pick_direction_generator
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
        
        self.speed = 1
        self.previous_direction = self.direction

        self.direction_generator = None

    def set_tile_attributes(self):
        self.friendly_tile = Tile.ENEMY
        self.enemy_tile = Tile.PLAYER

    def move(self, level, center_x, center_y):
        self.check_position(level, center_x, center_y)

        self.direction_generator = pick_direction_generator(self, level, center_x, center_y)
        self.direction = next(self.direction_generator, self.previous_direction)
        self.previous_direction = self.direction

        super().move()

    def die(self):
        self.dead = True
        self.respawn_time = pygame.time.get_ticks() + self.respawn_delay_ms

    def respawn(self, level):
        self.dead = False
        self.x, self.y = get_random_tile_coordinate(level, Tile.RESPAWN.board_index, self.square_size)