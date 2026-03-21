import numpy as np
from Queue import *
from Cell import *
from Board import *
#TODO learn to create packages

class Solver(Board):
    def start_game(self):
        self.create_user_grid()
        self.first_selected_cell_row = np.random.randint(0, 8)
        self.first_selected_cell_column = np.random.randint(0, 8)

        print(
            "Comp chose :",
            self.first_selected_cell_row,
            " ",
            self.first_selected_cell_column,
        )
        self.create_grid()
        self.set_mines(
            firstChosen = (self.first_selected_cell_row, self.first_selected_cell_column)
        )
        print("ZA TACAN GRID SHOWGRID")
        self.show_grid(self.grid)

        if self.grid[self.first_selected_cell_row][ self.first_selected_cell_column].cell_state > 0:
            self.user_grid[self.first_selected_cell_row][ self.first_selected_cell_column].cell_state = self.grid[self.first_selected_cell_row][self.first_selected_cell_column].cell_state
            self.user_grid[self.first_selected_cell_row][ self.first_selected_cell_column].image = self.grid[self.first_selected_cell_row][self.first_selected_cell_column].image
            self.user_grid[self.first_selected_cell_row][ self.first_selected_cell_column].cell_visability = True
            self.show_grid(self.user_grid)    
            print("---------------------------") 
        if self.grid[self.first_selected_cell_row][ self.first_selected_cell_column].cell_state == 0:
            self.reveal_safe_cells((self.first_selected_cell_row, self.first_selected_cell_column ))

    def reveal_safe_cells(self, chosen):
        #self.chosen_row, self.chosen_column = chosen

        queue = Queue()
        queue.enqueue([self.first_selected_cell_row,self.first_selected_cell_column])

        self.user_grid[self.first_selected_cell_row][self.first_selected_cell_column].image = self.grid[self.first_selected_cell_row][self.first_selected_cell_column].image #TODO ne vidi se 
        self.user_grid[self.first_selected_cell_row][self.first_selected_cell_column].cell_state = self.grid[self.first_selected_cell_row][self.first_selected_cell_column].cell_state
        self.check_for_numbers_in_reveal(self.first_selected_cell_row, self.first_selected_cell_column) 
        
        # find other safe cells
        dx = [0, 1, 0, -1]
        dy = [1, 0, -1, 0]

        while queue.isEmpty() == False:
            chosen_row = queue.peek()[0]
            chosen_column = queue.peek()[1]
            queue.dequeue()
            for i in range(4):
                new_row=chosen_row + dy[i]
                new_col=chosen_column + dx[i]  

        
                if (new_row >= 0 and new_row <= 8 and new_col >= 0 and new_col <=8):
                    if (self.grid[new_row][new_col].cell_state == 0 and self.user_grid[new_row][new_col].cell_visability == False):
                        self.user_grid[new_row][new_col].cell_state = self.grid[new_row][new_col].cell_state
                        self.user_grid[new_row][new_col].image = self.grid[new_row][new_col].image
                        self.user_grid[new_row][new_col].cell_visability=True
                        queue.enqueue([new_row, new_col])

                        self.check_for_numbers_in_reveal(new_row, new_col) 
        print("---------------------------")
        self.show_grid(self.user_grid)    
        print("---------------------------")                    

    def check_for_numbers_in_reveal(self, new_row, new_col):
        if (new_row - 1 >= 0 and self.grid[new_row-1][new_col].cell_state > 0):
            self.user_grid[new_row-1][new_col].cell_state = self.grid[new_row - 1][new_col].cell_state
            self.user_grid[new_row-1][new_col].image = self.grid[new_row - 1][new_col].image
            self.user_grid[new_row-1][new_col].cell_visability = True
                     
        if (new_row + 1 < 9 and self.grid[new_row + 1][new_col].cell_state > 0):
            self.user_grid[new_row + 1][ new_col].cell_state = self.grid[new_row + 1][new_col].cell_state
            self.user_grid[new_row + 1][ new_col].image = self.grid[new_row + 1][new_col].image
            self.user_grid[new_row + 1][ new_col].cell_visability = True
                         
        if (new_col-1>-1 and self.grid[new_row][new_col-1].cell_state > 0):
            self.user_grid[new_row][ new_col - 1].cell_state = self.grid[new_row][new_col - 1].cell_state
            self.user_grid[new_row][ new_col - 1].image = self.grid[new_row][new_col - 1].image
            self.user_grid[new_row][ new_col - 1].cell_visability = True
                         
        if (new_col + 1 < 9 and self.grid[new_row][ new_col + 1].cell_state > 0):
            self.user_grid[new_row][ new_col + 1].cell_state = self.grid[new_row][new_col + 1].cell_state
            self.user_grid[new_row][ new_col + 1].image = self.grid[new_row][new_col + 1].image
            self.user_grid[new_row][ new_col + 1].cell_visability = True  
