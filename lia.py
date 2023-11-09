import numpy as np
 
def create_grid():
    grid = np.zeros((6,7))
    return grid
 
grid = create_grid()
game_over = False
go = 0
 
while not game_over:
    # Request Player1 for an input
    if go == 0:
        position = int(input("Player1 choose your position (0-6):"))
    # Request Player2 for an input
    else:
        position = int(input("Player2 choose your position (0-6):"))
 
    go += 1
    go = go % 2 #alternate turns between player1 and 2