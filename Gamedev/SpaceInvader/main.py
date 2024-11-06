import pygame
import pygame.display as dp
import pygame.image as img
import random
import math
from pygame import mixer

pygame.init()

#Setting Resolutions
screen = dp.set_mode((800,600))

#Title,Background and Icon
dp.set_caption("Space Invaders")
icon = img.load('Assets/ufo.png')
dp.set_icon(icon)
bg=img.load('Assets/bg.png')
bgm=mixer.music.load('Assets/background.wav')
mixer.music.play(-1)



#Player
playerImg = img.load('Assets/arcade-game.png')
playerX = 370 #X-Coordinate
playerY = 480 #Y-Coordinate
score_values = 0


def show_score(x,y):
    font = pygame.font.Font('freesansbold.ttf',32)
    score = font.render("Score : " + str(score_values), True, (255,255,255))
    screen.blit(score, (x,y))


#Draws the player on the screen
def player(x,y):
    screen.blit(playerImg, (x,y))

#enemy
enemyImg     = []
enemyX       = []
enemyY       = []
enemyXchange = []
enemyYchange = []
num_of_enemies = 6
for i in range(num_of_enemies):
    enemyImg.append(img.load('Assets/enemy.png'))
    enemyX.append(random.randint(0,720)) #X-Coordinate
    enemyY.append(random.randint(50,150)) #Y-Coordinate
    enemyXchange.append(0.6)
    enemyYchange.append(40)

#Draws the enemy on the screen

def enemy(x,y,i):
    screen.blit(enemyImg[i], (x,y))

#bullet
# ready - You can't see the bullet on the screen
# fire - The bullet is currently moving
bulletImg = img.load('Assets/bullet.png')
bulletX = 0
bulletY = 480
bulletXchange = 0
bulletYchange = 4
bullet_state = "ready"

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x+16, y+10))
     #To make the bullet appear in the center of the spaceship

# Collision
def isCollision(enemyX,enemyY,bulletX,bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX,2)) + (math.pow(enemyY-bulletY,2)))
    if distance < 27:
        return True
    else:
        return False
    
def game_over_text():
    over_font = pygame.font.Font('freesansbold.ttf',64)
    over_text = over_font.render("GAME OVER", True, (255,255,255))
    screen.blit(over_text, (200,250))

    


#Game Loop
running = True
while running:

    #RGB - Red, Green, Blue
    screen.fill((0,0,0))
    screen.blit(bg,(0,0))
    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound('Assets/laser.wav')
                    bullet_sound.play()
                    bulletX=playerX
                    fire_bullet(bulletX, bulletY)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and playerX > 0:
        playerX -= 1
    if keys[pygame.K_RIGHT] and playerX < 736:
        playerX += 1
    if keys[pygame.K_UP] and playerY > 0:
        playerY -= 1
    if keys[pygame.K_DOWN] and playerY < 536:
        playerY += 1

    for i in range(num_of_enemies):

        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyXchange[i]
        if enemyY[i] >= 536:
            enemyY[i] = 536

        if enemyX[i] <= 0 :
            enemyX[i]=0
            enemyXchange[i] = 0.6
            enemyY[i] += enemyYchange[i]

        elif enemyX[i] >= 736:
            enemyX[i] = 736
            enemyXchange[i] = -0.6
            enemyY[i] += enemyYchange[i]
        
        #Collision
        collision = isCollision(enemyX[i] ,enemyY[i],bulletX,bulletY)
        if collision:
            collision_sound = mixer.Sound('Assets/explosion.wav')
            collision_sound.play()
            bulletY =  480
            bullet_state = "ready"
            score_values += 1
            enemyX[i] = random.randint(0,720) #X-Coordinate
            enemyY[i] = random.randint(50,150) #Y-Coordinate

        enemy(enemyX[i], enemyY[i],i)

        
    

        #Bullet Movement
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletYchange
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    



    player(playerX, playerY)
    show_score(10,10)
    
    dp.update()
