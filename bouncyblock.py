import pygame
import random

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 600, 700
SCROLL_HEIGHT = 450
SCROLL_SPEED = 6
FPS = 60
GRAVITY = 0.5
FRICTION = 0.5

BIG_FONT = pygame.font.SysFont("bahnschrift", 65)
MAIN_FONT = pygame.font.SysFont("bahnschrift", 35)
SCORE_FONT = pygame.font.SysFont("bahnschrift", 30)

COLOR_BLUE = (0,0,255)
COLOR_RED = (255,0,0)
COLOR_GREEN = (0,255,0)
COLOR_TURQUOISE = (0,255,190)
COLOR_BLACK = (0,0,0)
COLOR_WHITE = (255,255,255)

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

EDGE_WIDTH, EDGE_HEIGHT = 10, 45
UPPER_BOUNDARY = pygame.Rect(0, 0, SCREEN_WIDTH, EDGE_HEIGHT)
LEFT_BOUNDARY = pygame.Rect(0, 0, EDGE_WIDTH, SCREEN_HEIGHT)
RIGHT_BOUNDARY = pygame.Rect(SCREEN_WIDTH - EDGE_WIDTH, 0, EDGE_WIDTH, SCREEN_HEIGHT)
LEFT_BOUND_VELOCITY, RIGHT_BOUND_VELOCITY = (16, -6), (-16, -6)

PLAYER_MOVE_SPEED = 5
PLAYER_INITIAL_X, PLAYER_INITIAL_Y = 300, 400
PLAYER_HEIGHT, PLAYER_WIDTH = 20, 20
MAX_FALL_VELOCITY = 15

PLATFORM_WIDTH, PLATFORM_HEIGHT = 50, 4
STARTING_PLATFORM_HEIGHT = 10
PLATFORM_BUFFER_SPACE = 22
PLATFORM_VELOCITY = 2

NUM_PLATFORMS = (SCREEN_HEIGHT - STARTING_PLATFORM_HEIGHT - EDGE_HEIGHT) // PLATFORM_BUFFER_SPACE
FAKE_PLATFORMS = 3
MOVING_PLATFORMS = 5
NORMAL_PLATFORMS = NUM_PLATFORMS - FAKE_PLATFORMS - MOVING_PLATFORMS

SCORE_INCREMENT = 0.01

class Player:
    def __init__(self):
        self._color = COLOR_TURQUOISE
        self._left = PLAYER_INITIAL_X
        self._top = PLAYER_INITIAL_Y
        self._rect = pygame.Rect(self._left, self._top, PLAYER_HEIGHT, PLAYER_WIDTH)

    def update(self, left, top):
        self._left = left
        self._top = top
        self._rect = pygame.Rect(left, top, PLAYER_HEIGHT, PLAYER_WIDTH)

    def draw(self, display_screen):
        pygame.draw.rect(display_screen, self._color, self._rect)

    def collision(self, collidingRect):
        return self._rect.colliderect(collidingRect)

    def getTop(self):
        return self._top

    def getLeft(self):
        return self._left

class Platform:
    def __init__(self, left, top):
        self._color = COLOR_GREEN
        self._left = left
        self._top = top
        self._rect = pygame.Rect(left, top, PLATFORM_WIDTH, PLATFORM_HEIGHT)
        
    def draw(self, display_screen):
        pygame.draw.rect(display_screen, self._color, self._rect)

    def getColor(self):
        return self._color

    def getLeft(self):
        return self._left

    def setLeft(self, left):
        self._left = left
        self._rect = pygame.Rect(self._left, self._top, PLATFORM_WIDTH, PLATFORM_HEIGHT)

    def getTop(self):
        return self._top

    def setTop(self, top):
        self._top = top
        self._rect = pygame.Rect(self._left, self._top, PLATFORM_WIDTH, PLATFORM_HEIGHT)

    def getRect(self):
        return self._rect
    
    def update(self):
        pygame.Rect(self._left, self._top, PLATFORM_WIDTH, PLATFORM_HEIGHT)

class FakePlatform(Platform):
    def __init__(self, left, top):
        super().__init__(left, top)
        self._color = COLOR_RED
        
class MovingPlatform(Platform):
    def __init__(self, left, top):
        super().__init__(left, top)
        self._color = COLOR_BLUE
        self._velocity = PLATFORM_VELOCITY * random.choice([-1, 1])

    def getVelocity(self):
        return self._velocity

    def setVelocity(self, velocity):
        self._velocity = velocity



# Main Game Loop
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Bouncy Block')
clock = pygame.time.Clock()

playAgain = True
gameStarted = False
gameOver = False

# Creating Game Start State
while playAgain:
    if not gameOver:
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
        player_left, player_top = player.getLeft(), player.getTop()
        player_x_velocity, player_y_velocity = 0, 0

        # Drawing Rest of Initial Display
        player.draw(screen)
        pygame.draw.rect(screen, COLOR_BLACK, LEFT_BOUNDARY)
        pygame.draw.rect(screen, COLOR_BLACK, RIGHT_BOUNDARY)
        pygame.draw.rect(screen, COLOR_BLACK, START_BLOCK)
        screen.blit(START_TEXT_1, [(SCREEN_WIDTH / 2 - START_TEXT_1.get_rect().width / 2), START_TEXT_1_HEIGHT])
        screen.blit(START_TEXT_2, [(SCREEN_WIDTH / 2 - START_TEXT_2.get_rect().width / 2), START_TEXT_2_HEIGHT])
        pygame.display.update()

    # Initiating Game Loop      
    while not gameOver:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    gameStarted = True
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        # Starting Gameplay
        while gameStarted == True:
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
            
            # Drawing the Screen
            screen.fill(COLOR_WHITE)
            for platform in platforms:
                if player.collision(platform.getRect()) and platform.getColor() != COLOR_RED and player_y_velocity > 0:
                    player_top -= PLATFORM_HEIGHT * 3
                    player_y_velocity = -11
                if player.getTop() < SCROLL_HEIGHT:
                    platform.setTop(platform.getTop() + SCROLL_SPEED)
                    score += SCORE_INCREMENT
                if platform.getTop() > SCREEN_HEIGHT:
                    platform.setTop(EDGE_HEIGHT + PLATFORM_HEIGHT)
                    platform.setLeft(random.randint(EDGE_WIDTH, SCREEN_WIDTH - EDGE_WIDTH - PLATFORM_WIDTH))
                if platform.getColor() == COLOR_BLUE:
                    if platform.getRect().colliderect(LEFT_BOUNDARY) or platform.getRect().colliderect(RIGHT_BOUNDARY):
                        platform.setVelocity(platform.getVelocity() * -1)
                    platform.setLeft(platform.getLeft() + platform.getVelocity())
                platform.update()
                platform.draw(screen)
            player.update(player_left, player_top)
            player.draw(screen)                 

            pygame.draw.rect(screen, COLOR_BLACK, LEFT_BOUNDARY)
            pygame.draw.rect(screen, COLOR_BLACK, RIGHT_BOUNDARY)
            pygame.draw.rect(screen, COLOR_BLACK, UPPER_BOUNDARY)

            score_render = SCORE_FONT.render(str(int(score)), True, COLOR_WHITE)
            screen.blit(score_render, [(SCREEN_WIDTH / 2 - score_render.get_rect().width / 2), SCORE_HEIGHT])

            # Checking if the Player Lost
            if player.getTop() > SCREEN_HEIGHT:
                gameOver = True
                gameStarted = False

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
                gameOver = False
                gameStarted = False
            if event.key == pygame.K_n:
                playAgain = False
        if event.type == pygame.QUIT:
            playAgain = False

# Ending Game
pygame.quit()
quit()
