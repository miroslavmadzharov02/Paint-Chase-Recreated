import pygame
from src.tile import Tile
from src.board import boards
from src.player import Player
from src.enemy import Enemy
from src.bar import Bar

WIN_SVG_PATH = "assets/win.svg"
LOSE_SVG_PATH = "assets/lose.svg"

class Game:
    BOTTOM_PADDING = 50
    WIDTH_TOTAL_TILES = 15
    HEIGHT_TOTAL_TILES = 9
    SQUARE_SIZE = 50
    FPS = 60

    def __init__(self):
        pygame.init()

        self.WINDOW_WIDTH = self.WIDTH_TOTAL_TILES * self.SQUARE_SIZE
        self.WINDOW_HEIGHT = self.HEIGHT_TOTAL_TILES * self.SQUARE_SIZE + self.BOTTOM_PADDING

        self.screen = pygame.display.set_mode([self.WINDOW_WIDTH, self.WINDOW_HEIGHT])
        self.timer = pygame.time.Clock()

        self.current_level_index = 0
        self.level = boards[self.current_level_index]

        self.player = Player(self.SQUARE_SIZE, 0, 0)

        self.enemy = Enemy(self.SQUARE_SIZE, 0, self.WINDOW_HEIGHT - self.SQUARE_SIZE - self.BOTTOM_PADDING)

        self.bar = Bar(self.WINDOW_HEIGHT, self.WINDOW_WIDTH, self.BOTTOM_PADDING)

        self.win_image = pygame.transform.scale(pygame.image.load(WIN_SVG_PATH), (self.SQUARE_SIZE * 10, self.SQUARE_SIZE * 10))
        self.lose_image = pygame.transform.scale(pygame.image.load(LOSE_SVG_PATH), (self.SQUARE_SIZE * 10, self.SQUARE_SIZE * 10))

        self.running = True

    def draw_board(self):
        for row in range(len(self.level)):
            for col in range(len(self.level[row])):
                for tile in Tile:
                    if self.level[row][col] == tile.board_index:
                        pygame.draw.rect(self.screen, tile.color, (col * self.SQUARE_SIZE, row * self.SQUARE_SIZE, self.SQUARE_SIZE, self.SQUARE_SIZE))

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
            if self.player.direction_command == i and self.player.turns_allowed[i]:
                self.player.face(i)

    def display_game_over_screen(self, player_won):
        image = self.win_image if player_won else self.lose_image

        while True:
            self.screen.fill("black")
            self.screen.blit(image, (0, 0))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        return

    def update_display(self):
        self.timer.tick(self.FPS)
        self.screen.fill('black')
        self.draw_board()
        self.player.draw(self.screen)
        self.enemy.draw(self.screen)

        center_x, center_y = self.player.get_centered_coords()
        self.player.check_position(self.level, center_x, center_y)
        self.player.move()
        self.player.paint_tile(self.level, center_x, center_y, self.WINDOW_WIDTH)

        center_x_enemy, center_y_enemy = self.enemy.get_centered_coords()
        self.enemy.move(self.level, center_x_enemy, center_y_enemy)
        self.enemy.paint_tile(self.level, center_x_enemy, center_y_enemy, self.WINDOW_WIDTH)

        self.bar.draw(self.screen)
        if self.bar.is_time_over():
            self.display_game_over_screen(self.player.check_player_win(self.level))

        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update_display()
        pygame.quit()