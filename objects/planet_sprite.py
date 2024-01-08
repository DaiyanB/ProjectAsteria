import numpy as np
from numpy.linalg import norm

import pygame, math

from .constant import Constant
from utils.utils import get_average_color, rgb_to_hex

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

# fonts
FONT_16 = pygame.font.SysFont("Inter", 16)
FONT_20 = pygame.font.SysFont("Inter", 20)

class PlanetSprite(pygame.sprite.Sprite):
    def __init__(self, coordinates, ref_radius, mass, name, timestep, path, group):
        super().__init__(group)

        # position vector
        current_pos = np.array(coordinates) * self.SCALE + np.array([WIDTH / 2, HEIGHT / 2]) 

        self.image = pygame.image.load(f'{path}').convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, ref_radius*2/1024)
        self.rect = self.image.get_rect(center = (current_pos[0], current_pos[1]))

        self.colour = rgb_to_hex(get_average_color(self.image))

        self.coordinates = np.array(coordinates)
        self.ref_radius = ref_radius
        self.mass = mass 
        
        self.name = name.lower()

        self.trail = []

        self.velocity = np.array([0,self.orbital_velocity(self.coordinates)])    

        self.timestep = timestep  

        self.sun = False
        self.sun_distance = 0

    @property
    def SCALE(self):
        return Constant.SCALE
    
    @property
    def radius(self):
        # converts radius from AU to meters and then applies the appropriate scale
        return self.ref_radius*(Constant.SCALE*Constant.AU/100)
    
    def orbital_velocity(self, coordinates):
        # finds the velocity needed to keep the planet in orbit at that particular radius
        if coordinates[0] == 0:
            return 0
        
        velocity = math.sqrt(Constant.G * Constant.SUN_MASS / abs(coordinates[0]))*coordinates[0]/abs(coordinates[0])

        return velocity
    
    # def drawn(self, win):
    #     current_pos = self.coordinates * self.SCALE + np.array([WIDTH / 2, HEIGHT / 2]) # position vector

    #     if len(self.orbit) > 2:
    #         #
    #         # draws orbital trail
    #         #
    #         updated_points = []

    #         for pt in self.orbit:
    #             x_pt, y_pt = pt[0], pt[1]

    #             x_pt = x_pt * self.SCALE + WIDTH / 2
    #             y_pt = y_pt * self.SCALE + HEIGHT / 2

    #             updated_points.append((x_pt, y_pt))

    #         pygame.draw.lines(win, self.colour, False, updated_points, 2)

    #     pygame.draw.circle(win, self.colour, (current_pos[0], current_pos[1]), self.radius)

    #     if not self.sun:
    #         # renders "distance from" text
    #         distance_text = FONT_16.render(f"{round(self.sun_distance/1000, 2)} km", 1, WHITE)
    #         win.blit(distance_text, (current_pos[0] - distance_text.get_width()/2, current_pos[1] + distance_text.get_height()/2))

        
    
    def attraction(self, other):
        # coordinates of other object
        other_coordinates = other.coordinates

        # calculates straight line distance from the centres of each object
        displacement = other_coordinates - self.coordinates 

        distance = norm(displacement)

        # if other.sun:
        #     self.sun_distance = distance

        # calculates force due to gravity from every other object
        # using F = GMm/r^2
        force = Constant.G * self.mass * other.mass / distance**2

        # finds angle between vertical and horizontal components
        theta = math.atan2(displacement[1], displacement[0]) 
        
        # calculates the vector representing the force
        force_vector = np.array([math.cos(theta), math.sin(theta)]) * force

        # returns vector
        return force_vector
    
    def new_coordinates(self, planets):
        # sets resultant force to 0
        resultant_force = np.array([0,0])

        for planet in planets:
            # adds all up all the forces
            if self.name == planet.name:
                continue
        
            force = self.attraction(planet)

            resultant_force = resultant_force + force

        # updates velocity using v = u + at
        self.velocity = self.velocity + (resultant_force / self.mass * self.timestep.get_timestep())

        # updates coordinates accordingly
        self.coordinates = self.coordinates + (self.velocity * self.timestep.get_timestep())

        current_pos = self.coordinates * self.SCALE + np.array([WIDTH / 2, HEIGHT / 2])

        self.rect.center = current_pos

        # appends coordinates so that orbital path can be created
        # self.orbit.append((self.coordinates))

    def update(self, planets):
        self.new_coordinates(planets)