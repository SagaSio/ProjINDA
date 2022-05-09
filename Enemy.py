from turtle import width
import pygame
import os
from math import pi

WIDTH, HEIGHT = 1280, 720

class Enemy:
    def __init__(self, x, y):
        # The ship stores its own position, velocity and rotation.
        self.x = x
        self.y = y
        self.radius = 30
        self.rotation = pi/2
        self.xv = 0
        self.yv = 0
        self.asteroid = pygame.image.load(os.path.join("assets", "Asteroid.png"))
     
    # Adding methods

    # Drawing method. Draws on the surface "WINDOW"
    def draw(self, WINDOW):

        WINDOW.blit(self.asteroid, (self.x, self.y))


    def moveDown(self, velocity):
        if self.y > HEIGHT - 100 and velocity > 0:
            velocity *= -1
        
        self.y += velocity

        
        

    def moveRight(self, velocity):
        #self.y += velocity
        self.x += velocity

    def moveLeft(self, velocity):
        #self.y -= velocity
        self.x -= velocity

    def moveUp(self, velocity):
        self.y -= velocity
        #self.x -= velocity