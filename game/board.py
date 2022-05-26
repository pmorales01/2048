import pygame
from game import tile

class Board:
    def __init__(self, screen, size):
        self._screen = screen
        self._size = size

    @property
    def rect(self):
        return pygame.Rect(100, 150, 600, 600)

    def draw(self):
        pygame.draw.rect(self._screen, (214,185,149), self.rect, 600, 10)
