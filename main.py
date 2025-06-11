"""
main.py
-------------
A simple jumping game built with Pygame.
This module contains the main game loop.
To start the game, simply run this script.
"""

import random
import pygame
pygame.init()

from constants import *
from platforms import *
from player import *
from utils import *

# Main Game Loop
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Bouncy Block')
clock = pygame.time.Clock()

play_again = True
game_started = False
game_over = False

# Creating Game Start State
while play_again:
    if not game_over:
        score = 0

        # Generating and Drawing Platforms
        screen.fill(COLOR_WHITE)
        fake_spawn_flag = False
        platforms = []
        platform_dictionary = {
            Platform: NORMAL_PLATFORMS,
            FakePlatform: FAKE_PLATFORMS,
            MovingPlatform: MOVING_PLATFORMS
        }
        platform_top = STARTING_PLATFORM_HEIGHT
        for i in range(NORMAL_PLATFORMS + FAKE_PLATFORMS + MOVING_PLATFORMS):
            platform_constructors = [
                constructor for constructor, count in platform_dictionary.items()
                if count > 0 and not (fake_spawn_flag and constructor is FakePlatform)
            ]
            platform_constructor = random.choice(platform_constructors)
            platform_left = random.randint(EDGE_WIDTH, SCREEN_WIDTH - EDGE_WIDTH - PLATFORM_WIDTH)
            platforms.append(platform_constructor(platform_left, platform_top))
            platform_dictionary[platform_constructor] -= 1
            if platform_dictionary[platform_constructor] <= 0:
                del platform_dictionary[platform_constructor]
            platform_top += PLATFORM_BUFFER_SPACE
            fake_spawn_flag = platform_constructor is FakePlatform
            platforms[i].draw(screen)

        # Generating Player
        player = Player()
        player_left, player_top = player.get_left(), player.get_top()
        player_x_velocity, player_y_velocity = 0, 0

        # Drawing Rest of Initial Display
        player.draw(screen)
        draw_boundaries(screen, game_started)
        screen.blit(START_TEXT_1, [(SCREEN_WIDTH / 2 - START_TEXT_1.get_rect().width / 2), START_TEXT_1_HEIGHT])
        screen.blit(START_TEXT_2, [(SCREEN_WIDTH / 2 - START_TEXT_2.get_rect().width / 2), START_TEXT_2_HEIGHT])
        pygame.display.update()

    # Initiating Game Loop      
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    game_started = True
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        # Starting Gameplay
        while game_started == True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            # Moving the Player Horizontally         
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                player_left -= PLAYER_MOVE_SPEED
            if keys[pygame.K_RIGHT]:
                player_left += PLAYER_MOVE_SPEED
                 
            player_left += player_x_velocity
            if player_x_velocity < 0:
                player_x_velocity += FRICTION
            if player_x_velocity > 0:
                player_x_velocity -= FRICTION

            # Moving the Player Vertically
            player_top += player_y_velocity
            if player_y_velocity < MAX_FALL_VELOCITY:
                player_y_velocity += GRAVITY

            # Checking Player and Boundary Collisions
            if player.collision(UPPER_BOUNDARY):
                player_top += EDGE_HEIGHT // 2
                player_y_velocity = -player_y_velocity
            if player.collision(LEFT_BOUNDARY):
                player_x_velocity, player_y_velocity = LEFT_BOUND_VELOCITY
            if player.collision(RIGHT_BOUNDARY):
                player_x_velocity, player_y_velocity = RIGHT_BOUND_VELOCITY   
            
            # Updating and Drawing the Screen
            screen.fill(COLOR_WHITE)
            for platform in platforms:
                # if player hits platform, they bounce
                if player.collision(platform.get_rect()) and platform.get_color() != COLOR_RED and player_y_velocity > 0:
                    player_top -= BOUNCE_HEIGHT
                    player_y_velocity = BOUNCE_SPEED

                # if player reaches SCROLL_HEIGHT, move the entire screen up
                if player.get_top() < SCROLL_HEIGHT:
                    platform.set_top(platform.get_top() + SCROLL_SPEED)
                    score += SCORE_INCREMENT

                # if platform hits the bottom, move to top
                if platform.get_top() > SCREEN_HEIGHT:
                    platform.set_top(EDGE_HEIGHT + PLATFORM_HEIGHT)
                    platform.set_left(random.randint(EDGE_WIDTH, SCREEN_WIDTH - EDGE_WIDTH - PLATFORM_WIDTH))

                # moves MovingPlatform horizontally
                if platform.get_color() == COLOR_BLUE:
                    if platform.get_rect().colliderect(LEFT_BOUNDARY) or platform.get_rect().colliderect(RIGHT_BOUNDARY):
                        platform.set_velocity(platform.get_velocity() * -1)
                    platform.set_left(platform.get_left() + platform.get_velocity())

                platform.update()
                platform.draw(screen)

            player.update(player_left, player_top)
            player.draw(screen)                 
            draw_boundaries(screen, game_started)
            score_render = SCORE_FONT.render(str(int(score)), True, COLOR_WHITE)
            screen.blit(score_render, [(SCREEN_WIDTH / 2 - score_render.get_rect().width / 2), SCORE_HEIGHT])

            # Checking if the Player Lost
            if player.get_top() > SCREEN_HEIGHT:
                game_over = True
                game_started = False

            # Updating Game Display and Clock
            pygame.event.clear()
            pygame.display.update()
            clock.tick(FPS)

    # End Game Display
    screen.fill(COLOR_WHITE)
    final_score = SCORE_FONT.render(("Final Score: " + str(int(score))), True, COLOR_BLACK)
    screen.blit(GAME_OVER_TEXT, [(SCREEN_WIDTH / 2 - GAME_OVER_TEXT.get_rect().width / 2), GAME_OVER_TEXT_HEIGHT])
    screen.blit(REPLAY_TEXT, [(SCREEN_WIDTH / 2 - REPLAY_TEXT.get_rect().width / 2), REPLAY_TEXT_HEIGHT])
    screen.blit(final_score, [(SCREEN_WIDTH / 2 - final_score.get_rect().width / 2), SCREEN_WIDTH / 2])
    pygame.display.update()

    # Checking to Play Again
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_y:
                game_over = False
                game_started = False
            if event.key == pygame.K_n:
                play_again = False
        if event.type == pygame.QUIT:
            play_again = False

# Ending Game
pygame.quit()
quit()
