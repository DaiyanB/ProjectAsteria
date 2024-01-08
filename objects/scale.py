import pygame

from .constant import Constant

class Scale:
    # class to set and display the scale
    def __init__(self, Constant):
        self.Constant = Constant

        self.font = pygame.font.SysFont("Inter", 20)
        self.text = self.font.render(f"{int(round(self.SCALE*Constant.AU, 0))} px per AU", True, (255, 255, 255))

    @property
    def SCALE(self):
        return self.Constant.SCALE

    def render(self, win, width, zoom_scale):
        # zoom_scale = 1
        pos = (width-20-self.text.get_width(), 40)
        self.text = self.font.render(f"{int(round(self.SCALE*Constant.AU*zoom_scale, 0))} px per AU", True, (255, 255, 255))
        win.blit(self.text, pos)