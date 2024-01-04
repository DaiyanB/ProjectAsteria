import numpy as np
from numpy.linalg import norm

import pygame, math
from math import sin, cos, atan2, degrees, radians

from .constant import Constant

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

class Planet:
    def __init__(self, coordinates, ref_radius, mass, name, timestep):
        # initialises planet properties
        self.coordinates = np.array(coordinates)
        self.ref_radius = ref_radius
        self.mass = mass 

        self.name = name.lower() # debugging purposes

        self.orbit = []

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
    
    def draw(self, win):
        current_pos = self.coordinates * self.SCALE + np.array([WIDTH / 2, HEIGHT / 2]) # position vector

        if len(self.orbit) > 2:
            # draws orbital trail
            updated_points = []

            for pt in self.orbit:
                x_pt, y_pt = pt[0], pt[1]

                x_pt = x_pt * self.SCALE + WIDTH / 2
                y_pt = y_pt * self.SCALE + HEIGHT / 2

                updated_points.append((x_pt, y_pt))

            pygame.draw.lines(win, self.colour, False, updated_points, 2)

        # pygame.draw.circle(win, self.colour, (current_pos[0], current_pos[1]), self.radius)

        if not self.sun:
            # renders "distance from" text
            distance_text = FONT_16.render(f"{round(self.sun_distance/1000, 2)} km", 1, WHITE)
            win.blit(distance_text, (current_pos[0] - distance_text.get_width()/2, current_pos[1] + distance_text.get_height()/2))

        
    
    def attraction(self, other):
        # coordinates of other object
        other_coordinates = other.coordinates

        # calculates straight line distance from the centres of each object
        displacement = other_coordinates - self.coordinates 

        distance = norm(displacement)
        # distance = math.sqrt(displacement[0]**2 + displacement[1]**2)


        if other.sun:
            self.sun_distance = distance

        # calculates force due to gravity from every other object
        # using F = GMm/r^2
        force = Constant.G * self.mass * other.mass / distance**2

        # finds angle between vertical and horizontal components
        theta = math.atan2(displacement[1], displacement[0]) 
        
        # calculates the vector representing the force
        force_vector = np.array([math.cos(theta), math.sin(theta)]) * force

        # returns vector
        return force_vector
    
    def update_position(self, planets):
        # sets resultant force to 0
        resultant_force = np.array([0,0])

        for planet in planets:
            # adds all up all the forces
            if self == planet:
                continue
        
            force = self.attraction(planet)

            resultant_force = resultant_force + force

        # updates velocity using v = u + at
        self.velocity = self.velocity + (resultant_force / self.mass * self.timestep.get_timestep())

        # updates coordinates accordingly
        self.coordinates = self.coordinates + (self.velocity * self.timestep.get_timestep())

        # appends coordinates so that orbital path can be created
        self.orbit.append((self.coordinates))

class Rocket():
    def __init__(self, coordinates, velocity, thrust, mass, colour):
        # super().__init__(group)
        # intiisalises rocket properties
        self.coordinates = np.array(coordinates)
        self.velocity = np.array(velocity)
        self.thrust = np.array(thrust)
        self.mass = mass
        self.colour = colour

        #adjusts radius into km (??)
        self.ref_radius = 2*Constant.SCALE/100*Constant.AU
        # for orbital trail
        self.path = []

        self.sun_distance = 0
        self.sun = False

    @property
    def SCALE(self):
        return Constant.SCALE
    
    @property
    def radius(self):
        # converts radius from AU to meters and then applies the appropriate scale
        return self.ref_radius*(Constant.SCALE*Constant.AU/100)

    def draw(self, win):
        # gets current position from (0,0), i think
        current_pos = self.coordinates * self.SCALE + np.array([WIDTH / 2, HEIGHT / 2])
        if len(self.path) > 2:
            # draws orbital trail
            updated_points = []

            for pt in self.path:
                x_pt, y_pt = pt[0], pt[1]

                x_pt = x_pt * self.SCALE + WIDTH / 2
                y_pt = y_pt * self.SCALE + HEIGHT / 2

                updated_points.append((x_pt, y_pt))

            pygame.draw.lines(win, self.colour, False, updated_points, 2)  


        # removes the first 5 elements every 500 elements
        # prevents array getting too big
        if len(self.path) == 500:
            self.path = self.path[5:]
        

        # renders distance, velocity, thrust, and angle from original position
        distance_text = FONT_20.render(f"{round(self.sun_distance/1000, 2)} km", 1, WHITE)
        win.blit(distance_text, (20, 20))

        vel_text = FONT_20.render(f"{round(norm(self.velocity)/1000, 2)} km/s", 1, WHITE)
        win.blit(vel_text, (20, distance_text.get_height()+20))

        thurst_text = FONT_20.render(f"{int(round(norm(self.thrust)))} N", 1, WHITE)
        win.blit(thurst_text, (20, distance_text.get_height()*2+20))

        angle_text = FONT_20.render(f"{int(round(degrees(atan2(self.thrust[0], self.thrust[1]))))}°", 1, WHITE)
        win.blit(angle_text, (20, distance_text.get_height()*3+20))

        # draws rocket as a circle
        pygame.draw.circle(win, self.colour, (current_pos[0], current_pos[1]), self.radius)

    def attraction(self, other):
        # coordinates of other object
        other_coordinates = other.coordinates

        # calculates straight line distance from the centres of each object
        displacement = other_coordinates - self.coordinates 
        # print("atr", self.coordinates)

        distance = norm(displacement)

        if other.sun:
            self.sun_distance = distance
        
        # calculates force due to gravity from every other object
        # using F = GMm/r^2
        force = Constant.G * self.mass * other.mass / distance**2

        # finds angle between vertical and horizontal components
        theta = math.atan2(displacement[1], displacement[0])

        # calculates the vector representing the force
        force_vector = np.array([math.cos(theta), math.sin(theta)]) * force

        # returns vector
        return force_vector
    
    def rotate_force(self, theta):
        # converts degrees to radians
        theta = radians(theta)
        
        # sets up rotation matrix
        rotation_matrix = np.array([[cos(theta), -sin(theta)], 
                                    [sin(theta), cos(theta)]])
        
        # direction of force rotated via a matrix transformation
        # rotation matrix multiplied by force vector
        self.thrust = np.matmul(rotation_matrix, self.thrust)

    def boost_break(self, factor):
        # changes the magnitude of the force by some factor
        magnitude = norm(self.thrust)
        f_factor = (magnitude+factor)/magnitude
        self.thrust = self.thrust*f_factor

    def booster(self, state):
        # turns booster on and off i.e. removes or adds back thrust
        if state == True:
        # adds 1000 N of thrust, y-axis only    
            self.thrust = np.array([0, 1000]) 
        elif state == False:
            self.thrust = np.array([0, 0])

    def update_position(self, planets):
        # sets resultant force to 0
        resultant_force = np.array([0,0])

        # adds all up all the forces
        for planet in planets:
            if self == planet:
                continue
        
            force = self.attraction(planet)

            resultant_force = resultant_force + force

        # adds force due to thrust
        resultant_force = resultant_force + self.thrust

        # updates velocity using v = u + at
        self.velocity = self.velocity + (resultant_force / self.mass * self.timestep.get_timestep())
        
        # updates coordinates accordingly
        self.coordinates = self.coordinates + (self.velocity * self.timestep.get_timestep())
        # if self.name == "earth":
        #     print(self.sun_distance)
        self.path.append((self.coordinates))
