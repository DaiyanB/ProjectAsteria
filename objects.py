import numpy as np
from numpy.linalg import norm

import pygame, math

from math import sin, cos, atan2, degrees, radians

# from utils.utils import magnitude

pygame.font.init()

WIDTH, HEIGHT = 900, 900

YELLOW = (255, 255, 0)
DARK_GREY = (80, 78, 81)
WHITE = (255, 255, 255)
BLUE = (10, 130, 255)
RED = (188, 39, 50)
GREEN = (47, 237, 40)
BEIGE = (230, 208, 178)

MONA_PURPLE = (136, 0, 231)

TIMESTEP = 86400/10

FONT_16 = pygame.font.SysFont("Inter", 16)
FONT_20 = pygame.font.SysFont("Inter", 20)

class Constant():
    AU = 149.6e6 * 1000
    G = 6.67428e-11
    SCALE = 100/AU # 1 AU = 100 px
    SUN_MASS = 1.988892e30

class scale:
    def __init__(self):
        self.font = pygame.font.SysFont("Inter", 20)
        self.text = self.font.render(f"{int(round(self.SCALE*Constant.AU, 0))} px per AU", True, (255, 255, 255))

    @property
    def SCALE(self):
        return Constant.SCALE

    def render(self, win, width):
        self.text = self.font.render(f"{int(round(self.SCALE*Constant.AU, 0))} px per AU", True, (255, 255, 255))
        win.blit(self.text, (width-20-self.text.get_width(), 40))

class Planet:
    def __init__(self, coordinates, ref_radius, colour, mass):
        self.coordinates = np.array(coordinates)
        self.ref_radius = ref_radius
        self.colour = colour
        self.mass = mass 

        self.name = "nein" # debugging purposes

        self.orbit = []

        self.velocity = np.array([0,self.orbital_velocity(self.coordinates)])      

        self.sun = False
        self.sun_distance = 0

    @property
    def SCALE(self):
        return Constant.SCALE
    @property
    def radius(self):
        return self.ref_radius*(Constant.SCALE*Constant.AU/100)
    
    def orbital_velocity(self, coordinates):
        if coordinates[0] == 0:
            return 0
        
        velocity = math.sqrt(Constant.G * Constant.SUN_MASS / abs(coordinates[0]))*coordinates[0]/abs(coordinates[0])
        return velocity
    
    def draw(self, win):
        current_pos = self.coordinates * self.SCALE + np.array([WIDTH / 2, HEIGHT / 2])

        if len(self.orbit) > 2:
            updated_points = []

            for pt in self.orbit:
                x_pt, y_pt = pt[0], pt[1]

                x_pt = x_pt * self.SCALE + WIDTH / 2
                y_pt = y_pt * self.SCALE + HEIGHT / 2

                updated_points.append((x_pt, y_pt))

            pygame.draw.lines(win, self.colour, False, updated_points, 2)

        if not self.sun:
            distance_text = FONT_16.render(f"{round(self.sun_distance/1000, 2)} km", 1, WHITE)
            win.blit(distance_text, (current_pos[0] - distance_text.get_width()/2, current_pos[1] + distance_text.get_height()/2))

        pygame.draw.circle(win, self.colour, (current_pos[0], current_pos[1]), self.radius)
    
    def attraction(self, other):
        other_coordinates = other.coordinates

        displacement = other_coordinates - self.coordinates 

        distance = norm(displacement)
        # distance = math.sqrt(displacement[0]**2 + displacement[1]**2)


        if other.sun:
            self.sun_distance = distance

        force = Constant.G * self.mass * other.mass / distance**2

        if self.name == "earth":
            print(force)

        theta = math.atan2(displacement[1], displacement[0])

        force_vector = np.array([math.cos(theta), math.sin(theta)]) * force

        return force_vector
    
    def update_position(self, planets):
        resultant_force = np.array([0,0])

        for planet in planets:
            if self == planet:
                continue
        
            force = self.attraction(planet)

            resultant_force = resultant_force + force

        self.velocity = self.velocity + (resultant_force / self.mass * TIMESTEP)

        self.coordinates = self.coordinates + (self.velocity * TIMESTEP)
        # if self.name == "earth":
        #     print(self.sun_distance)
        self.orbit.append((self.coordinates))

class Rocket:
    def __init__(self, coordinates, velocity, thrust, mass, colour): 
        self.coordinates = np.array(coordinates)
        self.velocity = np.array(velocity)
        self.thrust = np.array(thrust)
        # print("in", self.thrust)
        # print("in mag", magnitude(self.thrust))
        self.mass = mass
        self.colour = colour

        self.ref_radius = 2*Constant.SCALE/100*Constant.AU
        self.path = []

        self.sun_distance = 0
        self.sun = False

    @property
    def SCALE(self):
        return Constant.SCALE
    
    @property
    def radius(self):
        return self.ref_radius*(Constant.SCALE*Constant.AU/100)

    def draw(self, win):
        current_pos = self.coordinates * self.SCALE + np.array([WIDTH / 2, HEIGHT / 2])
        if len(self.path) > 2:
            updated_points = []

            for pt in self.path:
                x_pt, y_pt = pt[0], pt[1]

                x_pt = x_pt * self.SCALE + WIDTH / 2
                y_pt = y_pt * self.SCALE + HEIGHT / 2

                updated_points.append((x_pt, y_pt))
                
            pygame.draw.lines(win, self.colour, False, updated_points, 2)  

        if len(self.path) == 500:
            self.path = self.path[5:]

        distance_text = FONT_20.render(f"{round(self.sun_distance/1000, 2)} km", 1, WHITE)
        win.blit(distance_text, (20, 20))
        vel_text = FONT_20.render(f"{round(norm(self.velocity)/1000, 2)} km/s", 1, WHITE)
        win.blit(vel_text, (20, distance_text.get_height()+20))
        thurst_text = FONT_20.render(f"{int(round(norm(self.thrust)))} N", 1, WHITE)
        win.blit(thurst_text, (20, distance_text.get_height()*2+20))
        angle_text = FONT_20.render(f"{int(round(degrees(atan2(self.thrust[0], self.thrust[1]))))}°", 1, WHITE)
        win.blit(angle_text, (20, distance_text.get_height()*3+20))

        pygame.draw.circle(win, self.colour, (current_pos[0], current_pos[1]), self.radius)

    def attraction(self, other):
        other_coordinates = other.coordinates

        displacement = other_coordinates - self.coordinates 
        # print("atr", self.coordinates)

        distance = norm(displacement)

        if other.sun:
            self.sun_distance = distance

        force = Constant.G * self.mass * other.mass / distance**2

        # if self.name == "earth":
        #     print(force)

        theta = math.atan2(displacement[1], displacement[0])

        force_vector = np.array([math.cos(theta), math.sin(theta)]) * force

        return force_vector
    
    def rotate_force(self, theta):
        theta = radians(theta)
        rotation_matrix = np.array([[cos(theta), -sin(theta)], 
                                    [sin(theta), cos(theta)]])
    
        self.thrust = np.matmul(rotation_matrix, self.thrust)

    def boost_break(self, factor):
        magnitude = norm(self.thrust)
        f_factor = (magnitude+factor)/magnitude
        self.thrust = self.thrust*f_factor

    def booster(self, state):
        if state == True:
            self.thrust = np.array([0, 1000])
        elif state == False:
            self.thrust = np.array([0, 0])

    def update_position(self, planets):
        resultant_force = np.array([0,0])

        for planet in planets:
            if self == planet:
                continue
        
            force = self.attraction(planet)

            resultant_force = resultant_force + force

        resultant_force = resultant_force + self.thrust

        self.velocity = self.velocity + (resultant_force / self.mass * TIMESTEP)
        self.coordinates = self.coordinates + (self.velocity * TIMESTEP)
        # if self.name == "earth":
        #     print(self.sun_distance)
        self.path.append((self.coordinates))

sun = Planet([0, 0], 24, YELLOW, 1.988892e30)
sun.sun = True

mercury = Planet([0.387*Constant.AU, 0], 8, DARK_GREY, 3.30e23)

venus = Planet([0.723*Constant.AU, 0], 14, BEIGE, 4.8685e24)

earth = Planet([-Constant.AU, 0], 16, BLUE, 5.9742e24)

mars = Planet([-1.524*Constant.AU, 0], 12, RED, 6.39e23)

# pl = Planet([3*Constant.AU, 0], 23, MONA_PURPLE, 2.71828e29)
rocket = Rocket([-Constant.AU+2, earth.radius*Constant.SCALE*2], [0,11208.25589], [0, 20], 1e3, WHITE)
# rocket2 = Rocket([Constant.AU*2, earth.radius*Constant.SCALE*2], [0,11208.25589], 1e29, WHITE)

planets = [sun, mercury, venus, earth, mars, rocket]
# planets = [sun, mercury, venus, rocket]

# planets = [sun, rocket, rocket2]

