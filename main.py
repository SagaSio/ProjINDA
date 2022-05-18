
from dataclasses import dataclass
from math import atan2, sin, pi, cos, log
import math
import pygame
import os

from Bullet import *
from Ship import *
from Enemy import *
pygame.font.init()

WIDTH, HEIGHT = 1600, 900
os.environ['SDL_VIDEO_CENTERED'] = '1'
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

# Background
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "Background.png")), (WIDTH, HEIGHT))

def main():

    run = True

    # Constants
    dAngle = 1/math.sqrt(2)
    FPS = 60 
    num_bullets = 0
    main_font = pygame.font.SysFont("righteous", 30)

    # Player Settings
    maxv = 8
    acceleration = 0.3
    turnRate = pi/60
    lockTurn = False
    bulletvelocity = 20

    # Other settings

    # List for all player bullets
    numBullets = 0
    bulletlist = list()
    enemyBullets = list()

    amount_Time = 0


    

    

    # Creating a ship at middle of the screen
    ship = Ship(WIDTH/2, HEIGHT/2)
    enemies = []
    
    for i in range(20):
        enemies.append(Enemy(0))
        if i%5 == 0:
            ship.enemy_counter = ship.enemy_counter + 1
            enemies.append(Enemy(1))

    clock = pygame.time.Clock()

    # A function inside of the function
    def redraw_window():
        WINDOW.blit(BG, (0,0))

        # printing text
        num_bullets_label = main_font.render(f"BULLETS: {num_bullets}", 1, (255, 255, 255))
        player_life = main_font.render(f"LIVES: {ship.life}", 1, (255, 255, 255))
        num_Kills_label = main_font.render(f"KILLS: {ship.enemiesHit}", 1, (255, 255, 255))
        time_label = main_font.render(f"TIME: {amount_Time/1000}", 1, (255, 255, 255))
        score_label = main_font.render(f"SCORE: {ship.score}", 1, (255, 255, 255))

        WINDOW.blit(num_bullets_label, (20,50))
        WINDOW.blit(player_life, (20, 80))
        WINDOW.blit(num_Kills_label, (20, 110))
        WINDOW.blit(time_label, (20, 140))
        WINDOW.blit(score_label, (20, 170))

        # Spawn in new enemies
        if ship.enemy_counter < 5:
            enemies.append(Enemy(int(log(ship.score+10))))
            ship.enemy_counter = ship.enemy_counter + 1

        #Draw and handle logic for all enemies
        for enemy in enemies:
            
            #Remove enemy with 0 or less HP
            if enemy.life <= 0:
                if enemy.type > 0:
                    ship.life = min(ship.life+1, 10)
                    ship.score = ship.score + 10*enemy.type
                    ship.enemiesHit = ship.enemiesHit + 1
                    ship.enemy_counter = ship.enemy_counter - 1
                enemies.remove(enemy)
                

            #Collision check with player
            #distance between center of enemy and player is less than combined radius.
            if sqrt(pow(enemy.x-ship.x,2) + pow(enemy.y-ship.y,2)) <= (enemy.radius + ship.radius):

                #Calculate the collision angle
                collision_angle = atan2(enemy.yv-ship.yv, enemy.xv-ship.xv)

                #Increase amount of collisions
                ship.enemiesHit = ship.enemiesHit + 1

                print(collision_angle)
                #Update velocity
                enemy.xv = (enemy.xv-ship.xv) * 0.5*-enemy.radius/ship.radius
                enemy.yv = (enemy.yv-ship.yv) * 0.5*-enemy.radius/ship.radius
                enemy.life = enemy.life-1

                ship.xv = -ship.xv*0.5
                ship.yv = -ship.yv*0.5

                ship.life = ship.life-1

            #Handle enemy shooting bullets.
            if enemy.type > 0 and enemy.bulletCooldown <=0:
                enemyBullets.append(Bullet(enemy.x + enemy.radius*cos(enemy.rotation), enemy.y + enemy.radius*sin(enemy.rotation), 3*enemy.type, enemy.rotation, 1))
                enemy.bulletCooldown = int(300/enemy.type)

            #Player bullet collision check here
            for bullet in bulletlist:
                if sqrt(pow(enemy.x-bullet.x,2) + pow(enemy.y-bullet.y,2)) <= enemy.radius:
                    enemy.life = enemy.life - 2
                    bulletlist.remove(bullet) 

            #Draw each enemy
            enemy.draw(WINDOW,ship)


        # The ship will call its own draw method
        ship.draw(WINDOW)

        # Calls the health bar method
        ship.drawHealthbar(WINDOW)

        #Draw all bullets on screen
        for i in bulletlist:
            if abs(i.x-ship.x) < 3000 and abs(i.y-ship.y) < 3000:
                i.draw(WINDOW)
            else:
                bulletlist.remove(i)
        for j in enemyBullets:
            if abs(j.x-WIDTH/2) < WIDTH/2 and abs(j.y-HEIGHT/2) < HEIGHT/2:
                j.draw(WINDOW)
            else:
                enemyBullets.remove(j)
                
        for k in enemyBullets:
            if sqrt(pow(ship.x-k.x,2) + pow(ship.y-k.y,2)) <= ship.radius:
                ship.life = ship.life - 1
                enemyBullets.remove(k)

        pygame.display.update()

        #Draw other collidable objects in a loop here. Enemies, asteroids etc. 

    while run:
        clock.tick(FPS)
        amount_Time = amount_Time + clock.get_time()
        redraw_window()

        if ship.life <= 0:
            GAMEOVER(numBullets, ship.score, amount_Time, ship.enemiesHit)  

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # This is not positioned in the for loop above so that 
        # multiple keys can be pressed at the same time
        keys = pygame.key.get_pressed()

        # List of available key presses:
        #  WASD, 1, SPACE, RETURN
        if keys[pygame.K_a] and not keys[pygame.K_w] or keys[pygame.K_a] and not keys[pygame.K_s]: #left exlusive
            # change in speed
            if ship.xv>-maxv:
                ship.xv = ship.xv - acceleration
            else:
                ship.xv = -maxv
            if not lockTurn:
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
                ship.xv = ship.xv - acceleration*dAngle
            else:
                ship.xv = -maxv
            if ship.yv>-maxv:
                ship.yv = ship.yv - acceleration*dAngle
            else: 
                ship.yv = -maxv
            if not lockTurn:
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

        if keys[pygame.K_w] and not keys[pygame.K_a] or keys[pygame.K_w] and not keys[pygame.K_d] : #up exlusive
            #change in speed
            if ship.yv>-maxv:
                ship.yv = ship.yv - acceleration
            else:
                ship.yv = -maxv
            if not lockTurn:
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
                ship.xv = ship.xv + acceleration*dAngle
            else:
                ship.xv = maxv
            if ship.yv>-maxv:
                ship.yv = ship.yv - acceleration*dAngle
            else:
                ship.yv = -maxv
            if not lockTurn:
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

        if keys[pygame.K_d] and not keys[pygame.K_w] or keys[pygame.K_d] and not keys[pygame.K_s]: #right exlusive
            # change in speed
            if ship.xv<maxv:
                ship.xv = ship.xv + acceleration
            else:
                ship.xv = maxv
            if not lockTurn:
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
                ship.xv = ship.xv + acceleration*dAngle
            else:
                ship.xv = maxv
            if ship.yv<maxv:
                ship.yv = ship.yv + acceleration*dAngle
            else:
                ship.yv = maxv
            if not lockTurn:
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

        if keys[pygame.K_s] and not keys[pygame.K_a] or keys[pygame.K_s] and not keys[pygame.K_d]: #down exclusive
            # change in speed
            if ship.yv<maxv:
                ship.yv = ship.yv + acceleration
            else:
                ship.yv = maxv
            if not lockTurn:
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
                elif ship.rotation>=pi/2 and ship.rotation<=3*pi/2:
                    ship.rotation = ship.rotation - turnRate
                else: 
                    print("error down key")
            
        if keys[pygame.K_a] and keys[pygame.K_s]: #left and down
            # change in speed
            if ship.xv>-maxv:
                ship.xv = ship.xv - acceleration*dAngle
            else:
                ship.xv = -maxv
            if ship.yv<maxv:
                ship.yv = ship.yv + acceleration*dAngle
            else:
                ship.yv = maxv
            if not lockTurn:
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
                else:
                    print("Error left down")      

        # Shoots bullets
        if  keys[pygame.K_SPACE]:
            direction = ship.rotation
            xb = ship.x + ship.radius*cos(direction)
            yb = ship.y + ship.radius*sin(direction)
            bulletlist.append(Bullet(xb, yb, bulletvelocity, direction, 0))
            numBullets = numBullets + 1
            num_bullets += 1
            print("Active bullets:" + str(len(bulletlist)))
        
        # Resets player position
        if keys[pygame.K_RETURN]:
            ship.x = WIDTH/2
            ship.y = HEIGHT/2
        # Prints player position
        if keys[pygame.K_1]:
            print("X:" + str(ship.x) + " Y:" +str(ship.y))
        #Locks rotation
        if keys[pygame.K_o]:
            lockTurn = True
        else:
            lockTurn = False
        #locks position
        if keys[pygame.K_p]:
            if abs(ship.xv)<1:
                ship.xv = 0
            else:
                ship.xv = ship.xv * 0.98

            if abs(ship.yv)<1:
                ship.yv = 0
            else:
                ship.yv = ship.yv * 0.98


# Creates the home screen

def home():
    large_font = pygame.font.SysFont("righteous", 200)
    home_font = pygame.font.SysFont("righteous", 60)
    run = True
    while run:
        WINDOW.blit(BG, (0,0))
        home_text = home_font.render("PRESS THE MOUSE TO BEGIN", 1, (255, 255, 255))
        WINDOW.blit(home_text, (int(WIDTH/2 - home_text.get_width()/2), 550))

        home_text2 = large_font.render("SPACE INVADERS", 1, (255, 255, 255))
        WINDOW.blit(home_text2, (int(WIDTH/2 - home_text2.get_width()/2), 280))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                main()
                run = False
            
    pygame.quit()

def GAMEOVER(bullets, score, time, collisions):
    GAMEOVER_font = pygame.font.SysFont("righteous", 200)
    medium_font = pygame.font.SysFont("righteous", 75)
    smaller_font = pygame.font.SysFont("righteous", 25)
    smallest_font = pygame.font.SysFont("righteous", 20)
    run = True
    while run:
        WINDOW.blit(BG, (0,0))
        GAMEOVER_text = GAMEOVER_font.render("GAME OVER", 1, (255, 255, 255))
        WINDOW.blit(GAMEOVER_text, (int(WIDTH/2 - GAMEOVER_text.get_width()/2), 100))

        retry_text = medium_font.render("PRESS THE MOUSEBUTTON TO RESTART", 1, (255, 255, 255))
        WINDOW.blit(retry_text, (int(WIDTH/2 - retry_text.get_width()/2), 320))

        bullets_text = smaller_font.render("AMOUNT OF BULLETS: " + str(bullets), 1, (255, 255, 255))
        WINDOW.blit(bullets_text, (int(WIDTH/2 - bullets_text.get_width()/2), 450))

        kills_text = smaller_font.render("TOTAL SCORE: " + str(score), 1, (255, 255, 255))
        WINDOW.blit(kills_text, (int(WIDTH/2 - kills_text.get_width()/2), 485))
        
        time_text = smaller_font.render("TIME SURVIVED: " + str(time/1000) + "s", 1, (255, 255, 255))
        WINDOW.blit(time_text, (int(WIDTH/2 - time_text.get_width()/2), 515))

        collision_text = smaller_font.render("AMOUNT OF COLLISIONS: " + str(collisions), 1, (255, 255, 255))
        WINDOW.blit(collision_text, (int(WIDTH/2 - collision_text.get_width()/2), 545))

        producer_text = smallest_font.render("PRODUCED AND DESIGNED BY ", 1, (255, 255, 255))
        WINDOW.blit(producer_text, (int(WIDTH/2 - producer_text.get_width()/2), 610))

        producer_text2 = smallest_font.render("KALLE ANDERSSON & SAGA SIÖSTEEN", 1, (255, 255, 255))
        WINDOW.blit(producer_text2, (int(WIDTH/2 - producer_text2.get_width()/2), 625))

        producer_text3 = smallest_font.render("ALL RIGHTS RESERVED", 1, (255, 255, 255))
        WINDOW.blit(producer_text3, (int(WIDTH/2 - producer_text3.get_width()/2), 640))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                main()
                run = False
            
    pygame.quit()


home()
