import pytest
from src.tile import Tile
from src.player import Player

player = Player(square_size=50, x=0, y=0)

# 21 3's 19 20's
board_player_win = [
    [3, 3, 3, 3, 3, 3, 3, 5, 3, 3, 3, 3, 3, 3, 4],
    [3, 1, 3, 1, 3, 1, 1, 3, 3, 1, 3, 1, 3, 1, 3],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 1, 2, 2, 2],
    [2, 1, 2, 1, 2, 1, 2, 2, 2, 1, 0, 0, 0, 1, 0],
    [5, 0, 0, 0, 0, 0, 0, 5, 0, 1, 1, 1, 0, 1, 5],
    [0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0],
    [0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0],
    [4, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 4]
]

# 21 3's 22 2's
board_player_loss = [
    [3, 3, 3, 3, 3, 3, 3, 5, 3, 3, 3, 3, 3, 3, 4],
    [3, 1, 3, 1, 3, 1, 1, 3, 3, 1, 3, 1, 3, 1, 3],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 1, 2, 2, 2],
    [2, 1, 2, 1, 2, 1, 2, 2, 2, 1, 2, 2, 2, 1, 0],
    [5, 0, 0, 0, 0, 0, 0, 5, 0, 1, 1, 1, 0, 1, 5],
    [0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0],
    [0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0],
    [4, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 4]
]

def test_initialization() -> None:
    assert player.square_size == 50
    assert player.x == 0
    assert player.y == 0
    assert player.friendly_tile == Tile.PLAYER
    assert player.enemy_tile == Tile.ENEMY

def test_set_command() -> None:
    new_command = Player.Direction.UP
    player.set_command(new_command)

    assert player.direction_command == new_command

@pytest.mark.parametrize("board, expected", [
    (board_player_win, True),
    (board_player_loss, False)
])
def test_check_player_win(board, expected) -> None:
    assert player.check_player_win(board) == expected