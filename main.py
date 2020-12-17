import math
import random
from random import randrange

import pygame
from pygame import mixer

# Intialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((1200, 600))

# Background
background = pygame.image.load('spaceme.png')

# Sound
mixer.music.load("bensound-rumble.wav")
mixer.music.play(-1)

# Caption and Icon
pygame.display.set_caption("Space Battle")
icon = pygame.image.load('bs.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('bn.png')
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = randrange(5,10)

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('ufo.png'))
    enemyX.append(random.randint(200, 1150))
    enemyY.append(random.randint(20, 20))
    enemyX_change.append(5)
    enemyY_change.append(70)

# Bullet

# Ready - You can't see the bullet on the screen
# Fire - The bullet is currently moving

bulletImg = pygame.image.load('bullets.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 40
bullet_state = "ready"

# Score

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
testY = 10

# Game Over
#over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render("Score : " + str(score_value) + " |", True, (255, 255, 255))
    screen.blit(score, (x, y))

gameImg = pygame.image.load('game-over.png')
gameX = 500
gameY = 170
gameX_change = 0

def game_over_text(x,y):
 #   over_text = over_font.render("GAME OVER", True, (255, 255, 255))
 #   screen.blit(over_text, (200, 250))
    screen.blit(gameImg, (x, y))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game Loop
running = True
while running:

    # RGB = Red, Green, Blue
    screen.fill((0, 0, 0))
    # Background Image
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -6
            if event.key == pygame.K_RIGHT:
                playerX_change = 6
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
         #           bulletSound = mixer.Sound("laser.wav")
         #           bulletSound.play()
                    # Get the current x cordinate of the spaceship
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # 5 = 5 + -0.1 -> 5 = 5 - 0.1
    # 5 = 5 + 0.1

    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 1136:
        playerX = 1136

    # Enemy Movement
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] >= 426 and enemyX[i] == playerX_change :
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text(gameX,gameY)
            break

        if enemyY[i] >= 470 :
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text(gameX,gameY)
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 5
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 1150:
            enemyX_change[i] = -5
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
      #      explosionSound = mixer.Sound("explosion.wav")
      #      explosionSound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(200, 1150)
            enemyY[i] = random.randint(20, 20)
            
            

        enemy(enemyX[i], enemyY[i], i)

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, testY)
    pygame.display.update()
