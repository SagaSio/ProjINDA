from math import cos
from math import sin
import pygame
import os

class Bullet:
    def __init__(self, x, y, v, direction, bullet_type):
        #Fix x and y after direction, velocity
        self.x = x
        self.y = y
        self.v = v
        self.direction = direction
        self.xv = cos(self.direction)*self.v
        self.yv = sin(self.direction)*self.v
        self.rotation = 0
        self.type = bullet_type
        
    #Updates bullet and draws it each frame
    def draw(self, WINDOW):
        #Update x and y position of bullet with direction and velocity
        self.x = int(self.x + self.xv)
        self.y = int(self.y + self.yv)
        if self.type == 0:
            pygame.draw.circle(WINDOW, (255, 255, 255), (self.x, self.y), 5, 2)
        else:
            pygame.draw.circle(WINDOW, (255, 0, 0), (self.x, self.y), 5, 2)
        
   