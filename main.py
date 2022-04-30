from math import sin
from math import pi
from math import cos
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
        self.v = 10
        self.rotation = 0
        self.direction = direction
    
    def draw(self, WINDOW):
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
        # Allows us to draw the ship. These will be defined as we create the individual ships
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.bullet_Pause = 0
     
    # Adding methods

    # Drawing method. Draws on the surface "WINDOW"
    def draw(self, WINDOW):
        pygame.draw.circle(WINDOW, (255, 0, 0), (self.x, self.y), self.radius)
        pygame.draw.circle(WINDOW, (255, 255, 255), (int(self.x+self.radius*cos(self.rotation)), int(self.y+self.radius*sin(self.rotation))), 5)


# To be used later
# Class that inherits from Ship
# class Player(Ship)

def main():
    run = True
    # Frames per second
    FPS = 60 

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
        if keys[pygame.K_a] and ship.x - player_vel > 30: #left
            ship.x -= player_vel
            ship.rotation = pi
            
        if keys[pygame.K_d] and ship.x - player_vel + 30 < WIDTH: #right
            ship.x += player_vel
            ship.rotation = 0

        if keys[pygame.K_w] and ship.y - player_vel > 30: #up
            ship.y -= player_vel
            ship.rotation = 3*pi/2

        if keys[pygame.K_s] and ship.y + player_vel + 30 < HEIGHT: #down
            ship.y += player_vel
            ship.rotation = pi/2

        if keys[pygame.K_SPACE]:
            direction = ship.rotation
            xb = ship.x + ship.radius*cos(direction)
            yb = ship.y + ship.radius*sin(direction)
            bulletlist.append(Bullet(xb, yb, direction))
            numBullets = numBullets + 1
            print(numBullets)
            print(len(bulletlist))
 

main()
