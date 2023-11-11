import numpy as np
 
ROW_COUNT = 6
POSITION_COUNT = 7
 
def create_grid():
    grid = np.zeros((ROW_COUNT,POSITION_COUNT))
    return grid
 
def place_piece(grid, row, position, counter):
    grid[row][position] = counter
 
def is_valid_location(grid, position): #checking to see if a counter can be placed here, or if the space in the grid is full
    return grid[ROW_COUNT-1][position] == 0
 
def get_next_available_row(grid, position): #checking to see what row the piece will fall on
    for r in range(ROW_COUNT):
        if grid[r][position] == 0: #if the space is still zero, then it is empty and it will return the first time this occurs
            return r
        
def print_grid(grid):
    print(np.flip(grid, 0))
 
def winning_move(grid, counter): #makes the player aware that they won
    #check horizontal locations for win
    for c in range(POSITION_COUNT-3):
        for r in range(c):
            if grid[r][position] == counter and grid[r][position+1] == counter and grid[r][position+2] == counter and grid[r][position+3] == counter:
                return True
    # return False
            
    #check vertical locations for win
 
 
grid = create_grid()
print_grid(grid)
game_over = False
go = 0
 
while not game_over:
    # Request Player1 for an input
    if go == 0:
        position = int(input("Player1 choose your position (0-6):"))
 
        if is_valid_location(grid, position):
            row = get_next_available_row(grid, position)
            place_piece(grid, row, position, 1)
 
            if winning_move(grid, 1):
                print("CONGRATULATIONS PLAYER 1, YOU WIN!!!")
                game_over = True
 
   
   
    # Request Player2 for an input
    else:
        position = int(input("Player2 choose your position (0-6):"))
 
        if is_valid_location(grid, position):
            row = get_next_available_row(grid, position)
            place_piece(grid, row, position, 2)
 
    print_grid(grid)
 
    go += 1
    go = go % 2 #alternate turns between player1 and 2