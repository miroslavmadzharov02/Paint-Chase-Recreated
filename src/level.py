import pygame
from src.board import boards, board_enemy_counts
from src.tile import Tile
from src.enemy import Enemy
from src.misc import get_random_tile_coordinate

class Level:
    def __init__(self, level_index):
        self.boards_count = len(boards)
        if self.boards_count < level_index:    
            return
        self.current_level_index = level_index

        self.board = boards[self.current_level_index]

        self.rows_count = len(self.board)
        self.cols_count = len(self.board[0])

        self.square_size = 50

        if len(board_enemy_counts) < self.current_level_index:
            return
        self.enemy_count = board_enemy_counts[self.current_level_index]

    def draw(self, screen):
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                for tile in Tile:
                    if self.board[row][col] == tile.board_index:
                        pygame.draw.rect(screen, tile.color, (col * self.square_size, row * self.square_size, self.square_size, self.square_size))

    def get_initial_spawn_coordinates_enemies(self):
        return [get_random_tile_coordinate(self.board, Tile.RESPAWN.board_index, self.square_size) 
            for _ in range(self.enemy_count)]
    
    def get_enemies(self):
        coords = self.get_initial_spawn_coordinates_enemies()
        return [Enemy(self.square_size, x, y) for x,y in coords]