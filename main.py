import pygame 
import numpy as np
from sys import exit
from math import radians
from random import randint

# from objects import Planet
from objects import planets, Constant, Scale, RocketSprite, PlanetSprite, Camera, RandomSurface
from objects import WIDTH, HEIGHT
from utils.utils import FPS, generator
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

# stars
# for _ in range (2000):
#     x = randint(0, 8000)
#     y = randint(0, 3000)
#     radius = randint(1, 10)

#     RandomSurface((x, y), radius, WHITE, camera_group)

# planets
planet_group = pygame.sprite.Group()
planet_group.add(PlanetSprite([0, 0], 24, 1.988892e30, 'sun', 'sprites\sprites\sun_sprite.png', camera_group))
planet_group.add(PlanetSprite([0.387*Constant.AU, 0], 8, 3.30e23, 'mercury', 'sprites\sprites\mercury_sprite.png', camera_group))
planet_group.add(PlanetSprite([0.723*Constant.AU, 0], 14, 4.8685e24, 'venus', r'sprites\sprites\venus_sprite.png', camera_group))
planet_group.add(PlanetSprite([-Constant.AU, 0], 16, 5.9742e24, 'earth', 'sprites\sprites\earth_sprite.png', camera_group))
planet_group.add(PlanetSprite([-1.524*Constant.AU, 0], 12, 6.39e23, 'mars', 'sprites\sprites\marsR_sprite.png', camera_group))

# rocket
rocket_group = pygame.sprite.GroupSingle()
rocket = RocketSprite([Constant.AU*2,0], [0,11208.25589], [0, 0], 1e3, WHITE, camera_group)
rocket_group.add(rocket)
boost_counter = generator()
nuclear_counter = generator()

def main():
    while True:
        # fills window with black
        WIN.fill((0, 0, 0)) 

        for event in pygame.event.get():
            # checks if window is closed
            # ends program if it is
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # checks if keys are pressed that have actions associated with them
            # and then executes said actions
            if event.type == pygame.KEYDOWN:
                # exit via escape key
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
                    
                # resets zoom
                if event.key == pygame.K_r:
                    camera_group.zoom_scale = 1
                
                # turns booster on and off
                if event.key == pygame.K_o:
                    rocket.booster(next(boost_counter))

                # switches between the regular and nuclear rocket
                if event.key == pygame.K_n:
                    rocket.image = rocket.rocket_type[next(nuclear_counter)]
                
            # checks if the mousewheel has been used
            if event.type == pygame.MOUSEWHEEL:
                # increases zoom based on if the mouse wheel had been
                # moved up or down
                camera_group.zoom_scale += event.y * 0.05

                # sets bounds between 5 px per AU to 300 px per AU
                if camera_group.zoom_scale < 0.05: 
                    camera_group.zoom_scale = 0.05
                elif camera_group.zoom_scale > 3:
                    camera_group.zoom_scale = 3
        # for _ in range(2):
            # updates planet positions
        for planet in planets:
            # if not planet.sun:
            #     planet.update_position(planets)
            
            # updates position of planets
            planet.update_position(planets)
            # planet.draw(WIN)

        # updates position of sprite planets and draws them
        camera_group.update(planets)
        camera_group.camera_draw(rocket, fps, scale)

        pygame.display.update()
        
        # sets max framerate at 60 FPS
        fps.clock.tick(60)


main()