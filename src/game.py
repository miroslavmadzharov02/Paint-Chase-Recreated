import pygame
from src.board import boards
from src.player import Player

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

        self.running = True

    def draw_board(self):
        for row in range(len(self.level)):
            for col in range(len(self.level[row])):
                if self.level[row][col] == 0:
                    pygame.draw.rect(self.screen, 'purple', (col * self.SQUARE_SIZE, row * self.SQUARE_SIZE, self.SQUARE_SIZE, self.SQUARE_SIZE))
                if self.level[row][col] == 1:
                    pygame.draw.rect(self.screen, 'green', (col * self.SQUARE_SIZE, row * self.SQUARE_SIZE, self.SQUARE_SIZE, self.SQUARE_SIZE))


    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.player.direction = Player.Direction.RIGHT
                if event.key == pygame.K_LEFT:
                    self.player.direction = Player.Direction.LEFT
                if event.key == pygame.K_DOWN:
                    self.player.direction = Player.Direction.DOWN
                if event.key == pygame.K_UP:
                    self.player.direction = Player.Direction.UP

    def update_display(self):
        self.timer.tick(self.FPS)
        self.screen.fill('black')
        self.draw_board()
        self.player.draw(self.screen)
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update_display()
        pygame.quit()