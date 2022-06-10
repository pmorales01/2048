import pygame
import random
from .tile import Tile, font_size
from .colors import COLORS
from .pop_up import PopUp
import game.pop_up as popup
from .button import Button

# counts the number of available moves
RIGHT_AVAILABLE = 0
LEFT_AVAILABLE = 0
DOWN_AVAILABLE = 0
UP_AVAILABLE = 0

class Board:
    def __init__(self, screen, size):
        self._screen = screen
        self._size = size
        self._tiles = [[None for x in range(self._size)] for x in range(self._size)]
        self._positions = [[None for x in range(self._size)] for x in range(self._size)]
        self._popup = PopUp(self._screen, "GAME OVER", (400, 400))
        self._popup.add_button(Button((350, 525), self._screen, "quit", "Quit"))
        self._popup.add_button(Button((550, 525), self._screen, "retry", "Retry"))
        self._game_is_over = False
        self._exit_game = False
        self._score = 0
        font = pygame.font.Font(None, font_size(str(self._score), 50))
        self._text_color = (255, 255, 255)
        self._text = font.render(str(self._score), True, self._text_color)
        self._textpos = self._text.get_rect()
        self._textpos.centerx = self.score_rect.centerx
        self._textpos.centery = self.score_rect.centery + 10
        self._new_game = Button((675, 140), self._screen, None, "New", color=(124,103,83), border_on=False)

    @property
    def rect(self):
        return pygame.Rect(100, 150, 600, 600)

    @property
    def score_rect(self):
        return pygame.Rect(575, 25, 100, 50)

    def tile_positions(self):
        step = 500 // self._size
        space = 100 // (self._size + 1)
        x_pos = 100
        y_pos = 150 + step

        for j in range(self._size):
            x_pos += step
            for i in range(self._size):
                x_coord = x_pos + space * (j + 1)
                y_coord = y_pos + space * (i + 1)
                self._positions[i][j] = (x_coord, y_coord)
                y_pos += step
            y_pos = 150 + step

    def draw_score(self):
        font = pygame.font.Font(None, 25)
        text = font.render("SCORE", True, self._text_color)
        textpos = text.get_rect()
        textpos.centerx = self.score_rect.centerx
        textpos.centery = self.score_rect.centery - 15
        pygame.draw.rect(self._screen, (188,172,160), self.score_rect, 100, 15)
        self._screen.blit(self._text, self._textpos)
        self._screen.blit(text, textpos)

    def update_score(self):
        font = pygame.font.Font(None, font_size(str(self._score), 50))
        self._text = font.render(str(self._score), True, (255, 255, 255))
        self._textpos = self._text.get_rect()
        self._textpos.centerx = self.score_rect.centerx
        self._textpos.centery = self.score_rect.centery + 10

    def draw(self):
        self._screen.fill((250, 221, 185))
        pygame.draw.rect(self._screen, (188,172,160), self.rect, 600, 10)

        for i in range(0, self._size):
            for j in range(0, self._size):
                self._tiles[i][j].draw(self._screen)

        self.draw_score()

        self._new_game.draw(self._screen)

        if self._game_is_over:
            self._popup.draw()

    def initialize_tiles(self):
        self.tile_positions()
        step = 500 // self._size

        for i in range(0, self._size):
            for j in range(0, self._size):
                position = self._positions[i][j]
                self._tiles[i][j] = Tile(None, position[0], position[1], self._screen, (204, 193, 180), step)

        # select 2 random tiles to start the game
        tile_1 = self._tiles[random.choice(range(self._size))][random.choice(range(self._size))]
        tile_2 = self._tiles[random.choice(range(self._size))][random.choice(range(self._size))]

        while tile_1.center == tile_2.center:
            print("we are the same")
            tile_1 = self._tiles[random.choice(range(self._size))][random.choice(range(self._size))]
            tile_2 = self._tiles[random.choice(range(self._size))][random.choice(range(self._size))]

        tile_1.update_color((238, 228, 218))
        tile_1.update_value(2, (119, 110, 101))
        tile_2.update_color((238, 228, 218))
        tile_2.update_value(2, (119, 110, 101))

    def next_tile_is_none(self, current_cord, other_cord, execute_move):
        if not execute_move:
            return

        i,j = current_cord
        current = self._tiles[i][j]

        x,y = other_cord
        other = self._tiles[x][y]

        other_center = other.center

        self._tiles[x][y].update_value(current.value, current.text_color)
        self._tiles[x][y].update_center(other_center)
        self._tiles[x][y].update_color(current.color)

        x,y = current.center

        self._tiles[i][j] = Tile(None, x, y, self._screen, (204, 193, 180), current.width)

    def calculate_n(self, number):
        n = 0
        while number != 1:
            n += 1
            number = number // 2

        return n

    def combine_tiles(self, current_cord, other_cord, execute_move):
        if not execute_move:
            return

        i,j = current_cord
        current = self._tiles[i][j]

        x,y = other_cord
        other = self._tiles[x][y]

        n = self.calculate_n(other.value + current.value) - 2

        if n >= len(COLORS):
            n = len(COLORS) - 1

        self._score += other.value + current.value
        self.update_score()
        color_pair = COLORS[n]
        other.update_value((other.value + current.value), color_pair[1])
        other.update_color(color_pair[0])
        x,y = current.center
        self._tiles[i][j] = Tile(None, x, y, self._screen, (204, 193, 180), current.width)

    def move_right(self, execute_move=True):
        global RIGHT_AVAILABLE
        RIGHT_AVAILABLE = 0
        for i in range(0, self._size):
            for k in range(0, self._size):
                for j in range(0, self._size - 1):
                    if j + 1 <= self._size - 1:
                        if self._tiles[i][j + 1].value == self._tiles[i][j].value:
                            if self._tiles[i][j].value != None:
                                self.combine_tiles((i, j), (i, j + 1), execute_move)
                                RIGHT_AVAILABLE += 1
                        elif self._tiles[i][j + 1].value == None:
                            self.next_tile_is_none((i, j), (i, j + 1), execute_move)
                            RIGHT_AVAILABLE += 1


    def move_left(self, execute_move=True):
        global LEFT_AVAILABLE
        LEFT_AVAILABLE = 0
        for i in range(0, self._size):
            for k in range(0, self._size):
                for j in range(self._size - 1, 0, -1):
                    if j - 1 >= 0:
                        if self._tiles[i][j - 1].value == self._tiles[i][j].value:
                            if self._tiles[i][j].value != None:
                                self.combine_tiles((i, j), (i, j - 1), execute_move)
                                LEFT_AVAILABLE += 1
                        elif self._tiles[i][j - 1].value == None:
                            self.next_tile_is_none((i, j), (i, j - 1), execute_move)
                            LEFT_AVAILABLE += 1

    def move_down(self, execute_move=True):
        global DOWN_AVAILABLE
        DOWN_AVAILABLE = 0
        for j in range(0, self._size):
            for k in range(0, self._size):
                for i in range(0, self._size - 1):
                    if i + 1 <= self._size:
                        if self._tiles[i + 1][j].value == self._tiles[i][j].value:
                            if self._tiles[i][j].value != None:
                                self.combine_tiles((i, j), (i + 1, j), execute_move)
                                DOWN_AVAILABLE += 1
                        elif self._tiles[i + 1][j].value == None:
                            self.next_tile_is_none((i, j), (i + 1, j), execute_move)
                            DOWN_AVAILABLE += 1

    def move_up(self, execute_move=True):
        global UP_AVAILABLE
        UP_AVAILABLE = 0
        for j in range(0, self._size):
            for k in range(0, self._size):
                for i in range(self._size - 1, 0, -1):
                    if i - 1 >= 0:
                        if self._tiles[i - 1][j].value == self._tiles[i][j].value:
                            if self._tiles[i][j].value != None:
                                self.combine_tiles((i, j), (i - 1, j), execute_move)
                                UP_AVAILABLE += 1
                        elif self._tiles[i - 1][j].value == None:
                            self.next_tile_is_none((i, j), (i - 1, j), execute_move)
                            UP_AVAILABLE += 1

    def check_available_moves(self):
        self.move_right(False)
        self.move_left(False)
        self.move_down(False)
        self.move_up(False)

    def add_random_tile(self):
        empty_tiles = []
        for i in range(0, self._size):
            for j in range(0, self._size):
                if self._tiles[i][j].value == None:
                    empty_tiles.append((i, j))

        if len(empty_tiles) != 0:
            coord = random.choice(empty_tiles)

            i,j = coord

            self._tiles[i][j].update_color((238, 228, 218))
            self._tiles[i][j].update_value(2, (119, 110, 101))

        if len(empty_tiles) <= 1:
            print("board is full")
            self.check_available_moves()
            if RIGHT_AVAILABLE == 0 and LEFT_AVAILABLE == 0 and \
                UP_AVAILABLE == 0 and DOWN_AVAILABLE == 0:
                print("Game Over")
                self._game_is_over = True

    @property
    def exit_game(self):
        return self._exit_game

    def process_events(self, event):
        self._new_game.process_events(event)
        if self._new_game.pressed:
            self.initialize_tiles()
            self._score = 0
            self.update_score()
            self._new_game.unpress()
            return
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            self.move_right()
            if RIGHT_AVAILABLE != 0:
                self.add_random_tile()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            self.move_left()
            if LEFT_AVAILABLE != 0:
                self.add_random_tile()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            self.move_down()
            if DOWN_AVAILABLE != 0:
                self.add_random_tile()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            self.move_up()
            if UP_AVAILABLE != 0:
                self.add_random_tile()

        if self._game_is_over:
            self._popup.process_events(event)
            if popup.ACTION == "quit":
                self._exit_game = True
            elif popup.ACTION == "retry":
                self.initialize_tiles()
                self._game_is_over = False
                self._exit_game = False
                self._score = 0
                self.update_score()
                popup.ACTION = None
