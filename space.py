import pygame
import math
import random
from pygame import mixer 

# initializing pygame
pygame.init()

# creating window screen
window = pygame.display.set_mode((800, 600))

#background img
background = pygame.image.load('back_ground.jpg').convert()
# Editing window icon and name
pygame.display.set_caption("Space Invader")
pygame.display.set_icon(pygame.image.load("icon.png"))

# sound
# mixer.music.load("blast.wav")
# mixer.music.play(-1)

#score
score = 0
font = pygame.font.Font("freesansbold.ttf",30)

def show_score():
    scores = font.render("score :" + str(score),True , (255, 255, 0))
    window.blit(scores, (10 , 10))

#game over
font_o= pygame.font.Font("freesansbold.ttf",70)

def gameOver():
    over =font_o.render("GAME OVER !!!", True, (0, 255, 0))
    window.blit(over, (150 , 150))


# player
player_x=370
player_y=520
playerX_dx= 0
playerY_dy= 0
playerImg = pygame.image.load('spaceship.png')

def player(x,y):
    window.blit(playerImg , (x,y))

# enemy
enemy_x = []
enemy_y = []
enemyX_dx = []
enemyY_dy = []
enemyImg = []

for i in range(5):
    enemyImg.append(pygame.image.load("alien.png"))
    enemy_x.append(random.randint(0, 736))
    enemy_y.append(random.randint(0, 100))
    enemyX_dx.append(0.3)
    enemyY_dy.append(64)

def enemy(x , y, i):
    window.blit(enemyImg[i],(x , y))

# bullet
bullet_x = 0
bullet_y = player_y
bullet_state = "ready"
bulletImg = pygame.image.load("bullet.png")

def bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    window.blit(bulletImg, ( x+17 , y+16 ))

def collision(enemy_x, enemy_y, bullet_x, bullet_y):
    # comparing distance between bullet and enemy for collision to be occured 
    if math.sqrt(math.pow((enemy_x - bullet_x),2) + math.pow((enemy_y - bullet_y),2) ) <= 32:
        return True
    else:
        return False


running = True
while running :
    window.fill((0,0,0))
    window.blit(background , (0,0))
    for event in pygame.event.get():
        if event.type ==pygame.QUIT:
            running = False

        # check keystroke for player movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_dx =-3
            if event.key ==pygame.K_RIGHT:
                playerX_dx =3
            if event.key == pygame.K_UP:
                playerY_dy =-1
            if event.key ==pygame.K_DOWN:
                playerY_dy =2

            # for bullet
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_x = player_x  
                    bullet_y = player_y   
                    bullet(bullet_x,bullet_y)
                    
                    # bullet sound
                    bullet_sound = mixer.Sound("laser.wav") 
                    bullet_sound.play()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT :
                playerX_dx = 0
            if event.key == pygame.K_DOWN or event.key == pygame.K_UP:  
                playerY_dy = 0  
                
    # player movement    
    player_x +=playerX_dx
    if player_x <= 0:
        player_x = 0
    elif player_x >= 736:
        player_x = 736

    player_y +=playerY_dy
    if player_y <= 0:
        player_y = 0
    elif player_y >= 520:
        player_y = 520

    # enemy novement
    for i in range(5):
        if enemy_x[i] >=736:
            enemy_y[i] +=64
            enemy_x[i] =0
            enemyX_dx[i] = .5
        enemy_x[i] += enemyX_dx[i]

        # collision
        collided = collision(enemy_x[i], enemy_y[i], bullet_x, bullet_y)
        if collided:
            # blast sound
            blast = mixer.Sound("blast.wav")
            blast.play()

            bullet_y = 536
            bullet_state = "ready"
            enemy_x[i] = random.randint(0, 736)
            enemy_y[i] = random.randint(0, 100)
            score +=1
        enemy(enemy_x[i] , enemy_y[i], i)   

        # check for game over
        if enemy_y[i] > 384:
            gameOver()
            bullet_state = "ready"
            # clearing the enemy
            for i in range(5):
                enemy_x[i] =900
         
    # bullet movement
    if bullet_y <=0:
        bullet_y = 520
        bullet_state = "ready"
    if bullet_state == "fire":   
        bullet(bullet_x , bullet_y)
        bullet_y -=2

    show_score()
    player(player_x, player_y)
    enemy(enemy_x[i] , enemy_y[i], i)
    pygame.display.update()

    


