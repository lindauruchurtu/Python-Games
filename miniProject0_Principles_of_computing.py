"""
Clone of 2048 game.
"""

import poc_2048_gui
import random

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.    
OFFSETS = {UP: (1, 0), 
           DOWN: (-1, 0), 
           LEFT: (0, 1), 
           RIGHT: (0, -1)} 
   
def merge(line):
    """
    Helper function that takes the list line as a parameter and returns a new list 
    with the tile values from line slid towards the front of the list and merged
    """
    aux_list = list()
    merge_flag = 0
    
    # iterate through line elements
    for item in line:
        if len(aux_list) == 0 and item != 0:
            aux_list.append(item)
        elif item != 0:
            if (merge_flag != 1 and item == aux_list[len(aux_list) - 1]):
                merge_flag = 1
                aux_list[len(aux_list)-1] = 2 * aux_list[len(aux_list) - 1]
            else:
                aux_list.append(item)
                merge_flag = 0
        elif item == 0:
            pass

    while len(aux_list) != len(line):
        aux_list.append(0)
    return(aux_list)

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        self.height = grid_height
        self.width = grid_width
        self.grid = self.reset()
        
        # Generate list / dict of boundaries
        up_list = []
        down_list = []
        left_list = []
        right_list = []
        
        for col in range(self.width):
            up_list.append([0, col])
            down_list.append([self.height-1, col])

        for row in range(self.height):
            left_list.append([row, 0])
            right_list.append([row, self.width-1])
        
        self.boundaries = { UP: up_list, DOWN: down_list, LEFT: left_list, RIGHT: right_list}
        
    def reset(self):
        """
        Reset the game so the grid is empty.
        """
        self.grid = []
        for row in range(self.height):
            self.grid.append([])
            for dummy_col in range(self.width):
                self.grid[row].append(0)
        return self.grid
        
    
    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        string_rep = ""
        for elem in self.grid:
            string_rep += str(elem) + "\n"
        return string_rep

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self.height
    
    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self.width
                            
    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        # retrieve corresponding list
        boundary = self.boundaries[direction]

        temp = []
        aux = []
        
        for tile in boundary:
            temp = []
            row_index = tile[0]
            col_index = tile[1]
            
            if direction == 1 or direction == 2:
                limit = self.height
            elif direction == 3 or direction == 4:
                limit = self.width
            
            for num in range(limit):
                temp.append(self.grid[row_index][col_index])
                
                row_index = row_index + OFFSETS[direction][0]
                col_index = col_index + OFFSETS[direction][1]

            aux.append(merge(temp))
          
        for tile in boundary:
            row_index = tile[0]
            col_index = tile[1]
            
            if direction == 1 or direction ==2:
                for num in range(self.height): 
                    self.grid[row_index][col_index] = aux[col_index][num]
                    row_index = row_index + OFFSETS[direction][0]
                    col_index = col_index + OFFSETS[direction][1]
            elif direction ==3 or direction ==4:
                for num in range(self.width):
                    self.grid[row_index][col_index] = aux[row_index][num]
                    row_index = row_index + OFFSETS[direction][0]
                    col_index = col_index + OFFSETS[direction][1]
        
        self.new_tile()
        
    def new_tile(self):
        """
        Create a new tile in a randomly selected empty 
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        pos_zeros = []
        for row in range(self.height):
            for col in range(self.width):
                if self.grid[row][col] == 0:
                    pos_zeros.append([row,col])
        
        if len(pos_zeros) == 0:
            return
        else:
            tile = random.choice(pos_zeros)
            value = random.choice([2, 2, 2, 2, 2, 2, 2, 2, 2, 4])
            self.set_tile(tile[0], tile[1], value)

        
    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """        
        self.grid[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """        
        return self.grid[row][col]   
      
poc_2048_gui.run_gui(TwentyFortyEight(4, 4))
