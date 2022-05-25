import pygame, sys, os
from pygame.locals import *

from game.scene import (
    TitleScene
)

TILE_SIZE = 100

class Game:
    def __init__(self,
    height=800,
    width=800,
    window_title="2048"):

        pygame.init()
        self._window_size = (width, height)
        self._clock = pygame.time.Clock()
        self._screen = pygame.display.set_mode(self._window_size)
        pygame.display.set_caption(window_title)
        self._scenes = []

    def create_scenes(self):
        self._scenes = [TitleScene(self._screen, (64, 128, 237))]

    def run(self):
        for scene in self._scenes:
            while scene.scene_is_running:
                for event in pygame.event.get():
                    scene.input_event(event)
                scene.draw()
                pygame.display.update()
