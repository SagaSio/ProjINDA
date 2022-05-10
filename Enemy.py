from numpy import arctan
from random import choice, randint
import pygame
import os
from math import cos
from math import sin
from math import pi
from math import pow
from math import sqrt

WIDTH, HEIGHT = 1600, 900

class Enemy:
    def __init__(self, enemy_type):
        # The ship stores its own position, velocity and rotation.
        randx = randint(int(WIDTH/8), int(7*WIDTH/8))
        randy = randint(int(HEIGHT/8), int(7*HEIGHT/8))
        
        spawnangle = randint(0, 359)*pi/180
        self.x = WIDTH/2 + randint(1500, 2000)*cos(spawnangle)
        self.y = HEIGHT/2 + randint(1500, 2000)*sin(spawnangle)
        self.direction = 2*arctan((randx-self.x)/(randy-self.y)+ 0.000023)
        self.type = enemy_type
        if(enemy_type < 1):
            self.velocity = choice([1.5,2,3,4])

            #Vary size and radius here
            self.life = max(20, abs(enemy_type)*20)
            self.radius = 30
            self.sprite = pygame.image.load(os.path.join("assets", "Asteroid.png"))
        else:
            self.velocity = enemy_type
            self.radius = 30
            #Add sprite
        self.rotation = pi/2
        self.xv = self.velocity*cos(self.direction)
        self.yv = self.velocity*sin(self.direction)
        
     
    # Adding methods

    # Drawing method. Draws on the surface "WINDOW"
    def draw(self, WINDOW):
        if sqrt(pow(WIDTH/2-self.x, 2) + pow(HEIGHT/2-self.y, 2)) > 2000:
            randx = randint(int(WIDTH/4), int(6*WIDTH/8))
            randy = randint(int(HEIGHT/4), int(6*HEIGHT/8))
            spawnangle = randint(0, 359)*pi/180
            self.x = WIDTH/2 + randint(1500,2000)*cos(spawnangle)
            self.y = HEIGHT/2 + randint(1500,2000)*sin(spawnangle)
            self.direction = 2*arctan(randx-self.x/randy-self.y + 0.000023)

        if self.type < 1:
            self.x = self.x + self.xv
            self.y = self.y + self.yv
            WINDOW.blit(self.sprite, (int(round(self.x-self.radius/2)), int(round(self.y-self.radius/2))))
        else:
            pass


