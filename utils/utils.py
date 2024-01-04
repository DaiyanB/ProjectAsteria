import pygame

# class FPS:
#     def __init__(self):
#         self.clock = pygame.time.Clock() 
#         self.font = pygame.font.SysFont("Inter", 20)
#         self.text = self.font.render(f"{round(self.clock.get_fps(), 1)} FPS", True, (255, 255, 255))
    
#     def render(self, win, width):
#         # renders FPS counter
#         self.text = self.font.render(f"{round(self.clock.get_fps(), 1)} FPS", True, (255, 255, 255)) 
#         win.blit(self.text, (width-20-self.text.get_width(), 20))

# class Timestep:
#     def __init__(self, original_timestep):
#         self.original_timestep = original_timestep
#         self.timestep = original_timestep

#     def get_timestep(self):
#         return self.timestep
    
#     def get_original_timestep(self):
#         return self.original_timestep
    
#     def update_timestep(self, new_timestep):
#         if new_timestep > (max_timestep := 4*self.original_timestep):
#             self.timestep = max_timestep
#         elif new_timestep < (min_timestep := 0.25*self.original_timestep):
#             self.timestep = min_timestep
#         else:
#             self.timestep = new_timestep
    
#     def reset(self):
#         self.timestep = self.original_timestep

# def draw_text(text, font, text_col, coords, screen):
#     text = font.render(text, True, text_col)
#     screen.blit(text, coords)

# def get_average_color(surf):
#     color = pygame.transform.average_color(surf, surf.get_rect())
#     pxiel_count = pygame.mask.from_surface(surf).count()
#     scale = surf.get_width() * surf.get_height() / pxiel_count
#     return (round(color[0]*scale), round(color[1]*scale), round(color[2]*scale))

# def magnitude(arr):
#     sq_sum = 0

#     for i in arr:
#         print(i)
#         sq_sum += i**2

#     print(sq_sum)
#     return math.sqrt(sq_sum)

def generator():
    while True:
        yield 1
        yield 0