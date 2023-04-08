import pygame
import random

pygame.init()
dis=pygame.display.set_mode((600,666))
pygame.display.set_caption('Da Game')
pygame.display.update()

clock = pygame.time.Clock()

mainFont = pygame.font.SysFont("bahnschrift", 35)
bigFont = pygame.font.SysFont("bahnschrift", 65)
scoreFont = pygame.font.SysFont("bahnschrift", 30)

blue = (0,0,255)
red = (255,0,0)
green = (0,255,0)
turquoise = (0,255,160)
black = (0,0,0)
white = (255,255,255)

class Platform:
    color = green

    def __init__(self, left, top):
        self.rect = pygame.Rect(left, top, 50, 4)
        
    def draw(self):
        pygame.draw.rect(dis, self.color, self.rect)

class FakePlatform(Platform):
    color = red

    def __init__(self, left, top):
        self.rect = pygame.Rect(left, top, 50, 4)
        
class MovingPlatform(Platform):
    color = blue
    velocity = 2

    def __init__(self, left, top):
        self.rect = pygame.Rect(left, top, 50, 4)



# Main Game Loop
playAgain = True
gameStarted = False
gameOver = False
while playAgain:
    if not gameOver:
        
        dis.fill(white)
        score = 0
        x = 300
        y = 400
        vx = 0
        vy = 0
        
        platforms = []
        yplat = 14
        yplats = []
        while yplat<=652:
            yplats.append(yplat)
            yplat+=22

        mod = 30
        for i in range(23):
            rand = random.randint(10, 540)
            yplat = yplats[rand%mod]
            yplats.remove(yplat)
            mod-=1
            platforms.append(Platform(rand, yplat))

        for j in range(5):
            rand = random.randint(10, 540)
            yplat = yplats[rand%mod]
            yplats.remove(yplat)
            mod-=1
            platforms.append(FakePlatform(rand, yplat))

        for k in range(2):
            rand = random.randint(10, 540)
            yplat = yplats[k]
            platforms.append(MovingPlatform(rand, yplat))

        player = pygame.Rect(x, y, 20, 20)

        for platform in platforms:
            platform.draw()
        pygame.draw.rect(dis, turquoise, player)

        leftBoundary = pygame.Rect(0,0,10,666)
        rightBoundary = pygame.Rect(590,0,10,666)
        upperBoundary = pygame.Rect(0,0,600,47)
        pygame.draw.rect(dis, black, leftBoundary)
        pygame.draw.rect(dis, black, rightBoundary)
        pygame.draw.rect(dis, black, upperBoundary)

        start = scoreFont.render("START", True, white)
        dis.blit(start, [(300-start.get_rect().width/2),5])

        pygame.display.update()
                
    while not gameOver:
        
        for event in pygame.event.get():
            if event.type==pygame.KEYDOWN:
                gameStarted = True
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
                
        while gameStarted==True:
            
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    quit()
                        
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                x+=-5
            if keys[pygame.K_RIGHT]:
                x+=5

            if event.type==pygame.QUIT:
                gameOver=True
                break
                    
            if vx!=0:
                x+=vx
            if vx<0:
                vx+=0.5
            if vx>0:
                vx+=-0.5

            y+=vy
            if vy<15:
                vy+=0.5
                
            player.left=x
            player.top=y
                
            dis.fill(white)
            for platform in platforms:
                if player.top<400:
                    platform.rect.top+=6
                    score+=1
                if platform.rect.top>666:
                    platform.rect.top=0
                    rand = random.randint(10, 540)
                    platform.rect.left=rand
                if platform.color==blue:
                    if platform.rect.colliderect(leftBoundary) or platform.rect.colliderect(rightBoundary):
                        platform.velocity*=-1
                    platform.rect.left+=platform.velocity
                platform.draw()
            pygame.draw.rect(dis, turquoise, player)
                
            if player.colliderect(leftBoundary):
                vx=16
                vy=-6
            if player.colliderect(rightBoundary):
                vx=-16
                vy=-6
                    
            for platform in platforms:
                if player.colliderect(platform.rect) and platform.color!=red and vy>0:
                    vy=-11                  
                        
            if y>666:
                gameOver = True
                gameStarted = False

            pygame.draw.rect(dis, black, leftBoundary)
            pygame.draw.rect(dis, black, rightBoundary)
            pygame.draw.rect(dis, black, upperBoundary)
            
            if score%100==0:
                realScore = score/100
                currentScore = scoreFont.render(str(int(realScore)), True, white)
            dis.blit(currentScore, [(300-currentScore.get_rect().width/2),5])
            
            pygame.event.clear()
            pygame.display.update()
            clock.tick(60)

    dis.fill(white)
    gg = bigFont.render("GAME OVER", True, black)
    finalScore = scoreFont.render(("Final Score: " + str(int(realScore))), True, black)
    replay = mainFont.render("Play again? (Y or N)", True, black)
    dis.blit(gg, [(300-gg.get_rect().width/2),180])
    dis.blit(finalScore, [(300-finalScore.get_rect().width/2),300])
    dis.blit(replay, [(300-replay.get_rect().width/2),420])
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_y:
                gameOver = False
                gameStarted = False
            if event.key == pygame.K_n:
                playAgain = False
        if event.type == pygame.QUIT:
            playAgain = False
    
pygame.quit()
quit()

