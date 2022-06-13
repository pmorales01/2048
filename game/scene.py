# This file contains the scenes to run 2048.

"""Scene objects that make up the Title Screen and Game for 2048."""

import pygame, sys, os
from .button import Button
from pygame.locals import *
from .tile import Tile
from .board import Board

BOARD_SIZE = None

class Scene:
    """Parent class for creating scenes."""
    def __init__(self, screen, background_color):
        """Initialize a Scene"""
        self._screen = screen
        self._background = pygame.Surface(self._screen.get_size())
        self._background.fill(background_color)
        self._background.flip()
        self._frame_rate = 60

    def draw(self):
        """Draw the scene"""
        self._screen.blit(self._screen, (0, 0))

    def process_events(self, event):
        """Process a game event using the scene."""
        if event.type == pygame.QUIT:
            sys.exit(0)

class TitleScene(Scene):
    def __init__(self, screen, background_color):
        """Initialize the scene that runs the Title Screen."""
        self._frame_rate = 60
        self._screen = screen
        self._background_color = background_color
        self._scene_is_running = True
        self._tiles = []
        self._buttons = [Button((450, 400), self._screen, 4, "4 x 4"),
            Button((450, 500), self._screen, 5, "5 x 5"),
            Button((450, 600), self._screen, 6, "6 x 6")]

    def start_scene(self):
        """Start the scene."""
        self._screen.fill(self._background_color)
        self._tiles.append(Tile(2, 225, 200, self._screen, (50,205,50)))
        self._tiles.append(Tile(0, 375, 200, self._screen, (255,8,0)))
        self._tiles.append(Tile(4, 525, 200, self._screen, (50,205,50)))
        self._tiles.append(Tile(8, 675, 200, self._screen, (255,8,0)))

    def draw(self):
        """Draw the scene."""
        super().draw()
        for tile in self._tiles:
            tile.draw(self._screen)
            tile.draw_border()

        for button in self._buttons:
            button.draw(self._screen)

    @property
    def scene_is_running(self):
        """Return if the scene is running."""
        return self._scene_is_running

    def process_events(self, event):
        """Process a game event using the scene."""
        super().process_events(event)
        for button in self._buttons:
            button.process_events(event)
            if button.pressed:
                self._scene_is_running = False
                global BOARD_SIZE
                BOARD_SIZE = button.value

class VideoGameScene(Scene):
    def __init__(self, screen):
        """Initialize the scene that runs the Game."""
        self._board_size = BOARD_SIZE
        self._screen = screen
        self._scene_is_running = True
        self._board = None

    @property
    def scene_is_running(self):
        """Return if the scene is running."""
        return self._scene_is_running

    def start_scene(self):
        """Start the scene."""
        self._board_size = BOARD_SIZE
        self._board = Board(self._screen, self._board_size)
        self._screen.fill((250, 221, 185))
        self._board_size = BOARD_SIZE
        self._board.initialize_tiles()

    def draw(self):
        """Draw the game board."""
        self._board.draw()

    def process_events(self, event):
        """Process a game event."""
        super().process_events(event)
        self._board.process_events(event)
        if self._board.exit_game:
            self._scene_is_running = False
