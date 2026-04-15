import numpy as np
from Queue import *
from Cell import *
from Board import *
import pygame
#TODO learn to create packages

class Solver(Board):
    # used for checking the cells around the selected cell
    dx = [-1, -1, -1, 0, 0, 1, 1, 1] 
    dy = [-1,  0,  1, -1, 1, -1, 0, 1]

    def start_game(self): # creates both grids, sets the mines, makes the first move
        self.create_user_grid()
        first_selected_cell_row = np.random.randint(ROWS)
        first_selected_cell_column = np.random.randint(COLS)

        self.create_grid()
        self.set_mines(firstChosen = (first_selected_cell_row, first_selected_cell_column))

        self.reveal_cell(first_selected_cell_row, first_selected_cell_column)

    def flood_fill_safe_cells(self, chosen): # reveals the safe cells using BFS, by assuming the initial cell is zero; flood-fill
        chosen_row, chosen_column = chosen
        queue = Queue()
        queue.enqueue([chosen_row, chosen_column])
        
        # find other safe cells (0 cells) using BFS
        while queue.isEmpty() == False:
            chosen_row = queue.peek()[0]
            chosen_column = queue.peek()[1]
            queue.dequeue()
            for i in range(8):
                new_row=chosen_row + self.dy[i]
                new_col=chosen_column + self.dx[i]  
        
                if (self.in_grid_bounds(new_row, new_col)):
                    if (self.grid[new_row][new_col].cell_state == 0 and self.user_grid[new_row][new_col].cell_visability == False):
                        self.reveal_cell(new_row, new_col)
                        queue.enqueue([new_row, new_col])

                        self.reveal_hints_flood_fill(new_row, new_col)                   

    def reveal_cell(self, new_row, new_col): # Changes the cell_state, image and visability and reveals blank cells if it is picked
        self.user_grid[new_row][new_col].cell_state = self.grid[new_row][new_col].cell_state
        self.user_grid[new_row][new_col].image = self.grid[new_row ][new_col].image
        self.user_grid[new_row][new_col].cell_visability = True

        if (self.user_grid[new_row][new_col].cell_state == 0):
            self.flood_fill_safe_cells((new_row, new_col))

    def reveal_hints_flood_fill(self, new_row, new_col): # makes sure the flood fill goes one cell beyond to reveal the number hints
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
  
    def in_grid_bounds(self, new_row, new_col): # checks the cell being checked is in the grid bounds
        return bool(new_row >= 0 and new_row < ROWS and new_col >= 0 and new_col < COLS)
    
    def constraint_propagation(self, screen):
        cells_to_check = Queue()
        for row in self.user_grid:
            for cell in row:
                if cell.cell_visability and cell.cell_state != 0:
                    cells_to_check.enqueue([cell.y//TILESIZE, cell.x//TILESIZE])

        # basic constraints
        while cells_to_check.isEmpty() == False:
            touch = 0
            flagged = 0
            to_flag = []

            chosen_row = cells_to_check.peek()[0]
            chosen_column = cells_to_check.peek()[1]

            cells_to_check.dequeue()
            
            # if the cell is 0, flood fill
            if self.user_grid[chosen_row][chosen_column].cell_state == 0: 
                self.flood_fill_safe_cells((chosen_row, chosen_column))
            
            # check how many unrevealed and flagged neighbour cells the cell has
            for i in range(8):
                new_row = chosen_row + self.dy[i]
                new_col = chosen_column + self.dx[i]  
                
                if (self.in_grid_bounds(new_row, new_col)):
                    if (self.user_grid[new_row][new_col].cell_visability == False):
                        to_flag.append(self.user_grid[new_row][new_col])
                        touch += 1
                    if (self.user_grid[new_row][new_col].flagged):
                        flagged += 1
            
            if flagged == self.user_grid[chosen_row][chosen_column].cell_state and flagged>0:                 
                # if the cell's state is the same as the number of flagged cells around it, then other unflagged neighbour cells should be revealed
                for i in range(8):
                    new_row=chosen_row + self.dy[i]
                    new_col=chosen_column + self.dx[i]

                    if (self.in_grid_bounds(new_row, new_col)):
                        if (not self.user_grid[new_row][new_col].cell_visability and not self.user_grid[new_row][new_col].flagged):
                            self.reveal_cell(new_row,new_col)
                            if (self.user_grid[new_row][new_col].cell_state > 0):
                                cells_to_check.enqueue([new_row, new_col])                               

            elif touch == self.user_grid[chosen_row][chosen_column].cell_state and touch>0:
                # if the cell is touching the same amount of cells as it's state, then flag those cells it is touching                
                for cell in to_flag:                   
                    cell.cell_state = -1
                    cell.flagged = True
                    cell.image = tile_flag

                    # enque the cells that surround the flag
                    for i in range(8):
                                nr = cell.y // TILESIZE + self.dy[i]
                                nc = cell.x // TILESIZE + self.dx[i]
                                
                                if (self.in_grid_bounds(nr, nc)):
                                    if self.user_grid[nr][nc].cell_visability and self.user_grid[nr][nc].cell_state > 0:
                                        cells_to_check.enqueue([nr, nc])
                                        
            self.draw(screen)
            pygame.display.update()
            pygame.time.delay(SPEED)

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
        valid_candidates=[(r,c) for r in range(ROWS) for c in range (COLS) if not self.user_grid[r][c].cell_visability and not self.user_grid[r][c].flagged]
        if not valid_candidates:
            return False
        
        random_row, random_column = valid_candidates[np.random.randint(0, len(valid_candidates))]

        self.reveal_cell(random_row, random_column)
        self.draw(screen)
        pygame.display.update()
        pygame.time.delay(SPEED) 

        if (self.user_grid[random_row][random_column].cell_state == 0):
            self.flood_fill_safe_cells((random_row, random_column))

        if (self.grid[random_row][random_column].cell_state == -1):
            return True
        else:
            return False

# TODO subset constraints
