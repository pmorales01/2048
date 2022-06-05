import pygame
from .button import Button

ACTION = None

class PopUp:
    def __init__(self, screen, message, position, size=(400, 300)):
        self._screen = screen
        self._message = message
        self._buttons = []
        self._position = position
        self._size = size
        self._color = (191, 228, 252)
        font = pygame.font.Font(None, 50)
        self._text = font.render(message, True, (255, 255, 255))
        self._textpos = self._text.get_rect()
        self._textpos.centerx = self.rect.centerx
        self._textpos.centery = self.rect.centery

    @property
    def rect(self):
        x,y = self._position
        width,height = self._size
        left = x - width // 2
        top = y - height // 2
        return pygame.Rect(left, top, width, height)

    def draw_border(self):
        pygame.draw.rect(self._screen, (0, 0, 0), self.rect, self._size[0] // 100, 10)

    def draw(self):
        pygame.draw.rect(self._screen, self._color, self.rect, self._size[0], 10)
        self._screen.blit(self._text, self._textpos)
        self.draw_border()
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
                print("FROM POPUP: ACTION =", ACTION, "value = ", button.value)
