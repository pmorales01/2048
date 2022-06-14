# This file defines the Board class to create and run the game for 2048.

"""This file defines the Board class."""

import pygame
import random
from .tile import Tile, font_size
from .colors import COLORS
from .pop_up import PopUp
from .button import Button

# counts the number of available moves a player can make
RIGHT_AVAILABLE = 0
LEFT_AVAILABLE = 0
DOWN_AVAILABLE = 0
UP_AVAILABLE = 0

class Board:
    """Class used to create the game board."""
    def __init__(self, screen, size):
        """Initialize a board."""
        self._screen = screen
        self._size = size
        self._tiles = [
            [None for x in range(self._size)] for x in range(self._size)
        ]
        self._positions = [
            [None for x in range(self._size)] for x in range(self._size)
        ]
        self._popup = PopUp(self._screen, "GAME OVER", (400, 450))
        self._popup.add_button(
            Button((350, 575), self._screen, "quit", "Quit")
        )
        self._popup.add_button(
            Button((550, 575), self._screen, "retry", "Retry")
        )
        self._game_is_over = False
        self._exit_game = False
        self._score = 0
        font = pygame.font.Font(None, font_size(str(self._score), 50))
        self._text_color = (255, 255, 255)
        self._text = font.render(str(self._score), True, self._text_color)
        self._textpos = self._text.get_rect()
        self._textpos.centerx = self.score_rect.centerx
        self._textpos.centery = self.score_rect.centery + 10
        self._new_game = Button(
            (675, 140), self._screen, None, "New", color=(124,103,83), border_on=False
        )

    @property
    def rect(self):
        """Return the bounding rect."""
        return pygame.Rect(100, 150, 600, 600)

    @property
    def score_rect(self):
        """Return the score board's bounding rect."""
        return pygame.Rect(575, 25, 100, 50)

    def tile_positions(self):
        """Initialize the position of each tile on the board."""
        # How far apart each tile on the board should be
        step = 500 // self._size

        # Amount of space between each tile
        space = 100 // (self._size + 1)

        # Current x,y position of the tile
        x_pos = 100
        y_pos = 150 + step

        # Create a n x n list of (x, y) positions
        for j in range(self._size):
            x_pos += step
            for i in range(self._size):
                x_coord = x_pos + space * (j + 1)
                y_coord = y_pos + space * (i + 1)
                self._positions[i][j] = (x_coord, y_coord)
                y_pos += step
            y_pos = 150 + step

    def draw_title(self):
        """Draw the title '2048'."""
        font = pygame.font.Font(None, 150)
        text = font.render("2048", True, (124,103,83))
        textpos = text.get_rect()
        textpos.centerx = 250
        textpos.centery = 85
        self._screen.blit(text, textpos)

    def draw_score(self):
        """Draw the current player's score."""
        font = pygame.font.Font(None, 25)
        text = font.render("SCORE", True, self._text_color)
        textpos = text.get_rect()
        textpos.centerx = self.score_rect.centerx
        textpos.centery = self.score_rect.centery - 15
        pygame.draw.rect(self._screen, (188,172,160), self.score_rect, 100, 15)
        self._screen.blit(self._text, self._textpos)
        self._screen.blit(text, textpos)

    def update_score(self):
        """Update the player's score."""
        font = pygame.font.Font(None, font_size(str(self._score), 50))
        self._text = font.render(str(self._score), True, (255, 255, 255))
        self._textpos = self._text.get_rect()
        self._textpos.centerx = self.score_rect.centerx
        self._textpos.centery = self.score_rect.centery + 10

    def draw(self):
        """Draw the game board and tiles."""
        self._screen.fill((250, 221, 185))
        pygame.draw.rect(self._screen, (188,172,160), self.rect, 600, 10)

        # Draw each tile on the game board
        for i in range(0, self._size):
            for j in range(0, self._size):
                self._tiles[i][j].draw(self._screen)

        # Draw the current game score, 2048 Title, and New Game button
        self.draw_score()
        self.draw_title()
        self._new_game.draw(self._screen)

        # If the game is over, draw a Game Over Pop-Up
        if self._game_is_over:
            self._popup.draw()

    def initialize_tiles(self):
        """Create the tiles that will be used in the game."""
        # Initialize a n x n list of positions where the tiles will go
        self.tile_positions()

        # Size of each tile
        tile_size = 500 // self._size

        # Initialize an n x n list of Tiles
        for i in range(0, self._size):
            for j in range(0, self._size):
                position = self._positions[i][j]
                self._tiles[i][j] = Tile(
                    None, position[0], position[1], self._screen, (204, 193, 180), tile_size
                )

        # Select 2 random tiles to start the game
        tile_1 = self._tiles[
            random.choice(range(self._size))][random.choice(range(self._size))
        ]
        tile_2 = self._tiles[
            random.choice(range(self._size))][random.choice(range(self._size))
        ]

        # If the 2 random tiles are the same, select 2 new tiles
        while tile_1.center == tile_2.center:
            tile_1 = self._tiles[
                random.choice(range(self._size))][random.choice(range(self._size))
            ]
            tile_2 = self._tiles[
                random.choice(range(self._size))][random.choice(range(self._size))
            ]

        # Update the color and value of the 2 selected tiles
        tile_1.update_color((238, 228, 218))
        tile_1.update_value(2, (119, 110, 101))
        tile_2.update_color((238, 228, 218))
        tile_2.update_value(2, (119, 110, 101))

    def next_tile_is_none(self, current_cord, other_cord, execute_move):
        """Swaps the current tile with the other tile whose value is None."""

        # execute_move is false, return and do not swap the tiles
        if not execute_move:
            return

        i,j = current_cord
        current = self._tiles[i][j]

        x,y = other_cord
        other = self._tiles[x][y]

        other_center = other.center

        # Update the value, color, and center of the other Tile
        self._tiles[x][y].update_value(current.value, current.text_color)
        self._tiles[x][y].update_center(other_center)
        self._tiles[x][y].update_color(current.color)

        x,y = current.center

        # Update the current tile to have a value of None
        self._tiles[i][j] = Tile(
            None, x, y, self._screen, (204, 193, 180), current.width
        )

    def calculate_n(self, number):
        """Return the value of n = log of x to base 2."""
        n = 0
        while number != 1:
            n += 1
            number = number // 2

        return n

    def combine_tiles(self, current_cord, other_cord, execute_move):
        """Combine tiles if both tiles have the same value."""

        # execute_move is false, return and do not combine the tiles
        if not execute_move:
            return

        i,j = current_cord
        current = self._tiles[i][j]

        x,y = other_cord
        other = self._tiles[x][y]

        # n = log of x to base 2
        n = self.calculate_n(other.value + current.value) - 2

        if n >= len(COLORS):
            n = n % len(COLORS)

        # Update the player's score
        self._score += other.value + current.value

        self.update_score()

        # Update the other Tile's value and color to represent 2 tiles
        # combining. The new value should be the sum of the 2 tiles.
        # The new color is a color at the nth index of COLORS (list of RGB pairs)
        color_pair = COLORS[n]
        other.update_value((other.value + current.value), color_pair[1])
        other.update_color(color_pair[0])

        # Set the current tile's value to be None
        x,y = current.center
        self._tiles[i][j] = Tile(
            None, x, y, self._screen, (204, 193, 180), current.width
        )

    def move_right(self, execute_move=True):
        """Shift all tiles right."""
        global RIGHT_AVAILABLE
        RIGHT_AVAILABLE = 0
        for i in range(0, self._size):
            for k in range(0, self._size):
                for j in range(0, self._size - 1):
                    if j + 1 <= self._size - 1:
                        # If 2 adjacent tiles have the same value...
                        if self._tiles[i][j + 1].value == self._tiles[i][j].value:
                            # ...combine them if their value isn't None
                            if self._tiles[i][j].value != None:
                                self.combine_tiles(
                                    (i, j), (i, j + 1), execute_move
                                )
                                RIGHT_AVAILABLE += 1
                        elif self._tiles[i][j + 1].value == None:
                            # The adjacent tile's value is None
                            self.next_tile_is_none(
                                (i, j), (i, j + 1), execute_move
                            )
                            RIGHT_AVAILABLE += 1


    def move_left(self, execute_move=True):
        """Shift all tiles left."""
        global LEFT_AVAILABLE
        LEFT_AVAILABLE = 0
        for i in range(0, self._size):
            for k in range(0, self._size):
                for j in range(self._size - 1, 0, -1):
                    if j - 1 >= 0:
                        # If 2 adjacent tiles have the same value...
                        if self._tiles[i][j - 1].value == self._tiles[i][j].value:
                            # ...combine them if their value isn't None
                            if self._tiles[i][j].value != None:
                                self.combine_tiles(
                                    (i, j), (i, j - 1), execute_move
                                )
                                LEFT_AVAILABLE += 1
                        elif self._tiles[i][j - 1].value == None:
                            # The adjacent tile's value is None
                            self.next_tile_is_none(
                                (i, j), (i, j - 1), execute_move
                            )
                            LEFT_AVAILABLE += 1

    def move_down(self, execute_move=True):
        """Shift all tiles down."""
        global DOWN_AVAILABLE
        DOWN_AVAILABLE = 0
        for j in range(0, self._size):
            for k in range(0, self._size):
                for i in range(0, self._size - 1):
                    if i + 1 <= self._size:
                        # If 2 adjacent tiles have the same value...
                        if self._tiles[i + 1][j].value == self._tiles[i][j].value:
                            # ...combine them if their value isn't None
                            if self._tiles[i][j].value != None:
                                self.combine_tiles(
                                    (i, j), (i + 1, j), execute_move
                                )
                                DOWN_AVAILABLE += 1
                        elif self._tiles[i + 1][j].value == None:
                            # The adjacent tile's value is None
                            self.next_tile_is_none(
                                (i, j), (i + 1, j), execute_move
                            )
                            DOWN_AVAILABLE += 1

    def move_up(self, execute_move=True):
        """Shift all tiles up."""
        global UP_AVAILABLE
        UP_AVAILABLE = 0
        for j in range(0, self._size):
            for k in range(0, self._size):
                for i in range(self._size - 1, 0, -1):
                    if i - 1 >= 0:
                        # If 2 adjacent tiles have the same value...
                        if self._tiles[i - 1][j].value == self._tiles[i][j].value:
                            # ...combine them if their value isn't None
                            if self._tiles[i][j].value != None:
                                self.combine_tiles(
                                    (i, j), (i - 1, j), execute_move
                                )
                                UP_AVAILABLE += 1
                        elif self._tiles[i - 1][j].value == None:
                            # The adjacent tile's value is None
                            self.next_tile_is_none(
                                (i, j), (i - 1, j), execute_move
                            )
                            UP_AVAILABLE += 1

    def check_available_moves(self):
        """Count the number of swaps and tile combinations in each shift
            direction."""
        # False is used an argument instead of the default argument since
        # no tiles should move around the board when checking if the game is over.
        # NOTE: A game is over when the player can no longer move the tiles.
        self.move_right(False)
        self.move_left(False)
        self.move_down(False)
        self.move_up(False)

    def add_random_tile(self):
        """Set a random tile whose value is None to have a value of 2. If
            there is no more space on the game board, determine if the game
            is over."""
        # list to store Tiles whose value is None
        empty_tiles = []

        # search for all Tiles whose value is None and add them to empty_tiles
        for i in range(0, self._size):
            for j in range(0, self._size):
                if self._tiles[i][j].value == None:
                    empty_tiles.append((i, j))

        # If the length of empty_tiles is not 0...
        if len(empty_tiles) != 0:
            # ... there is space on the board to add a new Tile
            # A random Tile is chosen to have it's value and color updated
            coord = random.choice(empty_tiles)

            i,j = coord

            self._tiles[i][j].update_color((238, 228, 218))
            self._tiles[i][j].update_value(2, (119, 110, 101))

        # Check if the game is over since there is no more space on the board
        # to move tiles without combining them.
        if len(empty_tiles) <= 1:
            self.check_available_moves()

            # These variables track if there is at least 1 way to combine
            # tiles to make space in the board.
            # If tiles cannot be combined, the player cannot move any tiles,
            # therefore, the player loses the game.
            if RIGHT_AVAILABLE == 0 and LEFT_AVAILABLE == 0 and \
                UP_AVAILABLE == 0 and DOWN_AVAILABLE == 0:
                self._game_is_over = True

    @property
    def exit_game(self):
        """Return if the game is over."""
        return self._exit_game

    def process_events(self, event):
        """Process the game events and trigger a game over pop-up if applicable."""

        # Check if the player presses the New Game button
        self._new_game.process_events(event)
        if self._new_game.pressed:
            self.initialize_tiles()
            self._score = 0
            self.update_score()
            self._new_game.unpress()
            return

        # For the direction (right,left,down,up) chosen, shift all tiles that
        # direction and determine if a "2" Tile can be added to the game board
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

        # If the game is over, process game events for the Game Over Pop-Up
        if self._game_is_over:
            self._popup.process_events(event)
            if self._popup.buttons[0].pressed:
                self._exit_game = True
            elif self._popup.buttons[1].pressed:
                self.initialize_tiles()
                self._game_is_over = False
                self._exit_game = False
                self._score = 0
                self.update_score()
                self._popup.buttons[1].unpress()
