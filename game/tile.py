import pygame
import random
import math
from game import game

def color():
    return (210, 180, 140)

def font_size(string, width):
    for i in range(2, len(string)):
        width = width - width * 0.25

    return math.floor(width)

class Tile():
    def __init__(self, value, center_x, center_y, screen):
        self._value = value
        self._center = pygame.Vector2(center_x, center_y)
        self._width = game.TILE_SIZE
        self._color = color()
        self._screen = screen
        font = pygame.font.Font(None, font_size(str(value), self._width))
        self._text = font.render(str(value), True, (255, 255, 255))
        self._textpos = self._text.get_rect()
        self._textpos.centerx = self.rect.centerx
        self._textpos.centery = self.rect.centery

    @property
    def rect(self):
        left = self._center[0] - game.TILE_SIZE
        top = self._center[1] - game.TILE_SIZE
        return pygame.Rect(left, top, self._width, self._width)

    def draw_border(self):
        pygame.draw.rect(self._screen, (0, 0, 0), self.rect, self._width // 50, 10)

    def draw(self, surface):
        pygame.draw.rect(surface, self._color, self.rect, self._width, 10)
        surface.blit(self._text, self._textpos)

    def rand_color(self):
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        rgb = (r, g, b)
        self._color = rgb
