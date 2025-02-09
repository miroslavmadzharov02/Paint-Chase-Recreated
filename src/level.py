import pygame
from src.tile import Tile
from src.enemy import Enemy
from src.board_utils import get_random_tile_coordinate, get_tile_coordinates

class Level:
    """Class for handling details about current board"""
    def __init__(self, level_index: int, boards: list[list[list[int]]], board_enemy_counts: list[int]) -> None:
        self.boards_count: int = len(boards)
        if self.boards_count < level_index:
            raise IndexError("Level index is out of range.")
        self.current_level_index: int = level_index

        self.board: list[list[int]] = boards[self.current_level_index]
        if not self.board:
            raise ValueError("Expected loaded board to not be empty.")

        self.rows_count: int = len(self.board)
        self.cols_count: int = len(self.board[0])
        for index, row in enumerate(self.board):
            if len(row) != self.cols_count:
                raise ValueError(f"Row {index} has length {len(row)}; expected {self.cols_count}.")

        self.square_size: int = 50

        if not get_tile_coordinates(self.board, Tile.RESPAWN.board_index, self.square_size):
            raise ValueError("Board contains no places for enemies to spawn/respawn")

        if not board_enemy_counts:
            raise ValueError("Enemy count list is empty")
        if len(board_enemy_counts) < self.current_level_index:
            raise IndexError("Couldn't get enemy count.")
        self.enemy_count: int = board_enemy_counts[self.current_level_index]
        if self.enemy_count <= 0:
            raise ValueError("Expected enemy count to be larger than 0.")

    def draw(self, screen: pygame.Surface) -> None:
        for row_index, row in enumerate(self.board):
            for col_index, tile_index in enumerate(row):
                tile = next((t for t in Tile if t.board_index == tile_index), None)
                if tile:
                    pygame.draw.rect(
                        screen,
                        tile.color,
                        (col_index * self.square_size, row_index * self.square_size, self.square_size, self.square_size)
                    )

    def get_initial_spawn_coordinates_enemies(self) -> list[tuple[int, int]]:
        result = [get_random_tile_coordinate(self.board, Tile.RESPAWN.board_index, self.square_size) 
            for _ in range(self.enemy_count)]
        if not result:
            raise ValueError("Could not get initial spawn coords for enemies.")
        return result

    def get_enemies(self) -> list[Enemy]:
        coords = self.get_initial_spawn_coordinates_enemies()
        return [Enemy(self.square_size, x, y) for x,y in coords]