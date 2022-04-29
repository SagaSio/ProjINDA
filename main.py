import pygame
import os
import time
import random
pygame.font.init()

WIDTH, HEIGHT = 750, 750
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


# An abstract class. Won't be used in itself but inherited from!
class Ship:
    def __init__(self, x, y):
        # The ship stores its own position
        self.x = x
        self.y = y 
        # Allows us to draw the ship. These will be defined as we create the individual ships
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.bullet_Pause = 0

    # Adding methods

    # Drawing method. Draws on the surface "WINDOW"
    def draw(self, WINDOW):
        pygame.draw.circle(WINDOW, (255, 0, 0), (self.x, self.y), 30)

def main():
    run = True
    # Frames per second
    FPS = 60 

    # Velocty for player
    player_vel = 5

    # Creating a ship at bottom of the screen
    ship = Ship(300, 650)

    clock = pygame.time.Clock()

    # A function inside of the function
    def redraw_window():
        WINDOW.blit(BG, (0,0))

        # The ship will call its own draw method
        ship.draw(WINDOW)

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

        if keys[pygame.K_a]: #left
            ship.x -= player_vel 
        if keys[pygame.K_d]: #right
            ship.x += player_vel
        if keys[pygame.K_w]: #up
            ship.y -= player_vel
        if keys[pygame.K_s]: #down
            ship.y += player_vel

main()
