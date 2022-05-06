from dataclasses import dataclass
from math import sin
from math import pi
from math import cos
import math
import pygame
import os
import time
import random
from Bullet import *
from Ship import *
from Enemy import *
pygame.font.init()

WIDTH, HEIGHT = 1600, 900

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

# Background
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-black.png")), (WIDTH, HEIGHT))


def main():
    run = True
    # Constants
    dAngle = 1/math.sqrt(2)
    FPS = 60 
    num_bullets = 0
    main_font = pygame.font.SysFont("righteous", 30)

    # Player Settings
    maxv = 10.0 
    acceleration = 0.5 
    turnRate = pi/48
    lockTurn = False
    bulletvelocity = 25

    # Other settings
    enemy_spawnrate = 1
    enemy_velocity = 4
    enemy_rate_of_fire = 0

    # List for all player bullets
    numBullets = 0
    bulletlist = list()

    # Creating a ship at middle of the screen
    ship = Ship(WIDTH/2, HEIGHT/2)
    enemiesDown = []
    enemiesRight = []
    enemiesLeft = []
    enemiesUp = []
    enemy_velocity = 4

    clock = pygame.time.Clock()

    # A function inside of the function
    def redraw_window():
        WINDOW.blit(BG, (0,0))

        # printing text
        num_bullets_label = main_font.render(f"BULLETS: {num_bullets}", 1, (255, 255, 255))
        WINDOW.blit(num_bullets_label, (20,20))

        for enemy in enemiesDown:
            enemy.draw(WINDOW)
        
        for enemy in enemiesRight:
            enemy.draw(WINDOW)

        for enemy in enemiesLeft:
            enemy.draw(WINDOW)

        for enemy in enemiesUp:
            enemy.draw(WINDOW)


        # The ship will call its own draw method
        ship.draw(WINDOW)
        #Draw all bullets on screen
        for i in bulletlist:
            if abs(i.x-ship.x) < 3000 and abs(i.y-ship.y) < 3000:
                i.draw(WINDOW)
            else:
                bulletlist.remove(i)


    

        pygame.display.update()

        #Draw other collidable objects in a loop here. Enemies, asteroids etc. 

    while run:
        clock.tick(FPS)
        redraw_window()


        if len(enemiesDown) == 0:
            i = 0
            while i<3:
                enemy = Enemy(random.randrange(50, WIDTH-100), random.randrange(-1500, -100))
                enemiesDown.append(enemy)
                i+=1

        if len(enemiesRight) == 0:
            i = 0
            while i<3:
                enemy = Enemy(random.randrange(-1500, -100), random.randrange(50, HEIGHT-100))
                enemiesRight.append(enemy)
                i+=1

        if len(enemiesLeft) == 0:
            i = 0
            while i<3:
                enemy = Enemy(random.randrange(WIDTH + 100, WIDTH + 1500), random.randrange(50, HEIGHT-100))
                enemiesLeft.append(enemy)
                i+=1

        if len(enemiesUp) == 0:
            i = 0
            while i<3:
                enemy = Enemy(random.randrange(50, WIDTH-100), random.randrange(HEIGHT+100, HEIGHT+1500))
                enemiesUp.append(enemy)
                i+=1


        for enemy in enemiesDown:
             enemy.moveDown(enemy_velocity)

        for enemy in enemiesRight:
            enemy.moveRight(enemy_velocity)

        for enemy in enemiesLeft:
            enemy.moveLeft(enemy_velocity)

        for enemy in enemiesUp:
            enemy.moveUp(enemy_velocity)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # This is not positioned in the for loop above so that 
        # multiple keys can be pressed at the same time
        keys = pygame.key.get_pressed()

        # List of available key presses:
        #  WASD, 1, SPACE, RETURN
        if keys[pygame.K_a] and not keys[pygame.K_w] or keys[pygame.K_a] and not keys[pygame.K_s]: #left exlusive
            # change in speed
            if ship.xv>-maxv:
                ship.xv = ship.xv - acceleration
            else:
                ship.xv = -maxv
            if not lockTurn:
                # periodic switch if rotational value is out of range.
                if ship.rotation > 2*pi:
                    ship.rotation = ship.rotation - 2*pi
                elif ship.rotation < 0:
                    ship.rotation = ship.rotation + 2*pi
                # Rotation towards pi 
                elif abs(ship.rotation - pi)<0.01:
                    ship.rotation = pi
                elif ship.rotation>pi and ship.rotation <= 2*pi: 
                    ship.rotation = ship.rotation - turnRate
                else: 
                    ship.rotation = ship.rotation + turnRate
                    

        if keys[pygame.K_a] and keys[pygame.K_w]: #left and up
            # change in speed
            if ship.xv>-maxv:
                ship.xv = ship.xv - acceleration*dAngle
            else:
                ship.xv = -maxv
            if ship.yv>-maxv:
                ship.yv = ship.yv - acceleration*dAngle
            else: 
                ship.yv = -maxv
            if not lockTurn:
                # periodic switch if rotational value is out of range.
                if ship.rotation > 2*pi:
                    ship.rotation = ship.rotation - 2*pi
                elif ship.rotation < 0:
                    ship.rotation = ship.rotation + 2*pi
                # Rotation towards 5*pi/4
                elif abs(ship.rotation - 5*pi/4)<0.01:
                    ship.rotation = 5*pi/4
                elif ship.rotation>5*pi/4 and ship.rotation <= 2*pi or ship.rotation<pi/4 and ship.rotation>0: 
                    ship.rotation = ship.rotation - turnRate
                else: 
                    ship.rotation = ship.rotation + turnRate

        if keys[pygame.K_w] and not keys[pygame.K_a] or keys[pygame.K_w] and not keys[pygame.K_d] : #up exlusive
            #change in speed
            if ship.yv>-maxv:
                ship.yv = ship.yv - acceleration
            else:
                ship.yv = -maxv
            if not lockTurn:
            # periodic switch if rotational value is out of range.
                if ship.rotation > 2*pi:
                    ship.rotation = ship.rotation - 2*pi
                elif ship.rotation < 0:
                    ship.rotation = ship.rotation + 2*pi
                # change in rotation toward 3*pi/2
                elif abs(ship.rotation-3*pi/2)<0.01:
                    ship.rotation = 3*pi/2
                
                elif ship.rotation>=pi/2 and ship.rotation<3*pi/2: 
                    ship.rotation = ship.rotation + turnRate
                elif ship.rotation<pi/2 and ship.rotation>=0 or ship.rotation<=2*pi and ship.rotation>3*pi/2:
                    ship.rotation = ship.rotation - turnRate
                else: 
                    print("error up key")

        if keys[pygame.K_d] and keys[pygame.K_w]: #right and up
            # change in speed
            if ship.xv<maxv:
                ship.xv = ship.xv + acceleration*dAngle
            else:
                ship.xv = maxv
            if ship.yv>-maxv:
                ship.yv = ship.yv - acceleration*dAngle
            else:
                ship.yv = -maxv
            if not lockTurn:
                # periodic switch if rotational value is out of range.
                if ship.rotation > 2*pi:
                    ship.rotation =ship.rotation - 2*pi
                elif ship.rotation < 0:
                    ship.rotation = ship.rotation + 2*pi
                # change in rotation toward 0
                elif abs(ship.rotation-7*pi/4)<0.01:
                    ship.rotation = 7*pi/4
                
                elif ship.rotation<3*pi/4 and ship.rotation>=0 or ship.rotation>7*pi/4 and ship.rotation<=2*pi: 
                    ship.rotation = ship.rotation - turnRate
                else: 
                    ship.rotation = ship.rotation + turnRate

        if keys[pygame.K_d] and not keys[pygame.K_w] or keys[pygame.K_d] and not keys[pygame.K_s]: #right exlusive
            # change in speed
            if ship.xv<maxv:
                ship.xv = ship.xv + acceleration
            else:
                ship.xv = maxv
            if not lockTurn:
                # periodic switch if rotational value is out of range.
                if ship.rotation > 2*pi:
                    ship.rotation =ship.rotation - 2*pi
                elif ship.rotation < 0:
                    ship.rotation = ship.rotation + 2*pi
                # change in rotation toward 0
                elif abs(ship.rotation)<0.01 or abs(ship.rotation-2*pi)<0.01:
                    ship.rotation = 0            
                elif ship.rotation>pi and ship.rotation < 2*pi: 
                    ship.rotation = ship.rotation + turnRate
                else: 
                    ship.rotation = ship.rotation - turnRate

        if keys[pygame.K_d] and keys[pygame.K_s]: #right and down
            # change in speed
            if ship.xv<maxv:
                ship.xv = ship.xv + acceleration*dAngle
            else:
                ship.xv = maxv
            if ship.yv<maxv:
                ship.yv = ship.yv + acceleration*dAngle
            else:
                ship.yv = maxv
            if not lockTurn:
                # periodic switch if rotational value is out of range.
                if ship.rotation > 2*pi:
                    ship.rotation =ship.rotation - 2*pi
                elif ship.rotation < 0:
                    ship.rotation = ship.rotation + 2*pi
                # change in rotation toward pi/4
                elif abs(ship.rotation-pi/4)<0.01:
                    ship.rotation = pi/4        
                elif ship.rotation>pi/4 and ship.rotation <= 5*pi/4: 
                    ship.rotation = ship.rotation - turnRate
                else: 
                    ship.rotation = ship.rotation + turnRate

        if keys[pygame.K_s] and not keys[pygame.K_a] or keys[pygame.K_s] and not keys[pygame.K_d]: #down exclusive
            # change in speed
            if ship.yv<maxv:
                ship.yv = ship.yv + acceleration
            else:
                ship.yv = maxv
            if not lockTurn:
                # periodic switch if rotational value is out of range.
                if ship.rotation > 2*pi:
                    ship.rotation = ship.rotation - 2*pi
                elif ship.rotation < 0:
                    ship.rotation = ship.rotation + 2*pi
                # change in rotation toward pi/2
                elif abs(ship.rotation-pi/2)<0.01:
                    ship.rotation = pi/2
                
                elif ship.rotation>=0 and ship.rotation<pi/2 or ship.rotation>=3*pi/2 and ship.rotation<pi*2: 
                    ship.rotation = ship.rotation + turnRate
                elif ship.rotation>=pi/2 and ship.rotation<=3*pi/2:
                    ship.rotation = ship.rotation - turnRate
                else: 
                    print("error down key")
            
        if keys[pygame.K_a] and keys[pygame.K_s]: #left and down
            # change in speed
            if ship.xv>-maxv:
                ship.xv = ship.xv - acceleration*dAngle
            else:
                ship.xv = -maxv
            if ship.yv<maxv:
                ship.yv = ship.yv + acceleration*dAngle
            else:
                ship.yv = maxv
            if not lockTurn:
                # periodic switch if rotational value is out of range.
                if ship.rotation > 2*pi:
                    ship.rotation = ship.rotation - 2*pi
                elif ship.rotation < 0:
                    ship.rotation = ship.rotation + 2*pi
                # Rotation towards 3*pi/4
                elif abs(ship.rotation - 3*pi/4)<0.01:
                    ship.rotation = 3*pi/4
                elif ship.rotation>3*pi/4 and ship.rotation < 7*pi/4: 
                    ship.rotation = ship.rotation - turnRate
                elif ship.rotation>=0 and ship.rotation<3*pi/4 or ship.rotation>=7*pi/8 and ship.rotation<=2*pi:
                    ship.rotation = ship.rotation + turnRate
                else:
                    print("Error left down")      

        # Shoots bullets
        if  keys[pygame.K_SPACE]:
            direction = ship.rotation
            xb = ship.x + ship.radius*cos(direction)
            yb = ship.y + ship.radius*sin(direction)
            bulletlist.append(Bullet(xb, yb, bulletvelocity, direction))
            numBullets = numBullets + 1
            num_bullets += 1
            print("Active bullets:" + str(len(bulletlist)))
        
        # Resets player position
        if keys[pygame.K_RETURN]:
            ship.x = WIDTH/2
            ship.y = HEIGHT/2
        # Prints player position
        if keys[pygame.K_1]:
            print("X:" + str(ship.x) + " Y:" +str(ship.y))
        #Locks rotation
        if keys[pygame.K_o]:
            lockTurn = True
        else:
            lockTurn = False
        #locks position
        if keys[pygame.K_p]:
            if abs(ship.xv)<1:
                ship.xv = 0
            else:
                ship.xv = ship.xv * 0.98

            if abs(ship.yv)<1:
                ship.yv = 0
            else:
                ship.yv = ship.yv * 0.98



# Creates the home screen

def home():
    home_font = pygame.font.SysFont("righteous", 60)
    run = True
    while run:
        WINDOW.blit(BG, (0,0))
        home_text = home_font.render("PRESS THE MOUSE TO BEGIN", 1, (255, 255, 255))
        WINDOW.blit(home_text, (WIDTH/2 - home_text.get_width()/2, 350))

        home_text2 = home_font.render("---SPACE INVADERS---", 1, (255, 255, 255))
        WINDOW.blit(home_text2, (WIDTH/2 - home_text2.get_width()/2, 280))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                main()
            
    pygame.quit()


home()
