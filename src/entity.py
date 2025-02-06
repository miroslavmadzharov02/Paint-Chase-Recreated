from enum import Enum
import pygame
from src.tile import Tile, is_empty_tile, is_paintable_tile, is_boost_tile

class Entity:
    class Direction(int, Enum):
        RIGHT = 0
        LEFT = 1
        UP = 2
        DOWN = 3

    def __init__(self, square_size: int, image: pygame.Surface, x: int, y: int, friendly_tile: Tile, enemy_tile: Tile) -> None:
        self.square_size: int = square_size
        self.image: pygame.Surface = image
        self.x: int = x
        self.y: int = y
        self.direction: Entity.Direction = Entity.Direction.RIGHT
        self.turns_allowed: list[bool] = [False, False, False, False]
        
        self.base_speed: int = 2
        self.current_speed: int = self.base_speed
        self.boost_speed: int = 1
        self.boost_time: int = 0 
        self.boost_duration: int = 1000   

        self.friendly_tile = friendly_tile
        self.enemy_tile = enemy_tile

    def draw(self, screen) -> None:
        direction_map = {
        Entity.Direction.RIGHT: lambda: self.image,
        Entity.Direction.LEFT: lambda: pygame.transform.flip(self.image, True, False),
        Entity.Direction.UP: lambda: pygame.transform.rotate(self.image, 90),
        Entity.Direction.DOWN: lambda: pygame.transform.rotate(self.image, 270),
                        }

        transformed_image = direction_map.get(self.direction, lambda: self.image)()
        screen.blit(transformed_image, (self.x, self.y))

    def get_rect(self) -> pygame.Rect:
        center_x, center_y = self.get_centered_coords()
        return pygame.Rect(center_x, center_y, self.square_size, self.square_size)

    def check_position(self, board: list[list[int]], center_x: int, center_y: int) -> None:
        fudge = 15
        rows = len(board)
        cols = len(board[0]) if rows > 0 else 0

        self.turns_allowed = [False, False, False, False]

        direction_map = {
            self.Direction.DOWN: (center_y + fudge, center_x),
            self.Direction.UP: (center_y - fudge, center_x),
            self.Direction.LEFT: (center_y, center_x - fudge),
            self.Direction.RIGHT: (center_y, center_x + fudge),
        }

        def in_bounds(row: int, col: int) -> bool:
            return 0 <= row < rows and 0 <= col < cols

        for direction, (y_offset, x_offset) in direction_map.items():
            tile_row = (y_offset) // self.square_size
            tile_col = (x_offset) // self.square_size
            if in_bounds(tile_row, tile_col) and is_empty_tile(board[tile_row][tile_col]):
                self.turns_allowed[direction] = True

    def move(self) -> None:
        if self.direction == self.Direction.RIGHT and self.turns_allowed[self.Direction.RIGHT]:
            self.x += self.current_speed
        elif self.direction == self.Direction.LEFT and self.turns_allowed[self.Direction.LEFT]:
            self.x -= self.current_speed
        if self.direction == self.Direction.UP and self.turns_allowed[self.Direction.UP]:
            self.y -= self.current_speed
        elif self.direction == self.Direction.DOWN and self.turns_allowed[self.Direction.DOWN]:
            self.y += self.current_speed

    def interact_tile(self, board: list[list[int]], center_x: int, center_y: int, window_width: int) -> None:
        if 0 < center_x < window_width:
            current_tile = board[center_y // self.square_size][center_x // self.square_size]
            if is_paintable_tile(current_tile, self):
                 board[center_y // self.square_size][center_x // self.square_size] = self.friendly_tile.board_index
            if is_boost_tile(current_tile):
                if self.boost_time == 0:
                    self.current_speed += self.boost_speed 
                    self.boost_time = pygame.time.get_ticks()    

    def reset_speed(self) -> None:
        self.current_speed = self.base_speed

    def check_boost_time(self) -> None:
        if self.boost_time != 0:
            if pygame.time.get_ticks() - self.boost_time > self.boost_duration:
                self.reset_speed() 
                self.boost_time = 0 

    def face(self, direction) -> None:
        self.direction = direction

    def get_centered_coords(self) -> tuple[int, int]:
        center_x = self.x + (self.square_size // 2)
        center_y = self.y + (self.square_size // 2)

        return center_x, center_y