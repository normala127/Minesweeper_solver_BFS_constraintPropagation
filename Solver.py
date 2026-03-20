import numpy as np
from Queue import *
from Cell import *
from Board import *
#TODO learn to create packages
#TODO make code simpler/shorter
#TODO use 4 principles of OOP
class Solver(Board):
    def start_game(self):
        self.create_user_grid()
        self.first_selected_cell_row = np.random.randint(0, 8)
        self.first_selected_cell_column = np.random.randint(0, 8)
        #self.first_selected_cell_column = 0 #for testing
        #self.first_selected_cell_row = 0
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

        if self.grid[self.first_selected_cell_row, self.first_selected_cell_column] > 0:
            self.user_grid[self.first_selected_cell_row, self.first_selected_cell_column] = self.grid[self.first_selected_cell_row, self.first_selected_cell_column]
        if self.grid[self.first_selected_cell_row, self.first_selected_cell_column] == 0:
            self.reveal_safe_cells((self.first_selected_cell_row, self.first_selected_cell_column ))

    def reveal_safe_cells(self, chosen):
        chosen_row, chosen_column = chosen

        queue = Queue()
        queue.enqueue([chosen_row,chosen_column])

        self.user_grid[chosen_row, chosen_column] = self.grid[chosen_row, chosen_column]
        self.check_for_numbers_in_reveal(chosen_row, chosen_column) 
        
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
                    if (self.grid[new_row,new_col] == 0 and self.user_grid[new_row, new_col] == 'N'):
                        self.user_grid[new_row, new_col] = self.grid[new_row,new_col]
                        queue.enqueue([new_row, new_col])
                        #print("element u q ", queue.peek())
                        '''print("----------ZA QUEUE SHOW GRID--------------")
                        self.show_grid(self.user_grid)
                        print("------------------------------------------")'''

                        self.check_for_numbers_in_reveal(new_row, new_col) 
        print("---------------------------")
        self.show_grid(self.user_grid)    
        print("---------------------------")                    

    def check_for_numbers_in_reveal(self, new_row, new_col):
        if (new_row - 1 > - 1 and self.grid[new_row - 1,new_col] > 0):
            self.user_grid[new_row-1, new_col] = self.grid[new_row - 1,new_col]
                     
        if (new_row + 1 < 9 and self.grid[new_row + 1,new_col] > 0):
            self.user_grid[new_row + 1, new_col] = self.grid[new_row + 1,new_col]
                         
        if (new_col-1>-1 and self.grid[new_row,new_col-1]>0):
            self.user_grid[new_row, new_col - 1] = self.grid[new_row,new_col - 1]
                         
        if (new_col + 1 < 9 and self.grid[new_row, new_col + 1] > 0):
            self.user_grid[new_row, new_col + 1] = self.grid[new_row,new_col + 1]  
            '''print("----------ZA COL+1--------------")
            self.show_grid(self.user_grid)
            print("--------------------------------")'''


user = Solver()
user.start_game()