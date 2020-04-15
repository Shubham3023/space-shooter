import pygame
import random
# to calculate the distance
import math
# to add music sound effects
from pygame import mixer

# initialize the pygame
pygame.init()

# adding background music
mixer.music.load("background.wav")
mixer.music.play(-1)

# create the screen
screen = pygame.display.set_mode((800, 600))
# background
background = pygame.image.load("background.jpg")

# add title for the game
pygame.display.set_caption("space shooter")
# add icon for the game
icon = pygame.image.load("roc.png")
pygame.display.set_icon(icon)

# the shooting rocket of player
playerImg = pygame.image.load("hero.png")
# variables to initialize the position of player
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0

# display the enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_enemy = 8
for i in range(num_enemy):
    enemyImg.append(pygame.image.load("enemy.png"))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(5)
    enemyY_change.append(25)  # as enemy moves continuously so use higher value

# bullet
bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletY_change = 10
bullet_state = "steady"
# game over
gameoverImg = pygame.font.Font("freesansbold.ttf", 80)
gameX = 200
gameY = 250

# score
score_value = 0
score_font = pygame.font.Font("freesansbold.ttf", 35)
textX = 0
textY = 0

bombImg = pygame.image.load("flame.png")


def score_count(x, y):
    score = score_font.render("score: " + str(score_value), True,
                              (0, 255, 0))  # first we render or export the value of score
    screen.blit(score, (x, y + 40))  # by this we display the score in window


def player(x, y):
    screen.blit(playerImg, (x, y))  # set position of spaceship on screen


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y)) # set position of enemy on screen


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))  # we used 10 and 16 to place bullet exactly behind spaceship


def isCollision(enemyX, enemyY, bulletX, bulletY, i):
    # distance formula will calculate shortest distance between bullet and enemy when they both come close
    distance = math.sqrt(math.pow((enemyX[i] - bulletX), 2) + math.pow((enemyY[i] - bulletY), 2))
    if distance < 25:
        return True
    else:
        return False


def game_over(enemyX, enemyY, playerX, playerY, i):
    touch = math.sqrt(math.pow((enemyX[i] - playerX), 2) + math.pow((enemyY[i] - playerY), 2))
    if touch < 27:
        return True
    else:
        return False


def over(x, y):
    over = gameoverImg.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over, (x, y))


def blast(x, y):
    screen.blit(bombImg, (x + 30, y + 30))


# quit loop
running = True
while running:
    # RGB red, green or blue (to set background colour)
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    # to get all the events in pygame
    for event in pygame.event.get():
        # to quit the game
        if event.type == pygame.QUIT:
            running = False  # by turning running variable False will exit the window
        # to set keys for spaceship movement
        if event.type == pygame.KEYDOWN:  # pygame.KEYDOWN is executed when key is been pressed
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5

            if event.key == pygame.K_SPACE:
                if bullet_state == "fire":
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    continue  # by using this we are avoiding fluctuation of bullet while we press space key multiple time
                bulletX = playerX  # we use this to avoid path of bullet same as spaceship path
                bullet_sound = mixer.Sound("laser.wav")
                bullet_sound.play()
                fire_bullet(bulletX,
                            bulletY)  # by clicking space we call bullet() function and we change the bullet_state to "fire" and execute the if statment for bullet path

        if event.type == pygame.KEYUP:  # pygame.KEYUP is executed when key is been pressed
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    """e.g. for right key playerX=5 and playerX_change=0.1
    then from equation below
    5+=0.1 = 5.1 which will move spaceship right
    foe left key playerX=5 and playerX_change = -0.1
    then from eq below
    5+= -1 = 5 + (-1)= 4.9 which will move spaceship left"""

    playerX += playerX_change
    if playerX >= 736:  # set border for spaceship
        playerX = 736
    if playerX <= 0:
        playerX = 0
    playerY += playerY_change
    if playerY >= 536:  # set border for spaceship
        playerY = 536
    if playerY <= 0:
        playerY = 0

    # to keep enemy in window
    for i in range(num_enemy):
        # to remove the top left corner score count after the game is over and display the game over tag and final score
        if enemyY[i] < 430:
            score_count(textX, textY)
        elif enemyY[i] > 430:
            for j in range(num_enemy):
                enemyY[j] = 2000
            score_count(1000, 1000)
            over(gameX, gameY)
            score_count(gameX + 160, gameY + 35)
            break

        if enemyX[i] >= 736:
            enemyX_change[i] = -1
            enemyY[i] += enemyY_change[i]  # put the vertical movement in if statement to push enemy vertically
        if enemyX[i] <= 0:
            enemyX_change[i] = 1
            enemyY[i] += enemyY_change[i]

        # collision
        collision = isCollision(enemyX, enemyY, bulletX, bulletY, i)
        if collision == True:
            collision_sound = mixer.Sound("explosion.wav")
            collision_sound.play()
            bulletY = -1
            blast(enemyX[i], enemyY[i])
            score_value += 1

            # to keep enemy in screen we give enemy its co-ordinates again
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        enemyX[i] += enemyX_change[i]
        # to increase the difficulty level we increase the speed of enemy as well as the speed of bullet
        if score_value > 5:
            bulletY_change = 15
            if enemyX[i] >= 736:
                enemyX_change[i] = -2
                enemyY[i] += enemyY_change[i]  # put the vertical movement in if statement to push enemy vertically
            if enemyX[i] <= 0:
                enemyX_change[i] = 2
                enemyY[i] += enemyY_change[i]
            enemyX[i] += enemyX_change[i]
        elif score_value > 20:
            bulletY_change = 18
            if enemyX[i] >= 736:
                enemyX_change[i] = -3
                enemyY[i] += enemyY_change[i]  # put the vertical movement in if statement to push enemy vertically
            if enemyX[i] <= 0:
                enemyX_change[i] = 3
                enemyY[i] += enemyY_change[i]
            enemyX[i] += enemyX_change[i]

        enemy(enemyX[i], enemyY[i], i)
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)  # we recall the fire_bullet function to plot bullet on screen
        bulletY -= bulletY_change  # this expression will change the position of bullet and will create an illusion
    if bulletY <= 0:  # when bullet crosses 0 this will bring bullet back to steady state which will avoid continuous firing
        bulletY = 480
        bullet_state = "steady"

    # recall the player and enemy to plot the player rocket  and enemy on the screen
    player(playerX, playerY)

    # to update the screen (e.g to increas or decreas the score or to display the timer)
    pygame.display.update()

pygame.quit()
