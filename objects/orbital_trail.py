import pygame

from utils.utils import get_average_color, rgb_to_hex

class OrbitalTrail(pygame.sprite.Sprite):
    def __init__(self, object, original_scale, group):
        super().__init__(group)
        self.object = object
        self.original_scale = original_scale

        self.image = pygame.Surface((900, 900), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft = (0,0))
    
    def draw_orbital_trail(self):    
        # gets current position from (0,0), i think
        # current_pos = self.coordinates * self.SCALE + np.array([WIDTH / 2, HEIGHT / 2])
        if len(self.object.trail) > 2:
            # draws orbital trail
            updated_points = []

            for pt in self.object.trail:
                x_pt, y_pt = pt[0], pt[1]

                x_pt = x_pt * self.original_scale + 900 / 2
                y_pt = y_pt * self.original_scale + 900 / 2

                updated_points.append((x_pt, y_pt))

            pygame.draw.lines(self.image, self.object.colour, False, updated_points, 2) 
            self.image.blit() 


        # removes the first 5 elements every 500 elements
        # prevents array getting too big
        if len(self.object.trail) == 500:
            self.object.trail = self.object.trail[5:]

    def update(self, *args):
        self.draw_orbital_trail()