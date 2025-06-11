"""
utils.py
-------------
Utility functions to help run Bouncy Block.
"""

import pygame

from constants import (
    LEFT_BOUNDARY, RIGHT_BOUNDARY, UPPER_BOUNDARY, START_BLOCK,
    COLOR_BLACK
)

def draw_boundaries(display_screen: pygame.Surface, game_started: bool) -> None:
    """
    Draws the boundaries in the game.

    Parameters:
        display_screen: The Pygame display screen
        game_started: Whether or not the user has started a new game
    """
    pygame.draw.rect(display_screen, COLOR_BLACK, LEFT_BOUNDARY)
    pygame.draw.rect(display_screen, COLOR_BLACK, RIGHT_BOUNDARY)
    if game_started:
        pygame.draw.rect(display_screen, COLOR_BLACK, UPPER_BOUNDARY)
    else:
        pygame.draw.rect(display_screen, COLOR_BLACK, START_BLOCK)
