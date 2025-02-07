import pytest
from src.tile import Tile, is_empty_tile, is_paintable_tile, is_boost_tile

@pytest.mark.parametrize("tile, expected", [
        (Tile.EMPTY.board_index, True),
        (Tile.ENEMY.board_index, True),
        (Tile.PLAYER.board_index, True),
        (Tile.RESPAWN.board_index, True),
        (Tile.BOOST.board_index, True),
        (Tile.WALL.board_index, False)
    ])
def test_is_empty_tile(tile, expected):
    assert is_empty_tile(tile) == expected

@pytest.mark.parametrize("tile, entity_enemy_tile, expected", [
        (Tile.EMPTY.board_index, Tile.ENEMY, True),
        (Tile.ENEMY.board_index, Tile.ENEMY, True),
        (Tile.WALL.board_index, Tile.ENEMY, False),
        (Tile.BOOST.board_index, Tile.ENEMY, False),
        (Tile.RESPAWN.board_index, Tile.ENEMY, False)
    ])
def test_is_paintable_tile(mocker, tile, entity_enemy_tile, expected):
    entity_mock = mocker.Mock()
    entity_mock.enemy_tile = entity_enemy_tile
    assert is_paintable_tile(tile, entity_mock) == expected

@pytest.mark.parametrize("tile, expected", 
    [(tile.board_index, tile == Tile.BOOST) for tile in Tile.__members__.values()])
def test_is_boost_tile(tile, expected):
    assert is_boost_tile(tile) == expected