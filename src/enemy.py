import random
import pygame
from src.entity import Entity
from src.tile import Tile, is_paintable_tile, is_empty_tile
from src.board_utils import get_surrounding_tiles, get_random_tile_coordinate

ENEMY_SVG_PATH = 'assets/enemy_car.svg'

class Enemy(Entity):
    """Class for non-player controlled entity"""
    def __init__(self, square_size: int, x: int, y: int):
        image = pygame.transform.scale(pygame.image.load(ENEMY_SVG_PATH), (square_size, square_size))
        super().__init__(square_size, image, x, y, Tile.ENEMY, Tile.PLAYER)

        self.dead: bool = False
        self.respawn_delay_ms: int = 2000
        self.respawn_time: int = 0

        self.previous_direction: Entity.Direction = self.direction

    def move(self, board: list[list[int]], center_x: int, center_y: int) -> None:
        self.check_position(board, center_x, center_y)

        self.direction = self.get_next_direction(board, center_x, center_y)
        self.previous_direction = self.direction

        super().move()

    def die(self) -> None:
        self.dead = True
        self.respawn_time = pygame.time.get_ticks() + self.respawn_delay_ms

    def respawn(self, board: list[list[int]]) -> None:
        self.dead = False
        self.x, self.y = get_random_tile_coordinate(board, Tile.RESPAWN.board_index, self.square_size)

    def get_next_direction(self, board: list[list[int]], center_x: int, center_y:int) -> Entity.Direction:
        if self.turns_allowed[self.previous_direction]:
            if random.random() > 0.01:
                return self.previous_direction

        priority_directions = []
        empty_space_directions = []
        surrounding_tiles = get_surrounding_tiles(board, self, center_x, center_y)
        for direction, tile in surrounding_tiles:
            if is_paintable_tile(tile, self):
                priority_directions.append(direction)
            if is_empty_tile(tile):
                empty_space_directions.append(direction)

        if priority_directions:
            return random.choice(priority_directions)
        elif empty_space_directions:
            return random.choice(empty_space_directions)

        allowed_directions = [d for d in self.Direction if self.turns_allowed[d]]
        if allowed_directions:
            return random.choice(allowed_directions)

        return self.Direction.RIGHT