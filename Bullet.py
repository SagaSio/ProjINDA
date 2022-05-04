from math import cos
from math import sin
from math import pi
import pygame

## TODO: Expand class to be usable by both player and enemies. Collision should be exclusive, either enemy or player.
class Bullet:
    def __init__(self, x, y, v, direction):
        #Fix x and y after direction, velocity
        self.x = x
        self.y = y
        self.v = v
        self.direction = direction
        self.xv = cos(self.direction)*self.v
        self.yv = sin(self.direction)*self.v
        self.rotation = 0

    #Updates bullet and draws it each frame
    def draw(self, WINDOW):
        #Update x and y position of bullet with direction and velocity
        self.x = int(self.x + self.xv)
        self.y = int(self.y + self.yv)
        pygame.draw.circle(WINDOW, (255, 255, 255), (self.x, self.y), 5, 2)
   