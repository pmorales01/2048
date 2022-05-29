import pygame
import random
import math
from game import game

def font_size(string, width):
    for i in range(2, len(string)):
        width = width - width * 0.25

    return math.floor(width)

class Tile():
    def __init__(self, value, center_x, center_y, screen, color=(210, 180, 140), size=100):
        self._value = value
        self._center = pygame.Vector2(center_x, center_y)
        self._width = size
        self._color = color
        self._screen = screen
        font = pygame.font.Font(None, font_size(str(self._value), self._width))
        self._text = font.render(str(self._value), True, (255, 255, 255))
        self._textpos = self._text.get_rect()
        self._textpos.centerx = self.rect.centerx
        self._textpos.centery = self.rect.centery

    @property
    def rect(self):
        left = self._center[0] - self._width
        top = self._center[1] - self._width
        return pygame.Rect(left, top, self._width, self._width)

    @property
    def center(self):
        return self._center

    @property
    def value(self):
        return self._value

    @property
    def width(self):
        return self._width

    def draw_border(self):
        pygame.draw.rect(self._screen, (0, 0, 0), self.rect, self._width // 50, 10)

    def draw(self, surface):
        pygame.draw.rect(surface, self._color, self.rect, self._width, 10)
        if self._value != None:
            surface.blit(self._text, self._textpos)

    def update_value(self, value, color):
        self._value = value
        self.update_text(color)

    def update_text(self, color):
        font = pygame.font.Font(None, font_size(str(self._value), self._width))
        self._text = font.render(str(self._value), True, color)
        self._textpos = self._text.get_rect()
        self._textpos.centerx = self.rect.centerx
        self._textpos.centery = self.rect.centery

    def update_color(self, color):
        self._color = color

    def update_center(self, center):
        self._center = pygame.Vector2(center[0], center[1])
        self._textpos.centerx = self.rect.centerx
        self._textpos.centery = self.rect.centery

    def move(self, other_tile):
        self._center = other_tile.center
        self._textpos.centerx = other_tile.rect.centerx
        self._textpos.centery = other_tile.rect.centery

    def __repr__(self):
        return f'center: {self._center}'
