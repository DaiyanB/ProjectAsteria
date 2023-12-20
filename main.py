import pygame 
import numpy as np
from sys import exit
from math import radians
from random import randint

# from objects import Planet
from objects import planets, Constant, Scale, RocketSprite, PlanetSprite, Camera, RandomSurface
from objects import WIDTH, HEIGHT
from button import Button
from utils.utils import FPS, generator
from utils.variables import control_list
# from testing import planets
# from testing import WIDTH, HEIGHT

pygame.init()
 

screen = pygame.display.set_mode((WIDTH, HEIGHT)) # window dimensions

# colours
WHITE = (255, 255, 255)
GREEN = (47, 237, 40)
# WIN = pygame.display.set_mode((0, 0))

# fps and scale classes
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
rocket = RocketSprite([Constant.AU*2,0], [0,11208.25589], 100, 1e5, WHITE, camera_group)
rocket_group.add(rocket)
boost_counter = generator()
nuclear_counter = generator()

screen = pygame.display.set_mode((HEIGHT, WIDTH))

# game variables
game_state = 0 # defines possible game states between 0, 1, and 2

font = pygame.font.SysFont('Inter', 30, True)
font40 = pygame.font.SysFont('Inter', 40, True)
font16 = pygame.font.SysFont('Inter', 16, False)
text_col = (255, 255, 255)

# logo
logo = pygame.image.load('./logo/horizontal_logo.png').convert_alpha()
logo = pygame.transform.rotozoom(logo, 0, 0.5)
logo_rect = logo.get_rect(center = (450, 250))

# buttons
play = Button('Play', font, 200, 40, (350, 350), 6)
controls_button = Button('Controls', font, 200, 40, (350, 450), 6)
exit_button = Button('Exit', font, 200, 40, (350, 550), 6)
back_button = Button('Back', font, 200, 40, (660, 820), 6)

# control text
control_surf = [font16.render(i, True, 'white') for i in control_list]
control_rect = [control_surf[j].get_rect(topleft = (40, 140 + (1.6)*j)) for j in range(len(control_list))]

# def main():
while True:
    print(controls_button.action)
    # fills window with black

    if game_state == 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        
        screen.fill('#1a1a1a') 

        # draws buttons
        play.draw(screen)
        controls_button.draw(screen)
        exit_button.draw(screen)

        # draws logo
        screen.blit(logo, logo_rect)

        # checks if a button been pressed and 
        # executes the associated action
        if play.action == True:
            game_state = 1
            print(game_state)

        if controls_button.action == True:
            game_state = 2
            controls_button.action = False

        if exit_button.action == True:
            pygame.quit()
            exit()
            
    elif game_state == 1:
        screen.fill('black')
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
        
        # updates position of planets
        for planet in planets:            
            planet.update_position(planets)

        # updates position of sprite planets and draws them
        camera_group.update(planets)
        camera_group.camera_draw(rocket, fps, scale)
    
    elif game_state == 2:
        screen.fill('#1a1a1a') 
        for event in pygame.event.get():
            # checks if window is closed
            # ends program if it is
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        control_title_surf = font.render('Controls', True, 'white')
        control_title_rect = control_title_surf.get_rect(topleft = (40, 40))
        # control_text_surf = font.render(control_text, True, 'white')
        # control_text_rect = control_text_surf.get_rect(topleft = (30, 130))

        screen.blit(control_title_surf, control_title_rect)

        for idx, surf in enumerate(control_surf):
            rect = control_rect[idx]
            screen.blit(surf, rect)

        back_button.draw(screen)

        if back_button.action == True:
            game_state = 0
            back_button.action = False
        

        # screen.blit(control_text_surf, control_text_rect)
        

    pygame.display.update()
    
    # sets max framerate at 60 FPS
    fps.clock.tick(60)


# main()