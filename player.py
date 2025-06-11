"""
player.py
-------------
Defines the Player class for the Bouncy Block game.
Handles the player’s position, rendering, and collision detection.
"""

import pygame

from constants import (
    PLAYER_INITIAL_X, PLAYER_INITIAL_Y,
    PLAYER_WIDTH, PLAYER_HEIGHT,
    COLOR_TURQUOISE
)

class Player:
    """
    The player sprite, functions, and attributes.

    Attributes:
        _color (tuple[int, int, int]): RGB fill color for the player sprite.
        _left (int): The x-coordinate of the player’s left edge.
        _top (int): The y-coordinate of the player’s top edge.
        _rect (pygame.Rect): Pygame rectangle object used for drawing and collision.
    """
    def __init__(self):
        """Initializes Player object."""
        self._color = COLOR_TURQUOISE
        self._left = PLAYER_INITIAL_X
        self._top = PLAYER_INITIAL_Y
        self._rect = pygame.Rect(self._left, self._top, PLAYER_WIDTH, PLAYER_HEIGHT)

    def collision(self, collidingRect: pygame.Rect) -> bool:
        """
        Detects collisions with other Pygame Rect objects.

        Parameters:
            collidingRect: The Pygame Rect object the Player may have collided with
        """
        return self._rect.colliderect(collidingRect)

    def update(self, left: int, top: int) -> None:
        """
        Updates player's position.

        Parameters:
            left: New player x-coordinate
            top: New player y-coordinate
        """
        self._left = left
        self._top = top
        self._rect = pygame.Rect(left, top, PLAYER_WIDTH, PLAYER_HEIGHT)

    def draw(self, display_screen: pygame.Surface) -> None:
        """
        Draws player's Rect object on the display screen.

        Parameters:
            display_screen: The Pygame display screen
        """
        pygame.draw.rect(display_screen, self._color, self._rect)

    def get_left(self) -> int:
        """Returns player's current x-coordinate."""
        return self._left

    def get_top(self) -> int:
        """Returns player's current y-coordinate."""
        return self._top
