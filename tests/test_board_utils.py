import pytest
import pygame
from src.tile import Tile
from src.entity import Entity
from src.board_utils import get_surrounding_tiles, get_tile_coordinates, get_random_tile_coordinate

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

pygame.init()
image = pygame.Surface((0, 0))
entity = Entity(
square_size=1,
image=image,
x=0,
y=0,
friendly_tile=Tile.PLAYER,
enemy_tile=Tile.ENEMY
)

@pytest.mark.parametrize("center_x, center_y, expected_result", [
    (0, 0, [(Entity.Direction.RIGHT, 0), (Entity.Direction.DOWN, 0)]),
    (8, 4, [(Entity.Direction.RIGHT, 1), (Entity.Direction.LEFT, 5),(Entity.Direction.UP, 0), (Entity.Direction.DOWN, 0)])
])
def test_get_surrounding_tiles(center_x, center_y, expected_result) -> None:
    result = get_surrounding_tiles(board, entity, center_x, center_y)
    assert result == expected_result


tile_5_positions = [(0, 4), (7, 0), (7, 4), (14, 4), (7, 8)]
tile_4_positions = [(0, 8), (14,0), (14,8)]

@pytest.mark.parametrize("tile_type, expected_coordinates", [
    (5, tile_5_positions),
    (4, tile_4_positions), 
])
def test_get_tile_coordinates(tile_type, expected_coordinates) -> None:
    result = get_tile_coordinates(board, tile_type, square_size=1)
    assert sorted(result) == sorted(expected_coordinates)

def test_get_random_tile_coordinate() -> None:
    result = get_random_tile_coordinate(board, tile_type=5, square_size=1)
    assert result in tile_5_positions