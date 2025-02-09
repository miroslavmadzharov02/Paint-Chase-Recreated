import pygame

class Bar:
    """Class to track elapsed time"""
    def __init__(self, window_height: int, window_width: int, bottom_padding: int) -> None:
        seconds = 15

        self.bar_x = 0
        self.bar_y = window_height - bottom_padding

        self.bar_width = window_width
        self.bar_height = bottom_padding

        self.total_time = seconds * 1000
        self.start_ticks = pygame.time.get_ticks()
        
        self.main_color = 'gray17'
        self.alt_color = 'ghostwhite'

    def draw(self, screen: pygame.Surface) -> None:
        elapsed_time = pygame.time.get_ticks() - self.start_ticks
        progress_ratio = min(elapsed_time / self.total_time, 1)
        progress_width = int(self.bar_width * progress_ratio)

        pygame.draw.rect(screen, self.main_color, (self.bar_x, self.bar_y, self.bar_width, self.bar_height), 5)
        pygame.draw.rect(screen, self.alt_color, (self.bar_x, self.bar_y + 5, progress_width, self.bar_height - 10))

    def is_time_over(self) -> bool:
        elapsed_time = pygame.time.get_ticks() - self.start_ticks
        return elapsed_time >= self.total_time