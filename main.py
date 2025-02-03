from board import boards
import pygame

pygame.init()

BOTTOM_PADDING = 50
WIDTH_TOTAL_TILES = 15
HEIGHT_TOTAL_TILES = 9
SQUARE_SIZE = 50

WINDOW_WIDTH = WIDTH_TOTAL_TILES * SQUARE_SIZE
WINDOW_HEIGHT = HEIGHT_TOTAL_TILES * SQUARE_SIZE + BOTTOM_PADDING
screen = pygame.display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT])

timer = pygame.time.Clock()
FPS = 60

current_level_index = 0
level = boards[current_level_index]

def draw_board():
    for row in range(len(level)):
        for col in range(len(level[row])):
            if level[row][col] == 0:
                pygame.draw.rect(screen, 'purple', (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            if level[row][col] == 1:
                pygame.draw.rect(screen, 'green', (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

run = True
while run:
    timer.tick(FPS)
    screen.fill('black')
    draw_board()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.flip()
pygame.quit()