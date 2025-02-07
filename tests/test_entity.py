import pytest
import pygame
from src.tile import Tile, is_empty_tile, is_paintable_tile, is_boost_tile
from src.entity import Entity

pygame.init()
image = pygame.Surface((0, 0))
entity = Entity(
square_size=50,
image=image,
x=0,
y=0,
friendly_tile=Tile.PLAYER,
enemy_tile=Tile.ENEMY
)

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

@pytest.mark.parametrize("direction_to_face", [
    (Entity.Direction.LEFT),
    (Entity.Direction.DOWN)
])
def test_face(direction_to_face) -> None:
    entity.face(direction_to_face)
    assert entity.direction == direction_to_face

@pytest.mark.parametrize("x, y, expected", [
    (2, 2, [True, True, True, True])
])
def test_check_position(x, y, expected) -> None:
    entity.x = x
    entity.y = y
    center_x, center_y = entity.get_centered_coords()
    entity.check_position(board, center_x, center_y)
    assert entity.turns_allowed == expected

def test_interact_tile_paint() -> None:
    center_x, center_y = entity.get_centered_coords()
    entity.interact_tile(board, center_x, center_y, len(board[0]) * entity.square_size)
    assert board[0][0] == entity.friendly_tile.board_index

def test_move() -> None:
    entity.turns_allowed = [True, True, True, True]

    entity.x = 0
    entity.y = 0

    entity.face(Entity.Direction.RIGHT)
    entity.move()
    assert entity.x == entity.base_speed

    entity.face(Entity.Direction.LEFT)
    entity.move()
    assert entity.x == 0

    entity.face(Entity.Direction.DOWN)
    entity.move()
    assert entity.y == entity.base_speed

    entity.face(Entity.Direction.UP)
    entity.move()
    assert entity.y == 0