from math import sin
from math import pi
from math import cos
from numpy import rot90
import pygame
import os
import time
import random
pygame.font.init()

WIDTH, HEIGHT = 1280, 720
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

# Load images
RED_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_red_small.png"))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_green_small.png"))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_blue_small.png"))

# Player player
YELLOW_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_yellow.png"))

# Lasers
RED_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
YELLOW_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png"))

# Background
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-black.png")), (WIDTH, HEIGHT))


#Class for bullets
class Bullet:
    def __init__(self, x, y, direction):
        #Fix x and y after direction. Fixed velocity
        self.x = x
        self.y = y
        self.v = 20
        self.rotation = 0
        self.direction = direction
    
    def draw(self, WINDOW):
        #Update x and y position of bullet with direction and velocity
        self.x = int(self.x + cos(self.direction)*self.v)
        self.y = int(self.y + sin(self.direction)*self.v)
        pygame.draw.circle(WINDOW, (255, 255, 255), (self.x, self.y), 10)
   
# An abstract class. Won't be used in itself but inherited from!
class Ship:
    def __init__(self, x, y):
        # The ship stores its own position
        self.x = x
        self.y = y
        self.radius = 30
        self.rotation = pi/2
        self.xv = 0
        self.yv = 0
        # Allows us to draw the ship. These will be defined as we create the individual ships
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.bullet_Pause = 0
     
    # Adding methods

    # Drawing method. Draws on the surface "WINDOW"
    def draw(self, WINDOW):
        # update velocity
        if abs(self.xv)<0.2:
            self.xv = 0
        elif self.xv>0:
            self.xv = self.xv - 0.1
        else:
            self.xv = self.xv + 0.1
        if abs(self.yv)<0.2:
            self.yv = 0
        elif self.yv>0:
            self.yv = self.yv - 0.1
        else:
            self.yv = self.yv + 0.1
        #update x and y values by velocity
        self.x = int(self.x + self.xv)
        self.y = int(self.y + self.yv)
        pygame.draw.circle(WINDOW, (255, 0, 0), (self.x, self.y), self.radius)
        pygame.draw.circle(WINDOW, (255, 255, 255), (int(self.x+self.radius*cos(self.rotation)), int(self.y+self.radius*sin(self.rotation))), 5)


# To be used later
# Class that inherits from Ship
# class Player(Ship)

def main():
    run = True
    # Frames per second
    FPS = 60 

    #Settings
    maxv = 5.0 
    acceleration = 0.5      
    turnRate = pi/30
    # Velocty for player
    player_vel = 5

    # List for all bullets
    numBullets = 0
    bulletlist = list()
    # Creating a ship at bottom of the screen
    ship = Ship(300, 650)

    clock = pygame.time.Clock()

    # A function inside of the function
    def redraw_window():
        WINDOW.blit(BG, (0,0))

        # The ship will call its own draw method
        ship.draw(WINDOW)
        #Draw all bullets on screen
        for i in bulletlist:
            if abs(i.x) < 2000 and abs(i.y) < 2000:
                i.draw(WINDOW)
            else:
                bulletlist.remove(i)
        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_window()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # This is not positioned in the for loop above so that 
        # multiple keys can be pressed at the same time
        keys = pygame.key.get_pressed()
        # Also makes sure that there are boundaries
        if keys[pygame.K_a] and not keys[pygame.K_w] and not keys[pygame.K_s]: #left exlusive
            # change in speed
            if ship.xv>-maxv:
                ship.xv = ship.xv - acceleration
            else:
                ship.xv = -maxv
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
                ship.xv = ship.xv - acceleration
            else:
                ship.xv = -maxv
            if ship.yv>-maxv:
                ship.yv = ship.yv - acceleration
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

        if keys[pygame.K_w] and not keys[pygame.K_a] and not keys[pygame.K_d] : #up exlusive
            #change in speed
            if ship.yv>-maxv:
                ship.yv = ship.yv - acceleration
            else:
                ship.yv = -maxv
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
                ship.xv = ship.xv + acceleration
            else:
                ship.xv = maxv
            if ship.yv>-maxv:
                ship.yv = ship.yv - acceleration
            else:
                ship.yv = -maxv
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

        if keys[pygame.K_d] and not keys[pygame.K_w] and not keys[pygame.K_s]: #right exlusive
            # change in speed
            if ship.xv<maxv:
                ship.xv = ship.xv + acceleration
            else:
                ship.xv = maxv
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
                ship.xv = ship.xv + acceleration
            else:
                ship.xv = maxv
            if ship.yv<maxv:
                ship.yv = ship.yv + acceleration
            else:
                ship.yv = maxv
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
        if keys[pygame.K_s] and not keys[pygame.K_a] and not keys[pygame.K_d]: #down
            # change in speed
            if ship.yv<maxv:
                ship.yv = ship.yv + acceleration
            else:
                ship.yv = maxv
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
            elif ship.rotation>pi/2 and ship.rotation<=3*pi/2:
                ship.rotation = ship.rotation - turnRate
            else: 
                print("error down key")
            
        if keys[pygame.K_a] and keys[pygame.K_s]: #left and down
            # change in speed
            if ship.xv>-maxv:
                ship.xv = ship.xv - acceleration
            else:
                ship.xv = -maxv
            if ship.yv<maxv:
                ship.yv = ship.yv + acceleration
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


        if  keys[pygame.K_SPACE]:
            direction = ship.rotation
            xb = ship.x + ship.radius*cos(direction)
            yb = ship.y + ship.radius*sin(direction)
            bulletlist.append(Bullet(xb, yb, direction))
            numBullets = numBullets + 1
            print("Active bullets:" + str(len(bulletlist)))
 

main()
