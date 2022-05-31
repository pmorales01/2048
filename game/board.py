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
        # tile_1 = self._tiles[random.choice(range(self._size))][random.choice(range(self._size))]
        # tile_2 = self._tiles[random.choice(range(self._size))][random.choice(range(self._size))]
        # tile_1.update_color((238, 228, 218))
        # tile_1.update_value(2, (119, 110, 101))
        # tile_2.update_color((238, 228, 218))
        # tile_2.update_value(2, (119, 110, 101))

        tile_1 = self._tiles[1][3]
        tile_2 = self._tiles[1][2]
        tile_1.update_color((238, 228, 218))
        tile_1.update_value(2, (119, 110, 101))
        tile_2.update_color((238, 228, 218))
        tile_2.update_value(2, (119, 110, 101))
        tile_3 = self._tiles[1][0]
        tile_3.update_color((238, 228, 218))
        tile_3.update_value(8, (119, 110, 101))

    def no_adjacent_tile(self, tile_a, tile_b):
        i,j = tile_a
        current_tile = self._tiles[i][j]

        x,y = tile_b
        other_tile = self._tiles[x][y]

        other_center = self._tiles[x][y].center
        self._tiles[x][y] = self._tiles[i][j]
        self._tiles[x][y].update_center(other_center)
        x,y = current_tile.center
        self._tiles[i][j] = Tile(None, x,y, self._screen, (204, 193, 180), current_tile.width)

    def combine_tiles(self, tile_a, tile_b):
        i,j = tile_a
        current = self._tiles[i][j]

        x,y = tile_b
        other = self._tiles[x][y]

        other.update_value((other.value + current.value), (255, 0, 0))
        x,y = current.center
        self._tiles[i][j] = Tile(None, x, y, self._screen, (204, 193, 180), current.width)

    def move_right(self):
        for i in range(0, self._size):
            for k in range(0, self._size):
                for j in range(0, self._size - 1):
                    if j + 1 <= self._size:
                        if self._tiles[i][j + 1].value == self._tiles[i][j].value:
                            if self._tiles[i][j].value != None:
                                self.combine_tiles((i, j), (i, j + 1))
                        elif self._tiles[i][j + 1].value == None:
                            self.no_adjacent_tile((i, j), (i, j + 1))

    def move_left(self):
        print("move left")
        for i in range(0, self._size):
            for k in range(0, self._size):
                for j in range(self._size - 1, 0, -1):
                    if j - 1 >= 0:
                        if self._tiles[i][j - 1].value == self._tiles[i][j].value:
                            if self._tiles[i][j].value != None:
                                self.combine_tiles((i, j), (i, j - 1))
                        elif self._tiles[i][j - 1].value == None:
                            self.no_adjacent_tile((i, j), (i, j - 1))

    def move_down(self):
        for j in range(0, self._size):
            for k in range(0, self._size):
                for i in range(0, self._size - 1):
                    if i + 1 <= self._size:
                        if self._tiles[i + 1][j].value == self._tiles[i][j].value:
                            if self._tiles[i][j].value != None:
                                self.combine_tiles((i, j), (i + 1, j))
                        elif self._tiles[i + 1][j].value == None:
                            self.no_adjacent_tile((i, j), (i + 1, j))

    def move_up(self):
        for j in range(0, self._size):
            for k in range(0, self._size):
                for i in range(self._size - 1, -1, -1):
                    if i - 1 >= 0:
                        if self._tiles[i - 1][j].value == self._tiles[i][j].value:
                            if self._tiles[i][j].value != None:
                                self.combine_tiles((i, j), (i - 1, j))
                        elif self._tiles[i - 1][j].value == None:
                            self.no_adjacent_tile((i, j), (i - 1, j))

    def process_events(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            self.move_right()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            self.move_left()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            self.move_down()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            self.move_up()
