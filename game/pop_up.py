import pygame
from .button import Button

ACTION = None

class PopUp:
    def __init__(self, screen, message, position, size=(600, 600)):
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
        x,y = self._position
        width,height = self._size
        left = x - width // 2
        top = y - height // 2
        return pygame.Rect(left, top, width, height)

    def draw(self):
        surface = pygame.Surface(pygame.Rect(self.rect).size, pygame.SRCALPHA)
        pygame.draw.rect(surface, (191, 228, 252, 60), surface.get_rect())
        self._screen.blit(surface, self.rect)
        self._screen.blit(self._text, self._textpos)
        for button in self._buttons:
            button.draw(self._screen)

    def add_button(self, button):
        self._buttons.append(button)

    def process_events(self, event):
        for button in self._buttons:
            button.process_events(event)
            if button.pressed:
                global ACTION
                ACTION = button.value
                button.unpress()
