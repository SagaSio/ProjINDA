from math import cos
from math import sin
from math import pi
import math
import os

import pygame

class Ship:
    def __init__(self, x, y):
        # The ship stores its own position, velocity and rotation.
        self.x = x
        self.y = y
        self.radius = 30
        self.rotation = pi/2
        self.xv = 0
        self.yv = 0
        self.life = 10

        # Code for the healthbar
        self.lifeMax = 10
        self.healthbarLength = 400
        self.healthRatio = self.lifeMax / self.healthbarLength
        #Counters for main method
        self.score = 0
        self.enemiesHit = 0
        self.enemy_counter = 0
        # Allows us to draw the ship. These will be defined as we create the individual ships
        self.ship_img = pygame.image.load(os.path.join("assets", "SpaceShip.png"))
        self.rotated_ship = self.ship_img

    def drawHealthbar(self, WINDOW):
        # the red
        pygame.draw.rect(WINDOW, (255, 0, 0), (20, 10, self.life/ self.healthRatio, 25))
        # the white boundary
        pygame.draw.rect(WINDOW, (255, 255, 255), (20, 10, self.healthbarLength, 25), 2)


    # Drawing method. Draws on the surface "WINDOW"
    def draw(self, WINDOW):
        # Rate of slowdown for each frame
        acceleration = 0.1
        # update velocity
        if abs(self.xv)<=acceleration:
            self.xv = 0
        elif self.xv>0:
            self.xv = self.xv - acceleration
        else:
            self.xv = self.xv + acceleration
        if abs(self.yv)<=acceleration:
            self.yv = 0
        elif self.yv>0:
            self.yv = self.yv - acceleration
        else:
            self.yv = self.yv + acceleration

        #update x and y values by velocity
        self.x = int(round(self.x + self.xv))
        self.y = int(round(self.y + self.yv))
        #Rotates image to match rotation value
        self.rotated_ship = pygame.transform.rotate(self.ship_img, int((-math.degrees(self.rotation)-90)%360))
        rect = self.rotated_ship.get_rect()
        WINDOW.blit(self.rotated_ship, (self.x-rect.width/2, self.y-rect.height/2))
        pygame.draw.circle(WINDOW, (255, 255, 255), (int(self.x+self.radius*cos(self.rotation)), int(self.y+self.radius*sin(self.rotation))), 5, 2)