import pygame 
from sys import exit

from objects import Button, Camera, Constant, OrbitalTrail, Planet, PlanetSprite, RocketSprite, Scale
from utils import FPS, Timestep, generator, rocket_list, misc_list

# window dimensions
WIDTH, HEIGHT = 900, 900

# initialising pygame
pygame.init()

# creating screen surface
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# colours
WHITE = (255, 255, 255)
GREEN = (47, 237, 40)
MONA_PURPLE = (136, 0, 231)
# WIN = pygame.display.set_mode((0, 0))

# fps and scale classes
constant = Constant()
fps = FPS()
scale = Scale(constant)

# timestep (duh)
ORIGINAL_TIMESTEP = 86400/2
timestep = Timestep(ORIGINAL_TIMESTEP)

# window icon and caption
pygame.display.set_icon(pygame.image.load('./ui/appicon.ico'))
pygame.display.set_caption("Mona")

# camera
camera_group = Camera(constant)

# stars
# for _ in range (2000):
#     x = randint(0, 8000)
#     y = randint(0, 3000)
#     radius = randint(1, 10)

#     RandomSurface((x, y), radius, WHITE, camera_group)

# planets
# planet_group = pygame.sprite.Group()
# planet_group.add(PlanetSprite([0, 0], 24, 1.988892e30, 'sun', timestep, 'sprites\sprites\sun_sprite.png', camera_group))
# planet_group.add(PlanetSprite([0.387*Constant.AU, 0], 8, 3.30e23, 'mercury', timestep, 'sprites\sprites\mercury_sprite.png', camera_group))
# planet_group.add(PlanetSprite([0.723*Constant.AU, 0], 14, 4.8685e24, 'venus', timestep, r'sprites\sprites\venus_sprite.png', camera_group))
# planet_group.add(PlanetSprite([-Constant.AU, 0], 16, 5.9742e24, 'earth', timestep, 'sprites\sprites\earth_sprite.png', camera_group))
# planet_group.add(PlanetSprite([-1.524*Constant.AU, 0], 12, 6.39e23, 'mars', timestep, 'sprites\sprites\marsR_sprite.png', camera_group))

# sun = Planet([0, 0], 24, 1.988892e30, 'sun', timestep)
# sun.sun = True

# mercury = Planet([0.387*Constant.AU, 0], 8, 3.30e23, 'mercury', timestep)
# venus = Planet([0.723*Constant.AU, 0], 14, 4.8685e24, 'venus', timestep)
# earth = Planet([-Constant.AU, 0], 16, 5.9742e24, 'earth', timestep)
# mars = Planet([-1.524*Constant.AU, 0], 12, 6.39e23, 'mars', timestep)

planet_group = pygame.sprite.Group()

# sun = Planet([0, 0], 24, 1.988892e30, 'sun', timestep)
# sun.sun = True

# mercury = Planet([0.387*Constant.AU, 0], 8, 3.30e23, 'mercury', timestep)
# venus = Planet([0.723*Constant.AU, 0], 14, 4.8685e24, 'venus', timestep)
# earth = Planet([-Constant.AU, 0], 16, 5.9742e24, 'earth', timestep)
# mars = Planet([-1.524*Constant.AU, 0], 12, 6.39e23, 'mars', timestep)

sun = PlanetSprite([0, 0], 24, 1.988892e30, 'sun', timestep, 'sprites\sprites\sun_sprite.png', camera_group)
mercury = PlanetSprite([0.387*Constant.AU, 0], 8, 3.30e23, 'mercury', timestep, 'sprites\sprites\mercury_sprite.png', camera_group)
venus = PlanetSprite([0.723*Constant.AU, 0], 14, 4.8685e24, 'venus', timestep, r'sprites\sprites\venus_sprite.png', camera_group)
earth = PlanetSprite([-Constant.AU, 0], 16, 5.9742e24, 'earth', timestep, 'sprites\sprites\earth_sprite.png', camera_group)
mars = PlanetSprite([-1.524*Constant.AU, 0], 12, 6.39e23, 'mars', timestep, 'sprites\sprites\marsR_sprite.png', camera_group)

planet_group = pygame.sprite.Group()

planets = [sun, mercury, venus, earth, mars]

for i in planets:
    planet_group.add(i)


# rocket
rocket_group = pygame.sprite.GroupSingle()
rocket = RocketSprite([Constant.AU*2,0], [0,11208.25589], 1e2, 1e5, timestep, WHITE, constant, camera_group)
rocket_group.add(rocket)
boost_counter = generator()
nuclear_counter = generator()

planets.append(rocket)

# # orbital trail
# orbital_trail_group = pygame.sprite.Group()

# for planet in planets:
#     orbital_trail_group.add(OrbitalTrail(planet, constant.record_scale, camera_group))

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
home_button = Button('', font, 40, 40, (20, 840), 6, ['assets\home_normal.png', 'assets\home_hover.png'], 40/2400)

# control text
rocket_surf = [font16.render(i, True, 'white') for i in rocket_list]
rocket_rect = [rocket_surf[j].get_rect(topleft = (40, 160 + (16 + 5)*j)) for j in range(len(rocket_list))]
rocket_end = len(rocket_rect)*(16+5) + 180

# misc text
misc_surf = [font16.render(k, True, 'white') for k in misc_list]
misc_rect = [misc_surf[t].get_rect(topleft = (40, rocket_end + 20 + 40 + (16 + 5)*t)) for t in range(len(misc_list))]

# creates text surfaces for the controls
control_title_surf = font40.render('Controls', True, 'white')
control_title_rect = control_title_surf.get_rect(topleft = (40, 40))

rocket_title_surf = font.render('Rocket controls', True, '#8800e7')
rocket_title_rect = rocket_title_surf.get_rect(topleft = (40, 120))

misc_title_surf = font.render('Misc', True, '#8800e7')
misc_title_rect = misc_title_surf.get_rect(topleft = (40, rocket_end + 20))


# main loop
while True:
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
            play.action = False
            print(game_state)

        if controls_button.action == True:
            game_state = 2
            controls_button.action = False

        if exit_button.action == True:
            print('exit')
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
                    index = next(nuclear_counter)
                    rocket.image = rocket.rocket_type[index]
                    rocket.colour = rocket.colours[index]
                
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

                constant.update_scale(camera_group.zoom_scale)
        
        # updates position of planets
        # for planet in planets:            
        #     planet.update_position(planets)

        # updates position of sprite planets and draws them
        camera_group.update(planets)
        camera_group.camera_draw(rocket, fps, scale)

        home_button.draw(screen)

        if home_button.action:
            game_state = 0
            home_button.action = False

            # reinitialises everything

            # empties camera group
            camera_group.empty()

            # planets
            planet_group.add(PlanetSprite([0, 0], 24, 1.988892e30, 'sun', timestep, 'sprites\sprites\sun_sprite.png', camera_group))
            planet_group.add(PlanetSprite([0.387*Constant.AU, 0], 8, 3.30e23, 'mercury', timestep, 'sprites\sprites\mercury_sprite.png', camera_group))
            planet_group.add(PlanetSprite([0.723*Constant.AU, 0], 14, 4.8685e24, 'venus', timestep, r'sprites\sprites\venus_sprite.png', camera_group))
            planet_group.add(PlanetSprite([-Constant.AU, 0], 16, 5.9742e24, 'earth', timestep, 'sprites\sprites\earth_sprite.png', camera_group))
            planet_group.add(PlanetSprite([-1.524*Constant.AU, 0], 12, 6.39e23, 'mars', timestep, 'sprites\sprites\marsR_sprite.png', camera_group))
            
            sun = Planet([0, 0], 24, 1.988892e30, 'sun', timestep)
            sun.sun = True

            mercury = Planet([0.387*Constant.AU, 0], 8, 3.30e23, 'mercury', timestep)
            venus = Planet([0.723*Constant.AU, 0], 14, 4.8685e24, 'venus', timestep)
            earth = Planet([-Constant.AU, 0], 16, 5.9742e24, 'earth', timestep)
            mars = Planet([-1.524*Constant.AU, 0], 12, 6.39e23, 'mars', timestep)

            planets = [sun, mercury, venus, earth, mars]

            # empties rocket group
            rocket_group.empty()

            # reinitialises rocket
            rocket = RocketSprite([Constant.AU*2,0], [0,11208.25589], 100, 1e5, timestep, WHITE, camera_group)
            rocket_group.add(rocket)
            boost_counter = generator()
            nuclear_counter = generator()    

            # resets timestep
            timestep.reset()
    
    elif game_state == 2:
        screen.fill('#1a1a1a') 
        for event in pygame.event.get():
            # checks if window is closed
            # ends program if it is
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # draws titles
        screen.blit(control_title_surf, control_title_rect)
        screen.blit(rocket_title_surf, rocket_title_rect)
        screen.blit(misc_title_surf, misc_title_rect)

        # draws the actual text
        for idx, surf in enumerate(rocket_surf):
            rect = rocket_rect[idx]
            screen.blit(surf, rect)

        for idx, surf in enumerate(misc_surf):
            rect = misc_rect[idx]
            screen.blit(surf, rect)

        # draws back button
        back_button.draw(screen)

        if back_button.action == True:
            game_state = 0
            back_button.action = False
        

        # screen.blit(control_text_surf, control_text_rect)
        
    # updates display    
    pygame.display.update()
    
    # sets max framerate at 60 FPS
    fps.clock.tick(60)


# main()