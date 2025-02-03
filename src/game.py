import pygame
from enum import Enum
from src.board import boards
from src.player import Player

class Game:
    BOTTOM_PADDING = 50
    WIDTH_TOTAL_TILES = 15
    HEIGHT_TOTAL_TILES = 9
    SQUARE_SIZE = 50
    FPS = 60

    class TILE(int, Enum):
        EMPTY = 0
        WALL = 1

    def __init__(self):
        pygame.init()

        self.WINDOW_WIDTH = self.WIDTH_TOTAL_TILES * self.SQUARE_SIZE
        self.WINDOW_HEIGHT = self.HEIGHT_TOTAL_TILES * self.SQUARE_SIZE + self.BOTTOM_PADDING

        self.screen = pygame.display.set_mode([self.WINDOW_WIDTH, self.WINDOW_HEIGHT])
        self.timer = pygame.time.Clock()

        self.current_level_index = 0
        self.level = boards[self.current_level_index]

        self.player = Player(self.SQUARE_SIZE)
        self.turns_allowed = [False, False, False, False]

        self.running = True

    def check_position(self, center_x, center_y):
        self.turns_allowed = [False, False, False, False]
        fudge = 15

        if 0 < center_x // self.WIDTH_TOTAL_TILES < self.SQUARE_SIZE - 1:
            if self.player.direction == self.player.Direction.RIGHT:
                if self.level[center_y // self.SQUARE_SIZE][(center_x - fudge) // self.SQUARE_SIZE] == self.TILE.EMPTY:
                    self.turns_allowed[self.player.Direction.LEFT] = True 
            if self.player.direction == self.player.Direction.LEFT:
                if self.level[center_y // self.SQUARE_SIZE][(center_x + fudge) // self.SQUARE_SIZE] == self.TILE.EMPTY:
                    self.turns_allowed[self.player.Direction.RIGHT] = True 
            if self.player.direction == self.player.Direction.UP:
                if self.level[(center_y + fudge) // self.SQUARE_SIZE][center_x // self.SQUARE_SIZE] == self.TILE.EMPTY:
                    self.turns_allowed[self.player.Direction.DOWN] = True 
            if self.player.direction == self.player.Direction.DOWN:
                if self.level[(center_y - fudge) // self.SQUARE_SIZE][center_x // self.SQUARE_SIZE] == self.TILE.EMPTY:
                    self.turns_allowed[self.player.Direction.UP] = True      

            if self.player.direction == self.player.Direction.UP or self.player.direction == self.player.Direction.DOWN:
                if 22 <= center_x % self.SQUARE_SIZE <= 28:
                    if self.level[(center_y + fudge) // self.SQUARE_SIZE][center_x // self.SQUARE_SIZE] == self.TILE.EMPTY:
                        self.turns_allowed[self.player.Direction.DOWN] = True
                    if self.level[(center_y - fudge) // self.SQUARE_SIZE][center_x // self.SQUARE_SIZE] == self.TILE.EMPTY:
                        self.turns_allowed[self.player.Direction.UP] = True
                if 22 <= center_y % self.SQUARE_SIZE <= 28:
                    if self.level[center_y // self.SQUARE_SIZE][(center_x - self.SQUARE_SIZE) // self.SQUARE_SIZE] == self.TILE.EMPTY:
                        self.turns_allowed[self.player.Direction.LEFT] = True
                    if self.level[center_y // self.SQUARE_SIZE][(center_x + self.SQUARE_SIZE) // self.SQUARE_SIZE] == self.TILE.EMPTY:
                        self.turns_allowed[self.player.Direction.RIGHT] = True

            if self.player.direction == self.player.Direction.LEFT or self.player.direction == self.player.Direction.RIGHT:
                if 22 <= center_x % self.SQUARE_SIZE <= 28:
                    if self.level[(center_y + self.SQUARE_SIZE) // self.SQUARE_SIZE][center_x // self.SQUARE_SIZE] == self.TILE.EMPTY:
                        self.turns_allowed[self.player.Direction.DOWN] = True
                    if self.level[(center_y - self.SQUARE_SIZE) // self.SQUARE_SIZE][center_x // self.SQUARE_SIZE] == self.TILE.EMPTY:
                        self.turns_allowed[self.player.Direction.UP] = True
                if 22 <= center_y % self.SQUARE_SIZE <= 28:
                    if self.level[center_y // self.SQUARE_SIZE][(center_x - fudge) // self.SQUARE_SIZE] == self.TILE.EMPTY:
                        self.turns_allowed[self.player.Direction.LEFT] = True
                    if self.level[center_y // self.SQUARE_SIZE][(center_x + fudge) // self.SQUARE_SIZE] == self.TILE.EMPTY:
                        self.turns_allowed[self.player.Direction.RIGHT] = True

    def move_player(self):
        if self.player.direction == self.player.Direction.RIGHT and self.turns_allowed[self.player.Direction.RIGHT]:
            self.player.x += self.player.speed
        elif self.player.direction == self.player.Direction.LEFT and self.turns_allowed[self.player.Direction.LEFT]:
            self.player.x -= self.player.speed
        if self.player.direction == self.player.Direction.UP and self.turns_allowed[self.player.Direction.UP]:
            self.player.y -= self.player.speed
        elif self.player.direction == self.player.Direction.DOWN and self.turns_allowed[self.player.Direction.DOWN]:
            self.player.y += self.player.speed

    def draw_board(self):
        for row in range(len(self.level)):
            for col in range(len(self.level[row])):
                if self.level[row][col] == self.TILE.EMPTY:
                    pygame.draw.rect(self.screen, 'purple', (col * self.SQUARE_SIZE, row * self.SQUARE_SIZE, self.SQUARE_SIZE, self.SQUARE_SIZE))
                if self.level[row][col] == self.TILE.WALL:
                    pygame.draw.rect(self.screen, 'green', (col * self.SQUARE_SIZE, row * self.SQUARE_SIZE, self.SQUARE_SIZE, self.SQUARE_SIZE))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.player.set_command(Player.Direction.RIGHT)
                if event.key == pygame.K_LEFT:
                    self.player.set_command(Player.Direction.LEFT)
                if event.key == pygame.K_DOWN:
                    self.player.set_command(Player.Direction.DOWN)
                if event.key == pygame.K_UP:
                    self.player.set_command(Player.Direction.UP)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT and self.player.direction_command == self.player.Direction.RIGHT:
                    self.player.set_command(Player.Direction.RIGHT)
                if event.key == pygame.K_LEFT and self.player.direction_command == self.player.Direction.LEFT:
                    self.player.set_command(Player.Direction.LEFT)
                if event.key == pygame.K_DOWN and self.player.direction_command == self.player.Direction.DOWN:
                    self.player.set_command(Player.Direction.DOWN)
                if event.key == pygame.K_UP and self.player.direction_command == self.player.Direction.UP:
                    self.player.set_command(Player.Direction.UP)   

        for i in range(len(self.player.Direction)):
            if self.player.direction_command == i and self.turns_allowed[i]:
                self.player.face(i)

        if self.player.x > self.WINDOW_WIDTH:
            self.player.x = -50
        elif self.player.x < -50:
            self.player.x = self.WINDOW_WIDTH - 5




    def update_display(self):
        self.timer.tick(self.FPS)
        self.screen.fill('black')
        self.draw_board()
        self.player.draw(self.screen)

        center_x, center_y = self.player.get_centered_coords()
        self.check_position(center_x, center_y)
        self.move_player()
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update_display()
        pygame.quit()