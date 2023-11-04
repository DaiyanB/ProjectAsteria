import numpy as np
from numpy.linalg import norm

import pygame, math
from pygame import gfxdraw
from math import sin, cos, atan2, degrees, radians
from random import randint


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
TIMESTEP = 86400/1

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
    #
    # constant class
    #
    AU = 149.6e6 * 1000
    G = 6.67428e-11
    SCALE = 100/AU # 1 AU = 100 px
    SUN_MASS = 1.988892e30

class Scale:
    #
    # class to set and display the scale
    #
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

        if self.name == "earth": # debugging purposes
            print(force)

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
        self.velocity = self.velocity + (resultant_force / self.mass * TIMESTEP)

        #
        # updates coordinates accordingly
        #
        self.coordinates = self.coordinates + (self.velocity * TIMESTEP)

        #
        # appends coordinates so that orbital path can be created
        #
        self.orbit.append((self.coordinates))

class PlanetSprite(pygame.sprite.Sprite):
    def __init__(self, coordinates, ref_radius, mass, name, path, group):
        super().__init__(group)
        current_pos = np.array(coordinates) * self.SCALE + np.array([WIDTH / 2, HEIGHT / 2]) # position vector

        self.image = pygame.image.load(f'{path}').convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, ref_radius*2/1024)
        self.rect = self.image.get_rect(center = (current_pos[0], current_pos[1]))

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
    
    def drawn(self, win):
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
            # renders "distance from" text
            distance_text = FONT_16.render(f"{round(self.sun_distance/1000, 2)} km", 1, WHITE)
            win.blit(distance_text, (current_pos[0] - distance_text.get_width()/2, current_pos[1] + distance_text.get_height()/2))

        
    
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
        self.velocity = self.velocity + (resultant_force / self.mass * TIMESTEP)

        # updates coordinates accordingly
        self.coordinates = self.coordinates + (self.velocity * TIMESTEP)
        print(self.coordinates)
        current_pos = self.coordinates * self.SCALE + np.array([WIDTH / 2, HEIGHT / 2])
        print(current_pos)
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
        self.velocity = self.velocity + (resultant_force / self.mass * TIMESTEP)
        
        # updates coordinates accordingly
        self.coordinates = self.coordinates + (self.velocity * TIMESTEP)
        # if self.name == "earth":
        #     print(self.sun_distance)
        self.path.append((self.coordinates))

class RocketSprite(pygame.sprite.Sprite):
    def __init__(self, coordinates, velocity, thrust, mass, colour, group):
        super().__init__(group)
        current_pos = np.array(coordinates) * self.SCALE + np.array([WIDTH / 2, HEIGHT / 2]) # position vector

        self.coordinates = np.array(coordinates)
        self.velocity = np.array(velocity)
        self.thrust = np.array(thrust)
        self.mass = mass
        self.colour = colour

        normal = pygame.image.load(r'sprites\sprites\rocket_sprite.png').convert_alpha()
        # normal = pygame.Surface((10,10))
        # normal.fill('red')
        normal = pygame.transform.rotozoom(normal, 0, 0.01)
        nuclear = pygame.image.load(r'sprites\sprites\rocket_nuclear_sprite.png')
        nuclear = pygame.transform.rotozoom(nuclear, 0, 0.01)
        self.rocket_type = [normal, nuclear]
        self.rocket_index = 0

        self.image = normal
        self.rect = self.image.get_rect(center = (current_pos[0], current_pos[1]))
        self.ref_radius = 2*Constant.SCALE/100*Constant.AU
        self.path = []

        self.sun_distance = 0
        self.sun = False

        self.boost_counter = 0
        self.n_counter = 0

        # self.planets = planets

    @property
    def SCALE(self):
        return Constant.SCALE
    
    @property
    def radius(self):
        return self.ref_radius*(Constant.SCALE*Constant.AU/100)

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

        # if self.name == "earth":
        #     print(force)

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
        # turns booster on and off ie removes or adds back thrust
        if state == True:
            self.thrust = np.array([0, -1000])
        elif state == False:
            self.thrust = np.array([0, 0])

    def rocket_input(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_RIGHT]:
            self.rotate_force(0.2)
        
        if keys[pygame.K_LEFT]:
            self.rotate_force(-0.2)

        if keys[pygame.K_UP]:
            self.boost_break(1.5)

        if keys[pygame.K_DOWN]:
            self.boost_break(-1.5)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
   
                if event.key == pygame.K_o:
                    if self.boost_counter % 2 == 0:
                        self.booster(False)
                    else:
                        self.booster(True)

                    self.boost_counter += 1  

                if event.key == pygame.K_n:
                    # if self.n_counter % 2 == 0:
                    #     self.image = self.rocket_type[1]
                    #     self.colour = GREEN
                    # else:
                    #     self.image = self.rocket_type[0]
                    #     self.colour = WHITE
                    self.rocket_index += 1
                    self.image = self.rocket_type[self.rocket_index % 2]

                    self.n_counter += 1
  

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

        # updates velocity using v = u + at
        self.velocity = self.velocity + (resultant_force / self.mass * TIMESTEP)
        
        # updates coordinates accordingly
        self.coordinates = self.coordinates + (self.velocity * TIMESTEP)
        print(self.coordinates)
        current_pos = self.coordinates * self.SCALE + np.array([WIDTH / 2, HEIGHT / 2])
        print(current_pos)
        self.rect.center = current_pos
        # self.path.append((self.coordinates))   

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

    # def camera_draw(self, player):
    #     pygame.draw.circle(self.image, self.colour, self.coordinates, self.radius)

class Camera(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
    
        # camera offset
        self.offset = pygame.math.Vector2()
        #self.half_W = self.display_surface.get_size()[0] // 2
        #self.half_h = self.display_surface.get_size()[1] // 2

        #box setup
        self.camera_borders = {"left": 100, "top": 100, "width": 700, "height": 700}
        l, t, w, h = (self.camera_borders[i] for i in self.camera_borders)
        self.camera_rect = pygame.Rect(l, t, w, h)

    def box_target(self, target):
        if target.rect.left < self.camera_rect.left:
            self.camera_rect.left = target.rect.left
        if target.rect.right > self.camera_rect.right:
            self.camera_rect.right = target.rect.right
        if target.rect.top < self.camera_rect.top:
            self.camera_rect.top = target.rect.top
        if target.rect.bottom > self.camera_rect.bottom:
            self.camera_rect.bottom = target.rect.bottom

        self.offset.x = self.camera_rect.left - self.camera_borders["left"]
        self.offset.y = self.camera_rect.top - self.camera_borders["top"]

    def camera_draw(self, player):
        self.box_target(player)

        for sprite in self.sprites():
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

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

# pl = Planet([3*Constant.AU, 0], 23, MONA_PURPLE, 2.71828e29)
# rocket2 = Rocket([Constant.AU*2, earth.radius*Constant.SCALE*2], [0,11208.25589], 1e29, WHITE)

# rocket = pygame.sprite.GroupSingle()
# rocket.add(Rocket())

rocket = Rocket([-2*Constant.AU+2, earth.radius*Constant.SCALE*2], [0,11208.25589], [0, 0], 1e3, WHITE)
planets = [sun, mercury, venus, earth, mars]
#obj = Camera()
# planets = [sun, mercury, venus, rocket]

# planets = [sun, rocket, rocket2]

