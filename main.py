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
pygame.font.init()

WIDTH, HEIGHT = 1280, 720

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))


# Load images
RED_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_red_small.png"))

# Player player
YELLOW_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_yellow.png"))

# Lasers
RED_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))

# Background
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-black.png")), (WIDTH, HEIGHT))

   
# An abstract class. Won't be used in itself but inherited from!


# To be used later
# Class that inherits from Ship
# class Player(Ship)

def main():
    run = True
    # Constants
    dAngle = 1/math.sqrt(2)
    # Frames per second
    FPS = 60 
    num_bullets = 0
    main_font = pygame.font.SysFont("righteous", 30)

    # Player Settings
    maxv = 10.0 
    acceleration = 0.5 
    turnRate = pi/48
    lockTurn = False
    bulletvelocity = 25

    # List for all player bullets
    numBullets = 0
    bulletlist = list()

    # Creating a ship at middle of the screen
    ship = Ship(WIDTH/2, HEIGHT/2)

    clock = pygame.time.Clock()

    # A function inside of the function
    def redraw_window():
        WINDOW.blit(BG, (0,0))

        # printing text
        num_bullets_label = main_font.render(f"BULLETS: {num_bullets}", 1, (255, 255, 255))
        WINDOW.blit(num_bullets_label, (20,20))


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
