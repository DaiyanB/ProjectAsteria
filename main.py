import pygame 
import numpy as np
from sys import exit
from math import radians
from random import randint

# from objects import Planet
from objects import planets, Constant, Scale, RocketSprite, PlanetSprite, Camera, RandomSurface
from objects import WIDTH, HEIGHT
from utils.utils import FPS
# from testing import planets
# from testing import WIDTH, HEIGHT

pygame.init()
 

WIN = pygame.display.set_mode((WIDTH, HEIGHT)) # window dimensions

# colours
WHITE = (255, 255, 255)
GREEN = (47, 237, 40)
# WIN = pygame.display.set_mode((0, 0))

fps = FPS()
scale = Scale()

# window icon and caption
pygame.display.set_icon(pygame.image.load('./ui/appicon.ico'))
pygame.display.set_caption("Mona")

# camera
camera_group = Camera()

for _ in range (2000):
    x = randint(0, 8000)
    y = randint(0, 3000)
    radius = randint(1, 10)

    RandomSurface((x, y), radius, WHITE, camera_group)

# rocket
rocket_group = pygame.sprite.GroupSingle()
rocket = RocketSprite([Constant.AU*2,0], [0,11208.25589], [0, 0], 1e3, WHITE, camera_group)
rocket_group.add(rocket)

planet_group = pygame.sprite.Group()
planet_group.add(PlanetSprite([0, 0], 24, 1.988892e30, 'sun', 'sprites\sprites\sun_sprite.png', camera_group))
planet_group.add(PlanetSprite([0.387*Constant.AU, 0], 8, 3.30e23, 'mercury', 'sprites\sprites\mercury_sprite.png', camera_group))
planet_group.add(PlanetSprite([0.723*Constant.AU, 0], 14, 4.8685e24, 'venus', r'sprites\sprites\venus_sprite.png', camera_group))
planet_group.add(PlanetSprite([-Constant.AU, 0], 16, 5.9742e24, 'earth', 'sprites\sprites\earth_sprite.png', camera_group))
planet_group.add(PlanetSprite([-1.524*Constant.AU, 0], 12, 6.39e23, 'mars', 'sprites\sprites\marsR_sprite.png', camera_group))



def main():
    boost_counter = 0
    n_counter = 0

    while True:
        WIN.fill((0, 0, 0)) # fills window with black

        fps.render(WIN, WIDTH) # renders window

        scale.render(WIN, WIDTH) # scales window

        # checks if keys are pressed that have actions associated with them
        # and then executes said actions
        # keys = pygame.key.get_pressed()
        
        # if keys[pygame.K_RIGHT]:
        #         planets[-1].rotate_force(0.2)
        
        # if keys[pygame.K_LEFT]:
        #     planets[-1].rotate_force(-0.2)

        # if keys[pygame.K_UP]:
        #     planets[-1].boost_break(1.5)

        # if keys[pygame.K_DOWN]:
        #     planets[-1].boost_break(-1.5)

        for event in pygame.event.get():
            # checks if window is closed
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
                # run = False

            if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_RIGHT:
            #         planets[-1].rotate_force(5)
    
            #     if event.key == pygame.K_o:
            #         if boost_counter % 2 == 0:
            #             planets[-1].booster(False)
            #         else:
            #             planets[-1].booster(True)

            #         boost_counter += 1  

            #     if event.key == pygame.K_n:
            #         if n_counter % 2 == 0:
            #             planets[-1].colour = GREEN
            #         else:
            #             planets[-1].colour = WHITE
            #         n_counter += 1

                if event.key == pygame.K_EQUALS:
                    Constant.SCALE *= 1.5
                
                if event.key == pygame.K_MINUS:
                    Constant.SCALE /= 1.5
                
                if event.key == pygame.K_r:
                    Constant.SCALE = 100/Constant.AU
  
    # for _ in range(10):
        # updates planet positions
        for planet in planets:
            # if not planet.sun:
            #     planet.update_position(planets)

            planet.update_position(planets)
            # planet.draw(WIN)

        # rocket.draw(WIN)
        # rocket.update(planets)
        # planet_group.draw(WIN)
        # planet_group.update(planets)
        camera_group.update(planets)
        camera_group.camera_draw(rocket)

        
        # obj.draw()

        pygame.display.update()
        
        # sets max framerate at 60 FPS
        fps.clock.tick(60)


main()