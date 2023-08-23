import pygame 
# import math

# from objects import Planet
from objects import planets
from objects import WIDTH, HEIGHT

# from testing import planets
# from testing import WIDTH, HEIGHT

pygame.init()
 

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
# WIN = pygame.display.set_mode((0, 0))
pygame.display.set_icon(pygame.image.load('./ui/appicon.ico'))
pygame.display.set_caption("Mona")

def main():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        WIN.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN)

        pygame.display.update()
        
    pygame.quit()

main()