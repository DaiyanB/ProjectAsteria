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
    TIMESTEP = 3600*24*1000 # 1 day

    def __init__(self, x, y, radius, colour, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.colour = colour
        self.mass = mass 

        self.name = "nein"

        self.orbit = []

        self.x_vel = 0
        self.y_vel = 0        

        self.sun = False
        self.sun_distance = 0

    def draw(self, win):
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2

        if len(self.orbit) > 2:
            updated_points = []

            for pt in self.orbit:
                x_pt, y_pt = pt

                x_pt = x_pt * self.SCALE + WIDTH / 2
                y_pt = y_pt * self.SCALE + HEIGHT / 2

                updated_points.append((x_pt, y_pt))

            pygame.draw.lines(win, self.colour, False, updated_points, 2)

        if not self.sun:
            distance_text = FONT.render(f"{round(self.sun_distance/1000, 2)} km", 1, WHITE)
            win.blit(distance_text, (x - distance_text.get_width()/2, y + distance_text.get_height()/2))

        pygame.draw.circle(win, self.colour, (x, y), self.radius)
    
    def attraction(self, other):
        other_x, other_y = other.x, other.y

        distance_x = other_x - self.x
        distance_y = other_y - self.y

        distance = math.sqrt(distance_x**2 + distance_y**2)

        if other.sun:
            self.sun_distance = distance

        force = self.G * self.mass * other.mass / distance**2

        if self.name == "earth":
            print(force)

        theta = math.atan2(distance_y, distance_x)

        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force

        return force_x, force_y
    
    def update_position(self, planets):
        total_fx = total_fy = 0

        for planet in planets:
            if self == planet:
                continue
        
            fx, fy = self.attraction(planet)

            total_fx += fx
            total_fy += fy
        
        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP

        # if self.name == "earth":
        #     print([self.x, self.y])        

        self.orbit.append((self.x, self.y))



sun = Planet(0, 0, 30, YELLOW, 1.988892e30)
sun.sun = True

mercury = Planet(0.387*Planet.AU, 0, 8, DARK_GREY, 3.30e23)
mercury.y_vel = -47.4 * 1000

venus = Planet(0.723*Planet.AU, 0, 14, WHITE, 4.8685e24)
venus.y_vel = -35.02 * 1000

earth = Planet(-Planet.AU, 0, 16, BLUE, 5.9742e24)
earth.y_vel = 29.783 * 1000
earth.name = "earth"

mars = Planet(-1.524*Planet.AU, 0, 12, RED, 6.39e23)
mars.y_vel = 24.077 * 1000

planets = [sun, mercury, venus, earth, mars]

