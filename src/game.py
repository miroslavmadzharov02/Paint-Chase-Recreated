"""pygame module"""
import pygame
from src.player import Player
from src.bar import Bar
from src.level import Level

WIN_SVG_PATH = "assets/win.svg"
LOSE_SVG_PATH = "assets/lose.svg"

class Game:
    """Game class"""
    FPS = 60

    def __init__(self, level_index, multiplayer=False):
        pygame.init()

        self.level = Level(level_index)

        self.bottom_padding = self.level.square_size
        self.window_width = self.level.cols_count * self.level.square_size
        self.window_height = self.level.rows_count * self.level.square_size + self.bottom_padding

        self.screen = pygame.display.set_mode([self.window_width, self.window_height])
        self.timer = pygame.time.Clock()

        self.board = self.level.board

        self.multiplayer = multiplayer
        player_starting_coords = (0, 0)
        self.player = Player(self.level.square_size, *player_starting_coords)
        player2_starting_coords = (self.level.square_size, 0)
        self.player2 = Player(self.level.square_size, *player2_starting_coords) if multiplayer else None

        self.enemies = self.level.get_enemies()

        self.bar = Bar(self.window_height, self.window_width, self.bottom_padding)

        self.win_image = pygame.transform.scale(pygame.image.load(WIN_SVG_PATH), (self.level.square_size * 10, self.level.square_size * 10))
        self.lose_image = pygame.transform.scale(pygame.image.load(LOSE_SVG_PATH), (self.level.square_size * 10, self.level.square_size * 10))

        self.running = True

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

                if self.multiplayer:
                    if event.key == pygame.K_d:
                        self.player2.set_command(Player.Direction.RIGHT)
                    if event.key == pygame.K_a:
                        self.player2.set_command(Player.Direction.LEFT)
                    if event.key == pygame.K_s:
                        self.player2.set_command(Player.Direction.DOWN)
                    if event.key == pygame.K_w:
                        self.player2.set_command(Player.Direction.UP)

        for player in [self.player, self.player2] if self.multiplayer else [self.player]:
            for i in range(len(player.Direction)):
                if player.direction_command == i and player.turns_allowed[i]:
                    player.face(i)

    def display_game_over_screen(self, player_won):
        image = self.win_image if player_won else self.lose_image

        while True:
            self.screen.fill("black")
            self.screen.blit(image, (0, 0))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                        return

    def get_enemy_from_collision(self, player):
        player_rect = player.get_rect()
        for enemy in self.enemies:
            if player_rect.colliderect(enemy.get_rect()):
                return enemy
        return None

    def player_logic(self, player):
        player.draw(self.screen)

        center_x, center_y = player.get_centered_coords()
        player.check_position(self.board, center_x, center_y)
        player.move()
        player.interact_tile(self.board, center_x, center_y, self.window_width)

        player.check_boost_time()

    def enemy_logic(self):
        for enemy in self.enemies:
            if not enemy.dead:
                enemy.draw(self.screen)
                center_x_enemy, center_y_enemy = enemy.get_centered_coords()
                enemy.move(self.board, center_x_enemy, center_y_enemy)
                enemy.interact_tile(self.board, center_x_enemy, center_y_enemy, self.window_width)
            else:
                if pygame.time.get_ticks() >= enemy.respawn_time:
                    enemy.respawn(self.board)

        for player in [self.player, self.player2] if self.multiplayer else [self.player]:
            collision_enemy = self.get_enemy_from_collision(player)
            if collision_enemy:
                collision_enemy.die()

    def update_display(self):
        self.timer.tick(self.FPS)
        self.screen.fill('black')
        self.level.draw(self.screen)

        self.player_logic(self.player)
        if self.multiplayer:
            self.player_logic(self.player2)
        self.enemy_logic()
       
        self.bar.draw(self.screen)
        if self.bar.is_time_over():
            self.display_game_over_screen(self.player.check_player_win(self.board))

        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update_display()
        pygame.quit()