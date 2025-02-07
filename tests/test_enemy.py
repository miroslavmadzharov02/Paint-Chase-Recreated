import pygame
import random
from src.tile import Tile
from src.enemy import Enemy
from src.board_utils import get_random_tile_coordinate

pygame.init()
enemy = Enemy(square_size=50, x=0, y=0)

board = [
    [0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 4],
    [0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0],
    [0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0],
    [5, 0, 0, 0, 0, 0, 0, 5, 0, 1, 1, 1, 0, 1, 5],
    [0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0],
    [0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0],
    [4, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 4]
]

def test_initialization() -> None:
    assert enemy.square_size == 50
    assert enemy.x == 0
    assert enemy.y == 0
    assert enemy.dead == False
    assert enemy.friendly_tile == Tile.ENEMY
    assert enemy.enemy_tile == Tile.PLAYER

def test_move() -> None:
    initial_x, initial_y = enemy.x, enemy.y
    enemy.move(board, enemy.x, enemy.y)
    assert (initial_x, initial_y) != (enemy.x, enemy.y)

def test_die() -> None:
    enemy.die()
    assert enemy.dead == True

def test_respawn() -> None:
    random.seed(0)
    x, y = get_random_tile_coordinate(board, Tile.RESPAWN.board_index, enemy.square_size)
    enemy.respawn(board)
    assert enemy.dead is False
    assert (enemy.x, enemy.y) == (x, y)

def test_get_next_direction_paintable() -> None:
    direction = enemy.get_next_direction(board, 0, 0)
    assert direction  in [enemy.Direction.DOWN, enemy.Direction.RIGHT]
