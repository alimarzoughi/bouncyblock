"""
platforms.py
-------------
Defines the various platform types in the Bouncy Block game:
    Platform: stationary green platform
    FakePlatform: red platform that cannot be bounced off of
    MovingPlatform: blue platform that moves horizontally
"""

import pygame
import random

from constants import (
    PLATFORM_WIDTH, PLATFORM_HEIGHT, PLATFORM_VELOCITY,
    COLOR_BLUE, COLOR_GREEN, COLOR_RED
)

class Platform:
    """
    Basic green platform for player to bounce off of.

    Attributes:
        _color (tuple[int, int, int]): RGB fill color for the platform sprite.
        _left (int): The x-coordinate of the platform’s left edge.
        _top (int): The y-coordinate of the platform’s top edge.
        _rect (pygame.Rect): Pygame rectangle object used for drawing and collision.
    """
    def __init__(self, left: int, top: int):
        """
        Initializes Platform object.

        Parameters:
            left: Platform starting x-coordinate
            top: Platform starting y-coordinate
        """
        self._color = COLOR_GREEN
        self._left = left
        self._top = top
        self._rect = pygame.Rect(left, top, PLATFORM_WIDTH, PLATFORM_HEIGHT)

    def update(self) -> None:
        """Updates platform's Rect object based on position changes."""
        self._rect = pygame.Rect(self._left, self._top, PLATFORM_WIDTH, PLATFORM_HEIGHT)

    def draw(self, display_screen: pygame.Surface) -> None:
        """
        Draws platform's Rect object on the display screen.

        Parameters:
            display_screen: The Pygame display screen
        """
        pygame.draw.rect(display_screen, self._color, self._rect)

    def get_color(self) -> tuple[int, int, int]:
        """Returns platform's color in RGB form."""
        return self._color

    def get_left(self) -> int:
        """Returns platform's current x-coordinate."""
        return self._left

    def set_left(self, left: int) -> None:
        """
        Sets platform's new x-coordinate.

        Parameters:
            left: New platform x-coordinate
        """
        self._left = left
        self._rect = pygame.Rect(self._left, self._top, PLATFORM_WIDTH, PLATFORM_HEIGHT)

    def get_top(self) -> int:
        """Returns platform's current y-coordinate."""
        return self._top

    def set_top(self, top: int) -> None:
        """
        Sets platform's new y-coordinate.

        Parameters:
            top: New platform y-coordinate
        """
        self._top = top
        self._rect = pygame.Rect(self._left, self._top, PLATFORM_WIDTH, PLATFORM_HEIGHT)

    def get_rect(self) -> pygame.Rect:
        """Returns platform's Pygame Rect object."""
        return self._rect


class FakePlatform(Platform):
    """
    Fake red platform that the player cannot bounce off of.

    Inherits from Platform.
    """
    def __init__(self, left, top):
        """
        Initializes FakePlatform object.

        Parameters:
            left: Platform starting x-coordinate
            top: Platform starting y-coordinate
        """
        super().__init__(left, top)
        self._color = COLOR_RED


class MovingPlatform(Platform):
    """
    Blue platform that can be bounced off of, but moves horizontally back and forth.

    Inherits from Platform.
    New Attributes:
        _velocity (float): Horizontal speed and direction.
    """
    def __init__(self, left: int, top: int):
        """
        Initializes MovingPlatform object.

        Parameters:
            left: Platform starting x-coordinate
            top: Platform starting y-coordinate
        """
        super().__init__(left, top)
        self._color = COLOR_BLUE
        self._velocity = PLATFORM_VELOCITY * random.choice([-1, 1])

    def get_velocity(self) -> float:
        """Returns platform's horizontal velocity."""
        return self._velocity

    def set_velocity(self, velocity: float) -> None:
        """
        Sets platform's horizontal velocity.

        Parameters:
            velocity: New horizontal velocity
        """
        self._velocity = velocity
