"""
constants.py
-------------
Defines all configurable parameters for the Bouncy Block game, including:
  - screen dimensions and frame rate
  - physics (gravity, friction)
  - scoring parameters
  - scrolling thresholds
  - font and text renderers
  - colors
  - UI element positions and sizes
  - game boundary definitions
  - player and platform settings
"""

import pygame

# Screen Setup
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 700
FPS = 60

# Physics Parameters
GRAVITY = 0.5
FRICTION = 0.5

# Scoring
SCORE_INCREMENT = 0.01

# Scrolling
SCROLL_HEIGHT = 450
SCROLL_SPEED = 6

# Fonts (requires pygame.init() before import!)
BIG_FONT = pygame.font.SysFont("bahnschrift", 65)
MAIN_FONT = pygame.font.SysFont("bahnschrift", 35)
SCORE_FONT = pygame.font.SysFont("bahnschrift", 30)

# Colors
COLOR_BLACK = (0,0,0)
COLOR_BLUE = (0,0,255)
COLOR_GREEN = (0,255,0)
COLOR_RED = (255,0,0)
COLOR_TURQUOISE = (0,255,190)
COLOR_WHITE = (255,255,255)

# UI/Text
SCORE_HEIGHT = 10
START_BLOCK_HEIGHT = 140
START_TEXT_1_HEIGHT = 30
START_TEXT_2_HEIGHT = START_TEXT_1_HEIGHT + MAIN_FONT.get_linesize()
START_TEXT_1 = MAIN_FONT.render("Press Left or Right", True, COLOR_WHITE)
START_TEXT_2 = MAIN_FONT.render("Arrow Keys to Start", True, COLOR_WHITE)
START_BLOCK = pygame.Rect(0, 0, SCREEN_WIDTH, START_BLOCK_HEIGHT)

GAME_OVER_TEXT = BIG_FONT.render("GAME OVER", True, COLOR_BLACK)
REPLAY_TEXT = MAIN_FONT.render("Play again? (Y or N)", True, COLOR_BLACK)
GAME_OVER_TEXT_HEIGHT = 180
REPLAY_TEXT_HEIGHT = 420

# Boundaries
EDGE_WIDTH, EDGE_HEIGHT = 10, 45
UPPER_BOUNDARY = pygame.Rect(0, 0, SCREEN_WIDTH, EDGE_HEIGHT)
LEFT_BOUNDARY = pygame.Rect(0, 0, EDGE_WIDTH, SCREEN_HEIGHT)
RIGHT_BOUNDARY = pygame.Rect(SCREEN_WIDTH - EDGE_WIDTH, 0, EDGE_WIDTH, SCREEN_HEIGHT)
LEFT_BOUND_VELOCITY, RIGHT_BOUND_VELOCITY = (16, -6), (-16, -6)

# Player
PLAYER_MOVE_SPEED = 6
PLAYER_INITIAL_X, PLAYER_INITIAL_Y = 300, 400
PLAYER_HEIGHT, PLAYER_WIDTH = 20, 20
MAX_FALL_VELOCITY = 15

# Platforms
PLATFORM_WIDTH, PLATFORM_HEIGHT = 50, 4
STARTING_PLATFORM_HEIGHT = 10
PLATFORM_BUFFER_SPACE = 22
PLATFORM_VELOCITY = 2

BOUNCE_HEIGHT = PLATFORM_HEIGHT * 3
BOUNCE_SPEED = -11

NUM_PLATFORMS = (SCREEN_HEIGHT - STARTING_PLATFORM_HEIGHT - EDGE_HEIGHT) // PLATFORM_BUFFER_SPACE
FAKE_PLATFORMS = 3
MOVING_PLATFORMS = 5
NORMAL_PLATFORMS = NUM_PLATFORMS - FAKE_PLATFORMS - MOVING_PLATFORMS
