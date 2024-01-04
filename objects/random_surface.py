import numpy as np
from numpy.linalg import norm

import pygame, math
from pygame import gfxdraw
from math import sin, cos, atan2, degrees, radians

# from pygame.sprite import _Group

pygame.font.init()
pygame.init()

# window dimensions
WIDTH, HEIGHT = 900, 900

# colours
YELLOW = (255, 255, 0)
DARK_GREY = (80, 78, 81)
WHITE = (255, 255, 255)
BLUE = (10, 130, 255)
RED = (188, 39, 50)
GREEN = (47, 237, 40)
BEIGE = (230, 208, 178)

MONA_PURPLE = (136, 0, 231)

# timestep (duh)
# ORIGINAL_TIMESTEP = 86400/2
# timestep = Timestep(ORIGINAL_TIMESTEP)

# fonts
FONT_16 = pygame.font.SysFont("Inter", 16)
FONT_20 = pygame.font.SysFont("Inter", 20)

circle = pygame.Surface((2, 2), pygame.SRCALPHA)
# pygame.draw.circle(circle, WHITE, (0, 0), 1)
gfxdraw.aacircle(circle, 2, 2, 10, WHITE)
gfxdraw.filled_circle(circle, 2, 2, 10, WHITE)

class RandomSurface(pygame.sprite.Sprite):
    def __init__(self, coordinates, radius, colour, group):
        super().__init__(group)

        # self.image = pygame.Surface()
        self.image = circle
        self.image = pygame.transform.rotozoom(self.image, 0, radius/10)
        self.rect = self.image.get_rect(center = coordinates)


        # self.image.get_rect() = 

        self.radius = radius
        self.coordinates = coordinates
        self.colour = colour

        self.name = 'random_surface'

    # def camera_draw(self, player):
    #     pygame.draw.circle(self.image, self.colour, self.coordinates, self.radius)