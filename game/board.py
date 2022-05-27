import pygame
import random
from .tile import Tile

class Board:
    def __init__(self, screen, size):
        self._screen = screen
        self._size = size
        self._tiles = []
        self._positions = []

    @property
    def rect(self):
        return pygame.Rect(100, 150, 600, 600)

    def tile_positions(self):
        step = 500 // self._size
        space = 100 // (self._size + 1)
        x_pos = 100
        y_pos = 150 + step

        for i in range(0, self._size):
            x_pos += step
            for j in range(0, self._size):
                x_coord = x_pos + space * (i + 1)
                y_coord = y_pos + space * (j + 1)
                self._positions.append((x_coord, y_coord))
                y_pos += step

            y_pos = 150 + step

    def draw(self):
        pygame.draw.rect(self._screen, (188,172,160), self.rect, 600, 10)
        for tile in self._tiles:
            tile.draw(self._screen)

    def initialize_tiles(self):
        self.tile_positions()
        step = 500 // self._size
        for position in self._positions:
            self._tiles.append(Tile(0, position[0], position[1], self._screen, (255, 0, 0), step))

    def process_events(self, event):
        print(pygame.mouse.get_pos())
