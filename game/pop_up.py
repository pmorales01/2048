# This file defines the PopUp class used to create pop-ups in the game.

"""This file defines the PopUp class."""

import pygame
from .button import Button

class PopUp:
    """Class used to create pop-ups."""
    def __init__(self, screen, message, position, size=(600, 600)):
        """Initialize a pop-up."""
        self._screen = screen
        self._message = message
        self._buttons = []
        self._position = position
        self._size = size
        self._color = (191, 228, 252)
        font = pygame.font.Font(None, 125)
        self._text = font.render(message, True, (99,91,82))
        self._textpos = self._text.get_rect()
        self._textpos.centerx = self.rect.centerx
        self._textpos.centery = self.rect.centery - 65

    @property
    def rect(self):
        """Return the bounding rect."""
        x,y = self._position
        width,height = self._size
        left = x - width // 2
        top = y - height // 2
        return pygame.Rect(left, top, width, height)

    @property
    def buttons(self):
        """Return a list of the pop-up's buttons."""
        return self._buttons

    def draw(self):
        """Draw the pop-up."""
        surface = pygame.Surface(pygame.Rect(self.rect).size, pygame.SRCALPHA)
        pygame.draw.rect(surface, (191, 228, 252, 60), surface.get_rect())
        self._screen.blit(surface, self.rect)
        self._screen.blit(self._text, self._textpos)
        for button in self._buttons:
            button.draw(self._screen)

    def add_button(self, button):
        """Add a button to the pop-up."""
        self._buttons.append(button)

    def process_events(self, event):
        """Process the game events."""
        for button in self._buttons:
            button.process_events(event)
