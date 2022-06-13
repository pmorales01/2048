#!/usr/bin/env python3
#
# The file creates and runs an instance of 2048.

"""The file imports a Game object and executes main."""

import pygame, sys,os
from pygame.locals import *
from game.game import Game

if __name__ == "__main__":
    GAME = Game()
    GAME.create_scenes()
    GAME.run()
