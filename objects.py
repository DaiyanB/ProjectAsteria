import numpy as np
from numpy.linalg import norm

import pygame, math
from pygame import gfxdraw
from math import sin, cos, atan2, degrees, radians, pi
from random import randint

from utils.utils import Timestep, get_average_color

# from pygame.sprite import _Group

pygame.font.init()
pygame.init()
#
# window dimensions
#
WIDTH, HEIGHT = 900, 900

#
# colours
#
YELLOW = (255, 255, 0)
DARK_GREY = (80, 78, 81)
WHITE = (255, 255, 255)
BLUE = (10, 130, 255)
RED = (188, 39, 50)
GREEN = (47, 237, 40)
BEIGE = (230, 208, 178)

MONA_PURPLE = (136, 0, 231)

#
# timestep (duh)
#
ORIGINAL_TIMESTEP = 86400/2
timestep = Timestep(ORIGINAL_TIMESTEP)
#
# fonts
#
FONT_16 = pygame.font.SysFont("Inter", 16)
FONT_20 = pygame.font.SysFont("Inter", 20)

def convert_coordinates(coordinates, inverse=False):
    if inverse:
        return coordinates/Constant.AU * Constant.SCALE
    else:
        return coordinates*Constant.SCALE / Constant.AU

class Constant:
    # constant class
    AU = 149.6e6 * 1000
    G = 6.67428e-11
    SCALE = 100/AU # 1 AU = 100 px
    SUN_MASS = 1.988892e30

class Scale:
    # class to set and display the scale
    def __init__(self):
        self.font = pygame.font.SysFont("Inter", 20)
        self.text = self.font.render(f"{int(round(self.SCALE*Constant.AU, 0))} px per AU", True, (255, 255, 255))

    @property
    def SCALE(self):
        return Constant.SCALE

    def render(self, win, width, zoom_scale):
        pos = (width-20-self.text.get_width(), 40)
        self.text = self.font.render(f"{int(round(self.SCALE*Constant.AU*zoom_scale, 0))} px per AU", True, (255, 255, 255))
        # win.blit(self.text, (width-20-self.text.get_width(), 40))
        win.blit(self.text, pos)

class Planet:
    def __init__(self, coordinates, ref_radius, colour, mass, name):
        # initialises planet properties
        self.coordinates = np.array(coordinates)
        self.ref_radius = ref_radius
        self.colour = colour
        self.mass = mass 

        self.name = name.lower() # debugging purposes

        self.orbit = []

        self.velocity = np.array([0,self.orbital_velocity(self.coordinates)])      

        self.sun = False
        self.sun_distance = 0

    @property
    def SCALE(self):
        return Constant.SCALE
    
    @property
    def radius(self):
        #
        # converts radius from AU to meters and then applies the appropriate scale
        #
        return self.ref_radius*(Constant.SCALE*Constant.AU/100)
    
    def orbital_velocity(self, coordinates):
        #
        # finds the velocity needed to keep the planet in orbit at that particular radius
        #
        if coordinates[0] == 0:
            return 0
        
        velocity = math.sqrt(Constant.G * Constant.SUN_MASS / abs(coordinates[0]))*coordinates[0]/abs(coordinates[0])

        return velocity
    
    def draw(self, win):
        current_pos = self.coordinates * self.SCALE + np.array([WIDTH / 2, HEIGHT / 2]) # position vector

        if len(self.orbit) > 2:
            #
            # draws orbital trail
            #
            updated_points = []

            for pt in self.orbit:
                x_pt, y_pt = pt[0], pt[1]

                x_pt = x_pt * self.SCALE + WIDTH / 2
                y_pt = y_pt * self.SCALE + HEIGHT / 2

                updated_points.append((x_pt, y_pt))

            pygame.draw.lines(win, self.colour, False, updated_points, 2)

        pygame.draw.circle(win, self.colour, (current_pos[0], current_pos[1]), self.radius)

        if not self.sun:
            #
            # renders "distance from" text
            #
            distance_text = FONT_16.render(f"{round(self.sun_distance/1000, 2)} km", 1, WHITE)
            win.blit(distance_text, (current_pos[0] - distance_text.get_width()/2, current_pos[1] + distance_text.get_height()/2))

        
    
    def attraction(self, other):
        #
        # coordinates of other object
        #
        other_coordinates = other.coordinates

        #
        # calculates straight line distance from the centres of each object
        #
        displacement = other_coordinates - self.coordinates 

        distance = norm(displacement)
        # distance = math.sqrt(displacement[0]**2 + displacement[1]**2)


        if other.sun:
            self.sun_distance = distance

        #
        # calculates force due to gravity from every other object
        # using F = GMm/r^2
        #
        force = Constant.G * self.mass * other.mass / distance**2

        #
        # finds angle between vertical and horizontal components
        #
        theta = math.atan2(displacement[1], displacement[0]) 
        
        #
        # calculates the vector representing the force
        #
        force_vector = np.array([math.cos(theta), math.sin(theta)]) * force

        #
        # returns vector
        #
        return force_vector
    
    def update_position(self, planets):
        #
        # sets resultant force to 0
        #
        resultant_force = np.array([0,0])

        for planet in planets:
            #
            # adds all up all the forces
            #
            if self == planet:
                continue
        
            force = self.attraction(planet)

            resultant_force = resultant_force + force

        #
        # updates velocity using v = u + at
        #
        self.velocity = self.velocity + (resultant_force / self.mass * timestep.get_timestep())

        #
        # updates coordinates accordingly
        #
        self.coordinates = self.coordinates + (self.velocity * timestep.get_timestep())

        #
        # appends coordinates so that orbital path can be created
        #
        self.orbit.append((self.coordinates))

class PlanetSprite(pygame.sprite.Sprite):
    def __init__(self, coordinates, ref_radius, mass, name, path, group):
        super().__init__(group)

        # position vector
        current_pos = np.array(coordinates) * self.SCALE + np.array([WIDTH / 2, HEIGHT / 2]) 

        self.image = pygame.image.load(f'{path}').convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, ref_radius*2/1024)
        self.rect = self.image.get_rect(center = (current_pos[0], current_pos[1]))

        self.average_colour = get_average_color(self.image)

        self.coordinates = np.array(coordinates)
        self.ref_radius = ref_radius
        self.mass = mass 
        
        self.name = name.lower()

        self.orbit = []

        self.velocity = np.array([0,self.orbital_velocity(self.coordinates)])      

        self.sun = False
        self.sun_distance = 0

    @property
    def SCALE(self):
        return Constant.SCALE
    
    @property
    def radius(self):
        #
        # converts radius from AU to meters and then applies the appropriate scale
        #
        return self.ref_radius*(Constant.SCALE*Constant.AU/100)
    
    def orbital_velocity(self, coordinates):
        #
        # finds the velocity needed to keep the planet in orbit at that particular radius
        #
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
        self.velocity = self.velocity + (resultant_force / self.mass * timestep.get_timestep())

        # updates coordinates accordingly
        self.coordinates = self.coordinates + (self.velocity * timestep.get_timestep())

        current_pos = self.coordinates * self.SCALE + np.array([WIDTH / 2, HEIGHT / 2])

        self.rect.center = current_pos

        # appends coordinates so that orbital path can be created
        # self.orbit.append((self.coordinates))

    def update(self, planets):
        self.new_coordinates(planets)

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
        self.velocity = self.velocity + (resultant_force / self.mass * timestep.get_timestep())
        
        # updates coordinates accordingly
        self.coordinates = self.coordinates + (self.velocity * timestep.get_timestep())
        # if self.name == "earth":
        #     print(self.sun_distance)
        self.path.append((self.coordinates))

class RocketSprite(pygame.sprite.Sprite):
    def __init__(self, coordinates, velocity, thrust, mass, colour, group):
        super().__init__(group)

        # position vector
        current_pos = np.array(coordinates) * self.SCALE + np.array([WIDTH / 2, HEIGHT / 2])

        direction_vector = np.array([0, -1]) 

        self.coordinates = np.array(coordinates)

        self.velocity = np.array(velocity)
        self.thrust = np.array([0,0])
        self.thrust_record = thrust*direction_vector
        self.deceleration = 100

        self.angular_displacement = 0

        self.mass = mass

        self.colour = colour

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
        self.path = []

        self.sun_distance = 0
        self.sun = False

        self.name = 'rocket'

        # self.planets = planets

    @property
    def SCALE(self):
        return Constant.SCALE

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
        force = Constant.G * self.mass * other.mass / distance**2
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
            new_timestep =  timestep.get_timestep() + ORIGINAL_TIMESTEP*0.05
            timestep.update_timestep(new_timestep)
        
        if keys[pygame.K_MINUS]:
            new_timestep = timestep.get_timestep() - ORIGINAL_TIMESTEP*0.05
            timestep.update_timestep(new_timestep)

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
        self.velocity = self.velocity + (resultant_force / self.mass * timestep.get_timestep())
        
        # updates coordinates accordingly
        self.coordinates = self.coordinates + (self.velocity * timestep.get_timestep())
        # print(self.coordinates)
        current_pos = self.coordinates * self.SCALE + np.array([WIDTH / 2, HEIGHT / 2])
        # print(current_pos)
        self.rect.center = current_pos
        
        self.path.append((self.coordinates))   

    def render(self, win):
        # gets current position from (0,0), i think
        # current_pos = self.coordinates * self.SCALE + np.array([WIDTH / 2, HEIGHT / 2])
        # if len(self.path) > 2:
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
        # if len(self.path) == 500:
        #     self.path = self.path[5:]
        

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

        timestep_text = FONT_20.render(f"Timestep: {timestep.get_timestep()} s/frame", 1, WHITE)
        win.blit(timestep_text, (WIDTH-20-timestep_text.get_width(), 80))

        state = 'ON' if self.booster_counter else 'OFF'
        booster_text = FONT_20.render(f"Booster: {state}", 1, WHITE)
        win.blit(booster_text, (WIDTH-20-booster_text.get_width(), 60))

    def update(self, planets):
        self.rocket_input()
        self.new_coordinates(planets)



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

class Camera(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

        self.display_surface = pygame.display.get_surface()
    
        # camera offset
        self.offset = pygame.math.Vector2()
        self.half_w = self.display_surface.get_size()[0] // 2
        self.half_h = self.display_surface.get_size()[1] // 2

        #box setup
        self.camera_borders = {"left": 100, "top": 100, "width": 700, "height": 700}
        l, t, w, h = (self.camera_borders[i] for i in self.camera_borders)
        self.camera_rect = pygame.Rect(l, t, w, h)

        # zoom
        self.zoom_scale = 1
        self.internal_surface_size = (1500, 1500)
        self.internal_surface = pygame.Surface(self.internal_surface_size, pygame.SRCALPHA)
        self.internal_rect = self.internal_surface.get_rect(center = (self.half_w, self.half_h))
        self.internal_surface_size_vector = pygame.math.Vector2(self.internal_surface_size)
        self.internal_offset = pygame.math.Vector2((0,0))
        self.internal_offset.x = self.internal_surface_size[0] // 2 - self.half_w
        self.internal_offset.y = self.internal_surface_size[1] // 2 - self.half_h

    def box_target(self, target):
        # moves rectangle depending on the position of the the camera
        # which is dependent on the position of the rocket
        if target.rect.left < self.camera_rect.left:
            self.camera_rect.left = target.rect.left
        if target.rect.right > self.camera_rect.right:
            self.camera_rect.right = target.rect.right
        if target.rect.top < self.camera_rect.top:
            self.camera_rect.top = target.rect.top
        if target.rect.bottom > self.camera_rect.bottom:
            self.camera_rect.bottom = target.rect.bottom

        # adds the
        self.offset.x = self.camera_rect.left - self.camera_borders["left"]
        self.offset.y = self.camera_rect.top - self.camera_borders["top"]

    def zoom_input(self):
        keys = pygame.key.get_pressed()
    
        if keys[pygame.K_EQUALS]:
            self.zoom_scale += 0.1
        if keys[pygame.K_MINUS]:
            self.zoom_scale -= 0.1

    def camera_draw(self, player, fps, scale):
        self.box_target(player)

        self.internal_surface.fill('black')

        # adds offset to sprites
        for sprite in self.sprites():
            offset_pos = sprite.rect.topleft - self.offset + self.internal_offset
            self.internal_surface.blit(sprite.image, offset_pos)

        # scales sprites depending on the zoom
        scaled_surface = pygame.transform.smoothscale(self.internal_surface, self.internal_surface_size_vector * self.zoom_scale)
        scaled_rect = scaled_surface.get_rect(center = (self.half_w, self.half_h))
        self.display_surface.blit(scaled_surface, scaled_rect)

        # renders the fps and scale texts
        fps.render(self.display_surface, WIDTH)
        scale.render(self.display_surface, WIDTH, self.zoom_scale)

        # renders the rocket info text
        player.render(self.display_surface)

        # pygame.draw.rect(self.display_surface, "yellow", self.camera_rect, 5)
        # self.display_surface.blit()

# camera_group = pygame.sprite.Group()
# camera_group.add(Camera)

sun = Planet([0, 0], 24, YELLOW, 1.988892e30, 'sun')
sun.sun = True

mercury = Planet([0.387*Constant.AU, 0], 8, DARK_GREY, 3.30e23, 'mercury')

venus = Planet([0.723*Constant.AU, 0], 14, BEIGE, 4.8685e24, 'venus')

earth = Planet([-Constant.AU, 0], 16, BLUE, 5.9742e24, 'earth')

mars = Planet([-1.524*Constant.AU, 0], 12, RED, 6.39e23, 'mars')

rocket = Rocket([-2*Constant.AU+2, earth.radius*Constant.SCALE*2], [0,11208.25589], [0, 0], 1e3, WHITE)
planets = [sun, mercury, venus, earth, mars]

