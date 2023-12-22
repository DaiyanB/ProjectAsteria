import pygame
    
class Button:
    def __init__(self, text, font, width, height, pos, elevation, images = None, scale = 1):
        # core attr
        self.pressed = False
        self.elevation = elevation
        self.elevation_record = elevation
        self.original_y_pos = pos[1]

        # top rect
        self.top_rect = pygame.Rect(pos, (width, height))
        self.top_colour = '#FFFFFF'

        # bottom rect
        self.bottom_rect = pygame.Rect(pos, (width, elevation))
        self.bottom_colour = '#8800e7'

        # text
        if images != None:
            self.text_surf_normal = pygame.image.load(images[0]).convert_alpha()
            self.text_surf_normal = pygame.transform.rotozoom(self.text_surf_normal, 0, scale)
            self.text_surf_hover = pygame.image.load(images[1]).convert_alpha()
            self.text_surf_hover = pygame.transform.rotozoom(self.text_surf_hover, 0, scale)
        else:
            self.text_surf_normal = font.render(text, True, '#8800e7')
            self.text_surf_hover = font.render(text, True, '#6302a8')

        self.text_surf = self.text_surf_normal
        self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)

        # action attr
        self.action = False

    def draw(self, screen):
        # elevation logic
        self.top_rect.y = self.original_y_pos - self.elevation
        self.text_rect.center = self.top_rect.center

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.elevation

        pygame.draw.rect(screen, self.bottom_colour, self.bottom_rect, border_radius = 12)
        pygame.draw.rect(screen, self.top_colour, self.top_rect, border_radius = 12)
        screen.blit(self.text_surf, self.text_rect)

        self.check_click()

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()

        # checks if button is being hovered over
        if self.top_rect.collidepoint(mouse_pos):
            # changes colours accordingly
            self.top_colour = '#c7c7c7'
            self.bottom_colour = '#6302a8'
            self.text_surf = self.text_surf_hover

            # checks if it has been pressed
            if pygame.mouse.get_pressed()[0]:
                self.elevation = 0
                self.pressed = True
            else:
                self.elevation = self.elevation_record
                if self.pressed:
                    print('click')
                    self.action = True
                    self.pressed = False
        else:
            self.elevation = self.elevation_record
            self.top_colour = '#FFFFFF'
            self.bottom_colour = '#8800e7'
            self.text_surf = self.text_surf_normal
        