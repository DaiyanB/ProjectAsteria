class Timestep:
    def __init__(self, original_timestep):
        self.original_timestep = original_timestep
        self.timestep = original_timestep

    def get_timestep(self):
        return self.timestep
    
    def get_original_timestep(self):
        return self.original_timestep
    
    def update_timestep(self, new_timestep):
        if new_timestep > (max_timestep := 4*self.original_timestep):
            self.timestep = max_timestep
        elif new_timestep < (min_timestep := 0.25*self.original_timestep):
            self.timestep = min_timestep
        else:
            self.timestep = new_timestep
    
    def reset(self):
        self.timestep = self.original_timestep