import pygame
from src.entity import Entity
from src.tile import Tile

PLAYER_SVG_PATH = 'assets/player_car.svg'

class Player(Entity):
    """Player class"""
    def __init__(self, square_size, x, y):
        image = pygame.transform.scale(pygame.image.load(PLAYER_SVG_PATH), (square_size, square_size))
        super().__init__(square_size, image, x, y, Tile.PLAYER, Tile.ENEMY)

        self.direction_command = Entity.Direction.RIGHT

    def set_command(self, direction_command):
        self.direction_command = direction_command
    
    def check_player_win(self, board):
        count_enemy = sum(row.count(Tile.ENEMY.board_index) for row in board)
        count_player = sum(row.count(Tile.PLAYER.board_index) for row in board)

        return count_player > count_enemy