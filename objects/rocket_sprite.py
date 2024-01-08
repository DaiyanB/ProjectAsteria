import numpy as np
from numpy.linalg import norm

import pygame, math
from math import sin, cos, atan2, degrees, radians

if __name__ == "__main__":
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

class RocketSprite(pygame.sprite.Sprite):
    def __init__(self, coordinates, velocity, thrust, mass, timestep, colours, Constant, group):
        super().__init__(group)

        # position vector
        current_pos = np.array(coordinates) * Constant.SCALE + np.array([WIDTH / 2, HEIGHT / 2])

        direction_vector = np.array([0, -1]) 

        self.coordinates = np.array(coordinates)

        self.velocity = np.array(velocity)
        self.thrust = np.array([0,0])
        self.thrust_record = thrust*direction_vector
        self.deceleration = 100

        self.angular_displacement = 0

        self.mass = mass

        self.colours = colours
        self.colour = colours[0]

        # normal and nuclear version of rocket
        normal = pygame.image.load(r'sprites\sprites\rocket_sprite.png').convert_alpha()
        normal = pygame.transform.rotozoom(normal, 0, 0.01)
        nuclear = pygame.image.load(r'sprites\sprites\rocket_nuclear_sprite.png').convert_alpha()
        nuclear = pygame.transform.rotozoom(nuclear, 0, 0.01)
        self.rocket_type = [normal, nuclear]

        self.booster_counter = 0

        self.image = normal
        self.rect = self.image.get_rect(center = (current_pos[0], current_pos[1]))
        # self.ref_radius = 2*Constant.SCALE/100*Constant.AU
        self.trail = []

        self.sun_distance = 0
        self.sun = False

        self.name = 'rocket'

        self.timestep = timestep

        self.Constant = Constant
        print('HHHHHHHHHHHHHHHHHHHHHHHHHHH',self.Constant)
        # self.planets = planets

    @property
    def SCALE(self):
        return self.Constant.SCALE

    def attraction(self, other):
        # coordinates of other object
        other_coordinates = other.coordinates

        # calculates straight line distance from the centres of each object
        displacement = other_coordinates - self.coordinates 
        # if other.sun: print('displacement', displacement)
        # print("atr", self.coordinates)

        distance = norm(displacement)
        # if other.sun: print('distance', distance)

        # if other.sun:
        #     self.sun_distance = distance
        
        # calculates force due to gravity from every other object
        # using F = GMm/r^2
        force = self.Constant.G * self.mass * other.mass / distance**2
        # if other.sun: print('force', force)

        # if self.name == "earth":
        #     print(force)

        # finds angle between vertical and horizontal components
        theta = math.atan2(displacement[1], displacement[0])

        # calculates the vector representing the force
        force_vector = np.array([math.cos(theta), math.sin(theta)]) * force
        # if other.sun: print('force_vector', force_vector)

        # returns vector
        return force_vector

    def rotate_force(self, theta_deg):
        # adjusts the angular displacement from the direction vector
        self.angular_displacement = (theta_deg + self.angular_displacement) % 360

        # converts degrees to radians
        theta = radians(theta_deg)
        
        # sets up rotation matrix
        rotation_matrix = np.array([[cos(-theta), -sin(-theta)], 
                                    [sin(-theta), cos(-theta)]])
        
        # direction of force rotated via a matrix transformation
        # rotation matrix multiplied by force vector
        self.thrust = np.matmul(rotation_matrix, self.thrust)
        self.thrust_record = np.matmul(rotation_matrix, self.thrust_record)

        # rotates sprite according to the angular displacement
        self.image = pygame.transform.rotate(self.rocket_type[0], self.angular_displacement)

    def change_thrust(self, thrust_constant):
        # decreases the magnitude of the thrust by some factor equal to
        # the thrust_constant
        magnitude = norm(self.thrust)

        # new magnitude of thrust
        delta_thrust = magnitude+thrust_constant

        # thrust validation
        if magnitude != 0:
            if delta_thrust <= 0:
                self.thrust_record = self.thrust
                self.thrust = self.thrust*0
            else:
                normalised_factor = delta_thrust/magnitude
                self.thrust = self.thrust*normalised_factor

        elif magnitude == 0 and thrust_constant > 0:            
            normalised_factor = delta_thrust/norm(self.thrust_record)
            self.thrust = self.thrust_record*normalised_factor            

    def breaking(self):
        # decreases the magnitude of the velocity by some factor equal to
        # the deceleration
        magnitude = norm(self.velocity)

        # change in velocity
        delta_vel = magnitude-self.deceleration
        
        # velocity validation
        if magnitude != 0:
            if delta_vel <= 0:
                self.velocity = self.velocity*0
            else:
                breaking_factor = (delta_vel)/magnitude
                self.velocity = self.velocity*breaking_factor
        else:
            self.velocity = self.velocity*0

    def booster(self, boost_counter):
        # turns booster on and off ie removes or adds back thrust
        if boost_counter:
            print(self.thrust, self.thrust_record)
            self.thrust = self.thrust_record
        else:
            self.thrust_record = self.thrust
            self.thrust = np.array([0, 0])
            print('After',self.thrust, self.thrust_record)

        self.booster_counter = boost_counter

    def rocket_input(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_RIGHT]:
            self.rotate_force(-1)
        
        if keys[pygame.K_LEFT]:
            self.rotate_force(1)

        if self.booster_counter:
            if keys[pygame.K_UP]:
                self.change_thrust(10)

            if keys[pygame.K_DOWN]:
                self.change_thrust(-10)
        
        if keys[pygame.K_SPACE]:
            self.breaking()

        if keys[pygame.K_z]:
            self.velocity = self.velocity*0

        if keys[pygame.K_EQUALS]:
            new_timestep =  self.timestep.get_timestep() + self.timestep.get_original_timestep()*0.05
            self.timestep.update_timestep(new_timestep)
        
        if keys[pygame.K_MINUS]:
            new_timestep = self.timestep.get_timestep() - self.timestep.get_original_timestep()*0.05
            self.timestep.update_timestep(new_timestep)

        # for event in pygame.event.get():
        #     if event.type == pygame.KEYDOWN:
   
        #         if event.key == pygame.K_o:
        #             if self.boost_counter % 2 == 0:
        #                 self.booster()
        #             else:
        #                 self.booster()

        #             self.boost_counter += 1  

                # if event.key == pygame.K_n:
                #     # if self.n_counter % 2 == 0:
                #     #     self.image = self.rocket_type[1]
                #     #     self.colour = GREEN
                #     # else:
                #     #     self.image = self.rocket_type[0]
                #     #     self.colour = WHITE
                #     self.rocket_index += 1
                #     self.image = self.rocket_type[self.rocket_index % 2]

                #     self.n_counter += 1
  
    def new_coordinates(self, planets):
        # sets resultant force to 0
        resultant_force = np.array([0,0])

        for planet in planets:
            # adds all up all the forces
            if self == planet:
                continue
        
            force = self.attraction(planet)

            resultant_force = resultant_force + force

        # adds force due to thrust
        resultant_force = resultant_force + self.thrust

        # print(resultant_force)

        # updates velocity using v = u + at
        self.velocity = self.velocity + (resultant_force / self.mass * self.timestep.get_timestep())
        
        # updates coordinates accordingly
        self.coordinates = self.coordinates + (self.velocity * self.timestep.get_timestep())
        # print(self.coordinates)
        current_pos = self.coordinates * self.SCALE + np.array([WIDTH / 2, HEIGHT / 2])
        # print(current_pos)
        self.rect.center = current_pos
        
        self.trail.append((self.coordinates))   

    def scaler(self, coords):
        x, y = coords[0], coords[1]

        x = x * self.SCALE + WIDTH / 2
        y = y * self.SCALE + WIDTH / 2

        return (x, y)

    def render(self, win):
        # # gets current position from (0,0), i think
        # # current_pos = self.coordinates * self.SCALE + np.array([WIDTH / 2, HEIGHT / 2])
        # if len(self.trail) > 2:
        #     # draws orbital trail
        #     updated_points = []

        #     for pt in self.path:
        #         x_pt, y_pt = pt[0], pt[1]

        #         x_pt = x_pt * self.SCALE + WIDTH / 2
        #         y_pt = y_pt * self.SCALE + HEIGHT / 2

        #         updated_points.append((x_pt, y_pt))

        #     pygame.draw.lines(win, self.colour, False, updated_points, 2)  


        # # removes the first 5 elements every 500 elements
        # # prevents array getting too big
        # if len(self.trail) == 500:
        #     self.trail = self.trail[5:]
        

        # renders distance, velocity, thrust, and angle from original position
        distance_text = FONT_20.render(f"{round(self.sun_distance/1000, 2)} km", 1, WHITE)
        win.blit(distance_text, (20, 20))

        vel_text = FONT_20.render(f"{round(norm(self.velocity)/1000, 2)} km/s", 1, WHITE)
        win.blit(vel_text, (20, distance_text.get_height()+20))

        thurst_text = FONT_20.render(f"{int(round(norm(self.thrust)))} N", 1, WHITE)
        win.blit(thurst_text, (20, distance_text.get_height()*2+20))

        angle = 0 if self.angular_displacement == 0 else (360-self.angular_displacement)
        angle_text = FONT_20.render(f"{int(round(angle))}°", 1, WHITE)
        win.blit(angle_text, (20, distance_text.get_height()*3+20))

        timestep_text = FONT_20.render(f"Timestep: {self.timestep.get_timestep()} s/frame", 1, WHITE)
        win.blit(timestep_text, (WIDTH-20-timestep_text.get_width(), 80))

        state = 'ON' if self.booster_counter else 'OFF'
        booster_text = FONT_20.render(f"Booster: {state}", 1, WHITE)
        win.blit(booster_text, (WIDTH-20-booster_text.get_width(), 60))

    def update(self, planets):
        self.rocket_input()
        self.new_coordinates(planets)