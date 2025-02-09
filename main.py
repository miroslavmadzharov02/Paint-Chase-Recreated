"""Main class for running the game"""
from src.game import Game

CURRENT_LEVEL_INDEX = 0
MULTIPLAYER = False

game = Game(CURRENT_LEVEL_INDEX, MULTIPLAYER)
game.run()