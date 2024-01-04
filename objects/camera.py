import numpy as np
from numpy.linalg import norm

import pygame, math
from pygame import gfxdraw
from math import sin, cos, atan2, degrees, radians

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