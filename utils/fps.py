import pygame

class FPS:
    def __init__(self):
        self.clock = pygame.time.Clock() 
        self.font = pygame.font.SysFont("Inter", 20)
        self.text = self.font.render(f"{round(self.clock.get_fps(), 1)} FPS", True, (255, 255, 255))
    
    def render(self, win, width):
        # renders FPS counter
        self.text = self.font.render(f"{round(self.clock.get_fps(), 1)} FPS", True, (255, 255, 255)) 
        win.blit(self.text, (width-20-self.text.get_width(), 20))
