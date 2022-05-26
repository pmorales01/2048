import pygame, sys, os
from .button import Button
from pygame.locals import *
from .tile import Tile

BOARD_SIZE = None

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

    def process_events(self, event):
        if event.type == pygame.QUIT:
            print("Bye!")
            sys.exit(0)

class TitleScene(Scene):
    def __init__(self, screen, background_color):
        self._frame_rate = 60
        self._screen = screen
        self._background_color = background_color
        self._scene_is_running = True
        self._tiles = []
        self._buttons = [Button((450, 400), self._screen, "4 x 4"),
            Button((450, 500), self._screen, "5 x 5"),
            Button((450, 600), self._screen, "6 x 6")]

    def start_scene(self):
        self._screen.fill(self._background_color)
        self._tiles.append(Tile(2, 200, 200, self._screen))
        self._tiles.append(Tile(0, 350, 200, self._screen))
        self._tiles.append(Tile(4, 500, 200, self._screen))
        self._tiles.append(Tile(8, 650, 200, self._screen))

    def draw(self):
        super().draw()
        for tile in self._tiles:
            tile.rand_color()
            tile.draw(self._screen)
            tile.draw_border()

        for button in self._buttons:
            button.draw(self._screen)

    @property
    def scene_is_running(self):
        return self._scene_is_running

    @property
    def choice(self):
        return self._choice

    def process_events(self, event):
        super().process_events(event)
        for i in range (0, len(self._buttons)):
            self._buttons[i].process_events(event)
            if self._buttons[i].pressed:
                self._scene_is_running = False
                global BOARD_SIZE
                BOARD_SIZE = i + 4

class VideoGameScene(Scene):
    def __init__(self, screen):
        self._board_size = BOARD_SIZE
        self._screen = screen
        self._scene_is_running = True

    @property
    def scene_is_running(self):
        return self._scene_is_running

    def start_scene(self):
        self._screen.fill((251, 248, 239))
        self._board_size = BOARD_SIZE
