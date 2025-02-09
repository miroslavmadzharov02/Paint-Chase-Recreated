import pytest
import pygame
from src.board import boards, board_enemy_counts
from src.enemy import Enemy
from src.level import Level

boards = [[[0, 4],
        [1, 0]]]

board_enemy_counts = [1, 1]

index = 0
level = Level(index, boards, board_enemy_counts)

pygame.init()
screen = pygame.Surface((100, 100))

def test_invalid_level_index() -> None:
    with pytest.raises(IndexError, match="Level index is out of range."):
        Level(10, boards, board_enemy_counts)

def test_empty_board() -> None:
    with pytest.raises(ValueError, match="Expected loaded board to not be empty."):
        Level(index, [[]], board_enemy_counts)

def test_different_row_lengths() -> None:
    with pytest.raises(ValueError, match="Row 1 has length 1; expected 2."):
        Level(0, [[[1, 2], [3]]], board_enemy_counts)

def test_missing_enemy_spawn_location() -> None:
    with pytest.raises(ValueError, match="Board contains no places for enemies to spawn/respawn"):
        Level(0, [[[0, 1], [0, 1]]], board_enemy_counts)

def test_empty_enemy_count() -> None:
    with pytest.raises(ValueError, match="Enemy count list is empty"):
        Level(0, boards, [])

def test_wrong_enemy_count() -> None:
    with pytest.raises(ValueError, match="Expected enemy count to be larger than 0."):
        Level(0, boards, [0])


def test_valid_level_initialization() -> None:
    level = Level(0, boards, board_enemy_counts)
    assert level.boards_count == 1
    assert level.current_level_index == 0
    assert level.enemy_count == 1
    assert level.rows_count == 2
    assert level.cols_count == 2

def test_initial_spawn_coordinates() -> None:
    level = Level(0, boards, board_enemy_counts)
    spawn_coords = level.get_initial_spawn_coordinates_enemies()
    assert len(spawn_coords) == 1
    assert all(isinstance(coord, tuple) and len(coord) == 2 for coord in spawn_coords)

def test_get_enemies() -> None:
    level = Level(0, boards, board_enemy_counts)
    enemies = level.get_enemies()
    assert len(enemies) == 1
    assert all(isinstance(enemy, Enemy) for enemy in enemies)