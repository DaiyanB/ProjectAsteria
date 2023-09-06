import pygame 
from math import radians

# from objects import Planet
from objects import planets, Constant, scale
from objects import WIDTH, HEIGHT
from utils.utils import FPS
# from testing import planets
# from testing import WIDTH, HEIGHT

pygame.init()
 

WIN = pygame.display.set_mode((WIDTH, HEIGHT))

WHITE = (255, 255, 255)
GREEN = (47, 237, 40)
# WIN = pygame.display.set_mode((0, 0))
pygame.display.set_icon(pygame.image.load('./ui/appicon.ico'))
pygame.display.set_caption("Mona")

fps = FPS()
Scale = scale()

def main():
    run = True

    boost_counter = 0

    n_counter = 0

    while run:
        WIN.fill((0, 0, 0))

        fps.render(WIN, WIDTH)

        Scale.render(WIN, WIDTH)

        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_RIGHT]:
            planets[-1].rotate_force(0.2)
        
        if keys[pygame.K_LEFT]:
            planets[-1].rotate_force(-0.2)

        if keys[pygame.K_UP]:
            planets[-1].boost_break(1.5)

        if keys[pygame.K_DOWN]:
            planets[-1].boost_break(-1.5)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_RIGHT:
            #         planets[-1].rotate_force(5)
    
                if event.key == pygame.K_o:
                    if boost_counter % 2 == 0:
                        planets[-1].booster(False)
                    else:
                        planets[-1].booster(True)

                    boost_counter += 1  

                if event.key == pygame.K_n:
                    if n_counter % 2 == 0:
                        planets[-1].colour = GREEN
                    else:
                        planets[-1].colour = WHITE
                    n_counter += 1

                if event.key == pygame.K_EQUALS:
                    Constant.SCALE *= 1.5
                
                if event.key == pygame.K_MINUS:
                    Constant.SCALE /= 1.5
                
                if event.key == pygame.K_r:
                    Constant.SCALE = 100/Constant.AU



                            
    # for _ in range(10):
        for planet in planets:
            # if not planet.sun:
            #     planet.update_position(planets)

            planet.update_position(planets)
            planet.draw(WIN)

        

        pygame.display.update()
        
        fps.clock.tick(60)

    pygame.quit()

main()
