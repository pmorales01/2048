import pygame
import random
from .tile import Tile

class Board:
    def __init__(self, screen, size):
        self._screen = screen
        self._size = size
        self._default_tiles = [[None for x in range(self._size)] for x in range(self._size)]
        self._tiles = [[None for x in range(self._size)] for x in range(self._size)]
        self._positions = [[None for x in range(self._size)] for x in range(self._size)]

    @property
    def rect(self):
        return pygame.Rect(100, 150, 600, 600)

    def tile_positions(self):
        step = 500 // self._size
        space = 100 // (self._size + 1)
        x_pos = 100
        y_pos = 150 + step

        for j in range(self._size):
            x_pos += step
            for i in range(self._size):
                x_coord = x_pos + space * (j + 1)
                y_coord = y_pos + space * (i + 1)
                self._positions[i][j] = (x_coord, y_coord)
                y_pos += step
            y_pos = 150 + step

    def draw(self):
        pygame.draw.rect(self._screen, (188,172,160), self.rect, 600, 10)

        for i in range(0, self._size):
            for j in range(0, self._size):
                self._default_tiles[i][j].draw(self._screen)

        for i in range(0, self._size):
            for j in range(0, self._size):
                self._tiles[i][j].draw(self._screen)

    def initialize_tiles(self):
        self.tile_positions()
        step = 500 // self._size

        for i in range(0, self._size):
            for j in range(0, self._size):
                position = self._positions[i][j]
                self._tiles[i][j] = Tile(None, position[0], position[1], self._screen, (204, 193, 180), step)
                self._default_tiles[i][j] = Tile(None, position[0], position[1], self._screen, (204, 193, 180), step)

        # select 2 random tiles to start the game
        tile_1 = self._tiles[random.choice(range(self._size))][random.choice(range(self._size))]
        tile_2 = self._tiles[random.choice(range(self._size))][random.choice(range(self._size))]
        tile_1.update_color((238, 228, 218))
        tile_1.update_value(2, (119, 110, 101))
        tile_2.update_color((238, 228, 218))
        tile_2.update_value(2, (119, 110, 101))

    def has_neighbors(self, tile):
        pass

    def move_right(self):
        for i in range(0, self._size):
            j = 0
            while j + 1 <= self._size - 1 and \
                ((self._tiles[i][j + 1].value == self._tiles[i][j].value) or (self._tiles[i][j + 1].value == None) or self._tiles[i][j].value == None):
                if self._tiles[i][j].value == None:
                    j += 1
                    continue

                current = self._tiles[i][j]
                other = self._tiles[i][j + 1]
                if other.value == None:
                    other_center = self._tiles[i][j + 1].center
                    self._tiles[i][j + 1] = self._tiles[i][j]
                    self._tiles[i][j + 1].update_center(other_center)
                    position = current.center
                    self._tiles[i][j] = Tile(None, position[0], position[1], self._screen, (204, 193, 180), current.width)
                elif other.value == current.value:
                    other.update_value((other.value + current.value), (255, 0, 0))
                    position = current.center
                    self._tiles[i][j] = Tile(None, position[0], position[1], self._screen, (204, 193, 180), current.width)
                j += 1

    def move_left(self):
        print("move left")
        for i in range(self._size):
            for j in range(self._size):
                if (j - 1) >= 0:
                    self._tiles[i][j].move(self._tiles[i][j - 1])

    def move_down(self):
        for i in range(self._size):
            for j in range(self._size):
                if (i + 1) != self._size and (self._tiles[i][j]):
                    self._tiles[i][j].move(self._tiles[i + 1][j])

    def process_events(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            self.move_right()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            self.move_left()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            self.move_down()
