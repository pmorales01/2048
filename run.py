#!/usr/bin/env python3

import pygame, sys,os
from pygame.locals import *
from game.game import Game

if __name__ == "__main__":
    GAME = Game()
    GAME.create_scenes()
    GAME.run()
