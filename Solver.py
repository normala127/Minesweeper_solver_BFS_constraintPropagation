import numpy as np
from Queue import *
from Cell import *
from Board import *
import pygame
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
        chosen_row, chosen_column = chosen

        queue = Queue()
        queue.enqueue([chosen_row, chosen_column])

        self.user_grid[chosen_row][chosen_column].image = self.grid[chosen_row][chosen_column].image 
        self.user_grid[chosen_row][chosen_column].cell_state = self.grid[chosen_row][chosen_column].cell_state
        self.check_for_numbers_in_reveal(chosen_row, chosen_column) 
        
        # find other safe cells
        dx = [-1, -1, -1, 0, 0, 1, 1, 1]
        dy = [-1,  0,  1, -1, 1, -1, 0, 1]

        while queue.isEmpty() == False:
            chosen_row = queue.peek()[0]
            chosen_column = queue.peek()[1]
            queue.dequeue()
            for i in range(8):
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

    def reveal_cell(self, new_row, new_col): # TODO use this where possible
        self.user_grid[new_row][new_col].cell_state = self.grid[new_row][new_col].cell_state
        self.user_grid[new_row][new_col].image = self.grid[new_row ][new_col].image
        self.user_grid[new_row][new_col].cell_visability = True


    def check_for_numbers_in_reveal(self, new_row, new_col):
        if (new_row - 1 >= 0 and self.grid[new_row-1][new_col].cell_state > 0):
            self.reveal_cell(new_row=new_row-1, new_col=new_col)

            if (new_col -1 > -1 and self.grid[new_row - 1][new_col - 1].cell_state > 0):
                self.reveal_cell(new_row=new_row-1, new_col=new_col-1)
            if (new_col + 1 < 9 and self.grid[new_row - 1][ new_col + 1].cell_state > 0):
                self.reveal_cell(new_row=new_row - 1, new_col=new_col + 1)

        if (new_row + 1 < 9 and self.grid[new_row + 1][new_col].cell_state > 0):
            self.reveal_cell(new_row=new_row + 1, new_col=new_col)

            if (new_col - 1 > -1 and self.grid[new_row + 1][new_col - 1].cell_state > 0):
                self.reveal_cell(new_row=new_row+1, new_col=new_col - 1)
            if (new_col + 1 < 9 and self.grid[new_row + 1][ new_col + 1].cell_state > 0):
                self.reveal_cell(new_row=new_row + 1, new_col=new_col + 1)
                         
        if (new_col - 1 > -1 and self.grid[new_row][new_col-1].cell_state > 0):
            self.reveal_cell(new_row=new_row, new_col=new_col - 1)
                         
        if (new_col + 1 < 9 and self.grid[new_row][ new_col + 1].cell_state > 0):
            self.reveal_cell(new_row=new_row, new_col=new_col + 1)
  


    def constraint_propagation(self, screen):
        cells_to_check = Queue()
        for row in self.user_grid:
            for cell in row:
                if cell.cell_visability and cell.cell_state != 0:
                    cells_to_check.enqueue([cell.y//TILESIZE, cell.x//TILESIZE])

        # constraint 1
        dx = [-1, -1, -1, 0, 0, 1, 1, 1]
        dy = [-1,  0,  1, -1, 1, -1, 0, 1]
        to_be_revealed = []

        while cells_to_check.isEmpty() == False:
            print("SIZE F Q: ",cells_to_check.size())
            touch = 0
            flagged = 0
            to_flag = []
            chosen_row = cells_to_check.peek()[0]
            chosen_column = cells_to_check.peek()[1]
            cells_to_check.dequeue()
            print("Dequeued:", chosen_row," ", chosen_column)
            if self.user_grid[chosen_row][chosen_column].cell_state == 0:
                to_be_revealed.append((chosen_row, chosen_column))
                continue
            for i in range(8):
                new_row=chosen_row + dy[i]
                new_col=chosen_column + dx[i]  
                
                if (new_row >= 0 and new_row <= 8 and new_col >= 0 and new_col <=8):
                    if (self.user_grid[new_row][new_col].cell_visability == False):
                        to_flag.append(self.user_grid[new_row][new_col])
                        touch+=1
                    if (self.user_grid[new_row][new_col].flagged):
                        flagged+=1
            
            if flagged == self.user_grid[chosen_row][chosen_column].cell_state and flagged>0: 
                print("Amount of flags: ", flagged, "cell state: ", self.user_grid[chosen_row][chosen_column].cell_state)
                # logic that says if the cell's state is the same as the number of flagged cells around it, then other unflagged cells should be revealed
                for i in range(8):
                    new_row=chosen_row + dy[i]
                    new_col=chosen_column + dx[i]
                    if (new_row >= 0 and new_row <= 8 and new_col >= 0 and new_col <=8):
                        if (self.user_grid[new_row][new_col].cell_visability == False and not self.user_grid[new_row][new_col].flagged):
                            self.user_grid[new_row][new_col].cell_visability = True
                            self.user_grid[new_row][new_col].cell_state = self.grid[new_row][new_col].cell_state
                            self.user_grid[new_row][new_col].image = self.grid[new_row][new_col].image
                            if (self.user_grid[new_row][new_col].cell_state > 0):
                                cells_to_check.enqueue([new_row, new_col])
                                print("Enqueued in flagged: ", new_row, " ", new_col)

            elif touch == self.user_grid[chosen_row][chosen_column].cell_state and touch>0:
                # logic that says if the cell is touching the same amount of cells as it's state, then flag those cells it is toucing, it is a mine
                print("Amount of touches: ", touch, "cell state: ", self.user_grid[chosen_row][chosen_column].cell_state)
                for cell in to_flag:                   
                    cell.cell_state = -1
                    cell.flagged = True
                    cell.image = tile_flag
                    # enque the cells that surround the flag
                    for i in range(8):
                                nr = cell.y // TILESIZE + dy[i]
                                nc = cell.x // TILESIZE + dx[i]
                                print("in touch: ",nr, nc)
                                if (0 <= nr <= 8 and 0 <= nc <= 8):
                                    if self.user_grid[nr][nc].cell_visability and self.user_grid[nr][nc].cell_state > 0:
                                        cells_to_check.enqueue([nr, nc])
                                        print("Enqueued in touched: ", nr, " ", nc)

            '''print("constraint USER")
            self.show_grid(self.user_grid) 
            print(cells_to_check.size())'''
            self.draw(screen)
            pygame.display.update()
            pygame.time.delay(200)
        for item in to_be_revealed:
            self.reveal_safe_cells(item)

    def is_solved(self): # checks if the board has been solved or if solver lost/clicked a mine
        flagged_count = 0
        for row in self.user_grid:
            for cell in row:
                if cell.flagged:
                    flagged_count += 1
                if not cell.cell_visability and not cell.flagged:
                    return False
        if flagged_count != AMOUNT_MINES:
            return False
        return True

    def solve(self, screen): # solves the board using constraint prop and if needed random guess
        while not self.is_solved():
            self.constraint_propagation(screen)
            if not self.is_solved():
                lost = self.random_guess(screen)
                if lost:
                    return


    def random_guess(self, screen): #defaults to this if constraint prop is not enough
        print("RANDOMM GUESS TIME")
        valid_candidates=[(r,c) for r in range(ROWS) for c in range (COLS) if not self.user_grid[r][c].cell_visability and not self.user_grid[r][c].flagged]
        if not valid_candidates:
            return False
        random_row, random_column = valid_candidates[np.random.randint(0, len(valid_candidates))]
        self.reveal_cell(random_row, random_column)
        self.draw(screen)
        pygame.display.update()
        pygame.time.delay(200)   
        if (self.user_grid[random_row][random_column].cell_state == 0):
            self.reveal_safe_cells((random_row, random_column))    
        if (self.grid[random_row][random_column].cell_state == -1):
            return True
        else:
            return False

# TODO subset constraints
