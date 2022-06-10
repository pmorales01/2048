import pygame

class Button:
    def __init__(self, center, screen, value, text, width=100, height=50, color=(255, 0, 0), border_on=True):
        self._center = center
        self._screen = screen
        self._width = width
        self._height = height
        self._color = color
        self._original_color = color
        self._value = value
        self._border_on = border_on
        font = pygame.font.Font(None, self._height)
        self._text = font.render(text, True, (255, 255, 255))
        self._textpos = self._text.get_rect()
        self._textpos.centerx = self.rect.centerx
        self._textpos.centery = self.rect.centery
        self._pressed = False

    @property
    def rect(self):
        left = self._center[0] - self._width
        top = self._center[1] - self._height
        return pygame.Rect(left, top, self._width, self._height)

    @property
    def value(self):
        return self._value

    @property
    def pressed(self):
        return self._pressed

    def unpress(self):
        self._pressed = False

    def draw_border(self, surface):
        pygame.draw.rect(surface, (0, 0, 0), self.rect, self._width // 50, 10)

    def draw(self, surface):
        pygame.draw.rect(surface, self._color, self.rect, self._width, 10)
        surface.blit(self._text, self._textpos)
        if self._border_on:
            self.draw_border(surface)

    def change_color(self, color):
        self._color = color

    def process_events(self, event):
        point = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(point[0], point[1]):
                self.change_color((106, 238, 39))
            else:
                self.change_color(self._original_color)

        if self.rect.collidepoint(point) and event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed():
                self._pressed = True
