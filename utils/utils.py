import pygame, math, numpy as np

# from objects import Constant

def magnitude(arr):
    sq_sum = 0

    for i in arr:
        print(i)
        sq_sum += i**2

    print(sq_sum)
    return math.sqrt(sq_sum)

def generator():
    while True:
        yield 1
        yield 0

class FPS:
    def __init__(self):
        self.clock = pygame.time.Clock() 
        self.font = pygame.font.SysFont("Inter", 20)
        self.text = self.font.render(f"{round(self.clock.get_fps(), 1)} FPS", True, (255, 255, 255))
    
    def render(self, win, width):
        self.text = self.font.render(f"{round(self.clock.get_fps(), 1)} FPS", True, (255, 255, 255)) 
        win.blit(self.text, (width-20-self.text.get_width(), 20)) # renders FPS counter

