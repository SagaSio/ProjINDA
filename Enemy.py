import math
from numpy import arctan
from random import choice, randint
import pygame
import os
from math import atan2, cos
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
        self.x = WIDTH/2 + randint(1000, 1500)*cos(spawnangle)
        self.y = HEIGHT/2 + randint(500, 1000)*sin(spawnangle)
        self.direction = 2*arctan((randx-self.x)/(randy-self.y)+ 0.000023)
        self.type = enemy_type
        #Spawns an asteroid
        if(enemy_type < 1):
            self.velocity = choice([1.5,2,3,4])

            #Vary size and radius here
            self.life = max(20, abs(enemy_type)*20)
            self.radius = 30
            self.sprite = pygame.image.load(os.path.join("assets", "Asteroid.png"))
        #Spawns a ship. Higher type number creates a stronger enemy    
        else:
            self.life = 5*enemy_type
            self.velocity = max(1, 0.6*enemy_type)
            self.radius = 30
            #Add sprite
            self.sprite = pygame.image.load(os.path.join("assets", "EnemyShip.png"))
            self.bulletCooldown = 0
        self.rotated_ship = self.sprite
        self.rotation = pi/2
        self.xv = self.velocity*cos(self.direction)
        self.yv = self.velocity*sin(self.direction)

    # Drawing method. Draws on the surface "WINDOW"
    def draw(self, WINDOW, ship):
        if sqrt(pow(WIDTH/2-self.x, 2) + pow(HEIGHT/2-self.y, 2)) > 1000:
            randx = randint(int(WIDTH/4), int(6*WIDTH/8))
            randy = randint(int(HEIGHT/4), int(6*HEIGHT/8))
            spawnangle = randint(0, 359)*pi/180
            self.x = WIDTH/2 + randint(1000,1500)*cos(spawnangle)
            self.y = HEIGHT/2 + randint(500,1000)*sin(spawnangle)
            self.direction = 2*arctan(randx-self.x/randy-self.y + 0.000023)
        #For asteroids
        if self.type < 1:
            self.x = self.x + self.xv
            self.y = self.y + self.yv
            WINDOW.blit(self.sprite, (int(round(self.x-self.radius/2)), int(round(self.y-self.radius/2))))
        #For enemy ships
        else:
            self.rotated_ship = pygame.transform.rotate(self.sprite, int((-math.degrees(self.rotation)-90)%360))
            self.rotation = atan2(ship.y-self.y, ship.x-self.x)
            self.bulletCooldown = self.bulletCooldown - 1
            self.x = self.x + self.xv
            self.y = self.y + self.yv
            WINDOW.blit(self.rotated_ship, (int(round(self.x-self.radius/2)), int(round(self.y-self.radius/2))))

