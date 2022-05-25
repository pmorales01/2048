import pygame, sys, os
from pygame.locals import *
from .tile import Tile

class Scene:
    def __init__(self, screen, background_color):
        """Initialize a Scene"""
        self._screen = screen
        self._background = pygame.Surface(self._screen.get_size())
        self._background.fill(background_color)
        self._background.flip()
        self._frame_rate = 60

    def draw(self):
        self._screen.blit(self._screen, (0, 0))

    def input_event(self, event):
        if event.type == pygame.QUIT:
            print("Bye!")
            sys.exit(0)

class TitleScene(Scene):
    def __init__(self, screen, background_color):
        self._frame_rate = 60
        self._screen = screen
        self._scene_is_running = True
        self._tiles = []
        screen.fill(background_color)

    def draw(self):
        super().draw()
        self._tiles.append(Tile(2, 200, 200, self._screen))
        self._tiles.append(Tile(0, 350, 200, self._screen))
        self._tiles.append(Tile(4, 500, 200, self._screen))
        self._tiles.append(Tile(8, 650, 200, self._screen))

        clock = pygame.time.Clock()
        clock.tick(4)

        for tile in self._tiles:
            tile.rand_color()
            tile.draw(self._screen)
            tile.draw_border()

    @property
    def scene_is_running(self):
        return self._scene_is_running
