import numpy as np
from numpy.linalg import norm

import pygame, math

pygame.font.init()

WIDTH, HEIGHT = 800, 800

YELLOW = (255, 255, 0)
DARK_GREY = (80, 78, 81)
WHITE = (255, 255, 255)
BLUE = (10, 130, 255)
RED = (188, 39, 50)

FONT = pygame.font.SysFont("Inter", 16)

class Planet:
    AU = 149.6e6 * 1000
    G = 6.67428e-11
    SCALE = 200/AU # 1 AU = 100 px
    TIMESTEP = 3600*24*10 # 1 day
    SUN_MASS = 1.988892e30

    def __init__(self, coordinates, radius, colour, mass):
        self.coordinates = np.array(coordinates)
        self.radius = radius
        self.colour = colour
        self.mass = mass 

        self.name = "nein"

        self.orbit = []

        self.velocity = np.array([0,self.orbital_velocity(self.coordinates)])      

        self.sun = False
        self.sun_distance = 0

    def orbital_velocity(self, coordinates):
        if coordinates[0] == 0:
            return 0
        
        velocity = math.sqrt(self.G * self.SUN_MASS / abs(coordinates[0]))*coordinates[0]/abs(coordinates[0])
        return velocity
    
    def draw(self, win):
        current_pos = self.coordinates * self.SCALE + np.array([WIDTH / 2, HEIGHT / 2])
        # x = self.x * self.SCALE + WIDTH / 2
        # y = self.y * self.SCALE + HEIGHT / 2

        if len(self.orbit) > 2:
            updated_points = []

            for pt in self.orbit:
                x_pt, y_pt = pt[0], pt[1]

                x_pt = x_pt * self.SCALE + WIDTH / 2
                y_pt = y_pt * self.SCALE + HEIGHT / 2

                updated_points.append((x_pt, y_pt))

            pygame.draw.lines(win, self.colour, False, updated_points, 2)

        if not self.sun:
            distance_text = FONT.render(f"{round(self.sun_distance/1000, 2)} km", 1, WHITE)
            win.blit(distance_text, (current_pos[0] - distance_text.get_width()/2, current_pos[1] + distance_text.get_height()/2))

        pygame.draw.circle(win, self.colour, (current_pos[0], current_pos[1]), self.radius)
    
    def attraction(self, other):
        other_coordinates = other.coordinates

        displacement = other_coordinates - self.coordinates 

        distance = norm(displacement)
        # distance = math.sqrt(displacement[0]**2 + displacement[1]**2)


        if other.sun:
            self.sun_distance = distance

        force = self.G * self.mass * other.mass / distance**2

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
        
        # self.x_vel += total_fx / self.mass * self.TIMESTEP
        # self.y_vel += total_fy / self.mass * self.TIMESTEP

        self.velocity = self.velocity + (resultant_force / self.mass * self.TIMESTEP)

        # self.x += self.x_vel * self.TIMESTEP
        # self.y += self.y_vel * self.TIMESTEP

        self.coordinates = self.coordinates + (self.velocity * self.TIMESTEP)
        # if self.name == "earth":
        #     print(self.sun_distance)
        self.orbit.append((self.coordinates))



sun = Planet([0, 0], 30, YELLOW, 1.988892e30)
sun.sun = True

mercury = Planet([0.387*Planet.AU, 0], 8, DARK_GREY, 3.30e23)
# mercury.velocity[1] = -47.4 * 1000

venus = Planet([0.723*Planet.AU, 0], 14, WHITE, 4.8685e24)
# venus.velocity[1] = -35.02 * 1000

earth = Planet([-Planet.AU, 0], 16, BLUE, 5.9742e24)
# earth.velocity[1] = 29.783 * 1000
# earth.name = "earth"

mars = Planet([-1.524*Planet.AU, 0], 12, RED, 6.39e23)
# mars.velocity[1] = 24.077 * 1000

planets = [sun, mercury, venus, earth, mars]

