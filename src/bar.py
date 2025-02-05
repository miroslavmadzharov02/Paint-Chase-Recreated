import pygame

class Bar:
    def __init__(self, WINDOW_HEIGHT, WINDOW_WIDTH, BOTTOM_PADDING):
        SECONDS = 15

        self.bar_x = 0
        self.bar_y = WINDOW_HEIGHT - BOTTOM_PADDING
        self.bar_width = WINDOW_WIDTH
        self.bar_height = BOTTOM_PADDING
        self.total_time = SECONDS * 1000
        self.start_ticks = pygame.time.get_ticks()
        self.main_color = 'gray17'
        self.alt_color = 'ghostwhite'

    def draw(self, screen):
        elapsed_time = pygame.time.get_ticks() - self.start_ticks
        progress_ratio = min(elapsed_time / self.total_time, 1)
        progress_width = int(self.bar_width * progress_ratio)

        pygame.draw.rect(screen, self.main_color, (self.bar_x, self.bar_y, self.bar_width, self.bar_height), 5)
        pygame.draw.rect(screen, self.alt_color, (self.bar_x, self.bar_y + 5, progress_width, self.bar_height - 10))

    def is_time_over(self):
        elapsed_time = pygame.time.get_ticks() - self.start_ticks
        return elapsed_time >= self.total_time