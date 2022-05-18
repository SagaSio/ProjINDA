from math import cos
from math import sin
from math import pi
import pygame
import os

## TODO: Expand class to be usable by both player and enemies. Collision should be exclusive, either enemy or player.
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
        # if-sats här gällande vilken bullet-typ
        if bullet_type < 0:
            self.bullet_img = pygame.image.load(os.path.join("assets", "ShipBullet.png"))
        else:
            self.bullet_img = pygame.image.load(os.path.join("assets", "EnemyBullet.png"))
        

    #Updates bullet and draws it each frame
    def draw(self, WINDOW):
        #Update x and y position of bullet with direction and velocity
        self.x = int(self.x + self.xv)
        self.y = int(self.y + self.yv)
        if self.type == 0:
            pygame.draw.circle(WINDOW, (255, 255, 255), (self.x, self.y), 5, 2)
        else:
            pygame.draw.circle(WINDOW, (255, 0, 0), (self.x, self.y), 5, 2)
        
   