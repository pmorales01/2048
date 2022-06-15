# The file defines the Tile class which is used to make tiles used in 2048.

"""This file contains the Tile class used to make tiles."""

import pygame
import random
import math
from game import game

def font_size(string, width):
    """Returns a font size that will make the string fit within the given
        space/pixels."""
    for i in range(2, len(string)):
        width = width - width * 0.25

    return math.floor(width)

class Tile():
    """Tile class used to create tiles."""
    def __init__(
        self, value, center_x, center_y, screen, color=(210, 180, 140), size=100
    ):
        """Initialize a tile."""
        self._value = value
        self._center = pygame.Vector2(center_x, center_y)
        self._width = size
        self._color = color
        self._screen = screen
        font = pygame.font.Font(None, font_size(str(self._value), self._width))
        self._text_color = (255, 255, 255)
        self._text = font.render(str(self._value), True, self._text_color)
        self._textpos = self._text.get_rect()
        self._textpos.centerx = self.rect.centerx
        self._textpos.centery = self.rect.centery

    @property
    def rect(self):
        """Return the bounding rect."""
        left = self._center[0] - self._width
        top = self._center[1] - self._width
        return pygame.Rect(left, top, self._width, self._width)

    @property
    def center(self):
        """Return the tile's center."""
        return self._center

    @property
    def value(self):
        """Return the tile's value."""
        return self._value

    @property
    def width(self):
        """Return the tile's width."""
        return self._width

    @property
    def color(self):
        """Return the tile's color."""
        return self._color

    @property
    def text_color(self):
        """Return the tile's text's color."""
        return self._text_color

    def draw_border(self):
        """Draw the tile's border."""
        pygame.draw.rect(
            self._screen, (0, 0, 0), self.rect, self._width // 50, 10
        )

    def draw(self, surface):
        """Draw the tile."""
        pygame.draw.rect(surface, self._color, self.rect, self._width, 10)
        if self._value != None:
            surface.blit(self._text, self._textpos)

    def update_value(self, value, color):
        """Update the tile's value."""
        self._value = value
        self.update_text(color)

    def update_text(self, color):
        """Update the tile's text."""
        font = pygame.font.Font(None, font_size(str(self._value), self._width))
        self._text = font.render(str(self._value), True, color)
        self._textpos = self._text.get_rect()
        self._textpos.centerx = self.rect.centerx
        self._textpos.centery = self.rect.centery
        self._text_color = color

    def update_color(self, color):
        """Update the tile's color."""
        self._color = color

    def update_center(self, center):
        """Update the tile's center."""
        self._center = pygame.Vector2(center[0], center[1])
        self._textpos.centerx = self.rect.centerx
        self._textpos.centery = self.rect.centery
