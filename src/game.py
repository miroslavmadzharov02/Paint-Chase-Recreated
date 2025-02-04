import pygame
from src.tile import Tile
from src.board import boards
from src.player import Player
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

        self.player = Player(self.SQUARE_SIZE)
        self.turns_allowed = [False, False, False, False]

        self.bar = Bar(self.WINDOW_HEIGHT, self.WINDOW_WIDTH, self.BOTTOM_PADDING)

        self.win_image = pygame.transform.scale(pygame.image.load(WIN_SVG_PATH), (self.SQUARE_SIZE * 10, self.SQUARE_SIZE * 10))
        self.lose_image = pygame.transform.scale(pygame.image.load(LOSE_SVG_PATH), (self.SQUARE_SIZE, self.SQUARE_SIZE))

        self.running = True

    def check_position(self, center_x, center_y):
        fudge = 15
        self.turns_allowed = [False, False, False, False]
        
        def is_empty_tile(tile):
            return tile == Tile.EMPTY.board_index or tile == Tile.PLAYER.board_index or tile == Tile.ENEMY.board_index

        if self.player.direction == self.player.Direction.RIGHT:
            if is_empty_tile(self.level[center_y // self.SQUARE_SIZE][(center_x - fudge) // self.SQUARE_SIZE]):
                self.turns_allowed[self.player.Direction.LEFT] = True 
        if self.player.direction == self.player.Direction.LEFT:
            if is_empty_tile(self.level[center_y // self.SQUARE_SIZE][(center_x + fudge) // self.SQUARE_SIZE]):
                self.turns_allowed[self.player.Direction.RIGHT] = True 
        if self.player.direction == self.player.Direction.UP:
            if is_empty_tile(self.level[(center_y + fudge) // self.SQUARE_SIZE][center_x // self.SQUARE_SIZE]):
                self.turns_allowed[self.player.Direction.DOWN] = True 
        if self.player.direction == self.player.Direction.DOWN:
            if is_empty_tile(self.level[(center_y - fudge) // self.SQUARE_SIZE][center_x // self.SQUARE_SIZE]):
                self.turns_allowed[self.player.Direction.UP] = True      

        if self.player.direction == self.player.Direction.UP or self.player.direction == self.player.Direction.DOWN:
            if 22 <= center_x % self.SQUARE_SIZE <= 28:
                if is_empty_tile(self.level[(center_y + fudge) // self.SQUARE_SIZE][center_x // self.SQUARE_SIZE]):
                    self.turns_allowed[self.player.Direction.DOWN] = True
                if is_empty_tile(self.level[(center_y - fudge) // self.SQUARE_SIZE][center_x // self.SQUARE_SIZE]):
                    self.turns_allowed[self.player.Direction.UP] = True
            if 22 <= center_y % self.SQUARE_SIZE <= 28:
                if is_empty_tile(self.level[center_y // self.SQUARE_SIZE][(center_x - fudge) // self.SQUARE_SIZE]):
                    self.turns_allowed[self.player.Direction.LEFT] = True
                if is_empty_tile(self.level[center_y // self.SQUARE_SIZE][(center_x + fudge) // self.SQUARE_SIZE]):
                    self.turns_allowed[self.player.Direction.RIGHT] = True

        if self.player.direction == self.player.Direction.LEFT or self.player.direction == self.player.Direction.RIGHT:
            if 22 <= center_x % self.SQUARE_SIZE <= 28:
                if is_empty_tile(self.level[(center_y + fudge) // self.SQUARE_SIZE][center_x // self.SQUARE_SIZE]):
                    self.turns_allowed[self.player.Direction.DOWN] = True
                if is_empty_tile(self.level[(center_y - fudge) // self.SQUARE_SIZE][center_x // self.SQUARE_SIZE]):
                    self.turns_allowed[self.player.Direction.UP] = True
            if 22 <= center_y % self.SQUARE_SIZE <= 28:
                if is_empty_tile(self.level[center_y // self.SQUARE_SIZE][(center_x - fudge) // self.SQUARE_SIZE]):
                    self.turns_allowed[self.player.Direction.LEFT] = True
                if is_empty_tile(self.level[center_y // self.SQUARE_SIZE][(center_x + fudge) // self.SQUARE_SIZE]):
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
            if self.player.direction_command == i and self.turns_allowed[i]:
                self.player.face(i)

        if self.player.x < 0:
            self.player.x = 0
        elif self.player.x > self.WINDOW_WIDTH - self.SQUARE_SIZE:
            self.player.x = self.WINDOW_WIDTH - self.SQUARE_SIZE

        if self.player.y < 0:
            self.player.y = 0
        elif self.player.y > self.WINDOW_HEIGHT - self.SQUARE_SIZE - self.BOTTOM_PADDING:
            self.player.y = self.WINDOW_HEIGHT - self.SQUARE_SIZE - self.BOTTOM_PADDING

    def paint_player(self, center_x, center_y):
        if 0 < self.player.x < self.WINDOW_WIDTH - self.SQUARE_SIZE:
            current_tile = self.level[center_y // self.SQUARE_SIZE][center_x // self.SQUARE_SIZE]
            if current_tile == Tile.EMPTY.board_index or current_tile == Tile.ENEMY.board_index:
                 self.level[center_y // self.SQUARE_SIZE][center_x // self.SQUARE_SIZE] = Tile.PLAYER.board_index

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

        center_x, center_y = self.player.get_centered_coords()
        self.check_position(center_x, center_y)
        self.move_player()
        self.paint_player(center_x, center_y)

        self.bar.draw(self.screen)
        if self.bar.is_time_over():
            self.display_game_over_screen(self.player.check_player_win(self.level))

        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update_display()
        pygame.quit()