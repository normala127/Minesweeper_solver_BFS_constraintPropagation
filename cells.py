import numpy as np
import Queue

class Cell:
    def __init__(self, state, visability="N"):
        self.cell_state = state
        self.cell_visability = visability


possible_states = {"Mine": -1, "Safe": 0, "Number": 1}

cell_hidden = True


class Board:
    def __init__(self, dimension=(9, 9)):
        self.rows = dimension[0]
        self.columns = dimension[1]
        self.cell = Cell(0)
        self.numnber_of_mines = 10
        self.create_grid()

    def create_user_grid(self):
        self.user_grid = np.array(
            [[self.cell.cell_visability] * 9 for i in range(self.rows)]
        )
        self.show_grid(self.user_grid)

    def create_grid(self):
        self.grid = np.array([[self.cell.cell_state] * 9 for i in range(self.rows)])
        # print("No of rows ", len(self.grid))
        # print("No of columns ", len(self.grid[0]))
        # print(self.grid[1,1])
        # self.set_mines()

    def set_mines(self, firstChosen):
        mines_set = 0
        while mines_set < self.numnber_of_mines:
            while True:
                random_column = np.random.randint(0, 9)
                random_row = np.random.randint(0, 9)
                # random_column=0 #for testing
                # random_row=8
                if (
                    self.grid[random_row, random_column] != -1
                    and (random_row, random_column) != firstChosen
                ):
                    self.grid[random_row, random_column] = -1
                    # print("Row " ,randomRow, "Column " , randomColumn)
                    break

            # adjusting the hints
            if random_row != 0:
                i = random_row - 1
                # print("Izabrana je opcija 1")
                r = -1
            else:
                i = random_row
                # print("Izabrana je opcija 2")
                r = 0

            if random_column != 0:
                j = random_column - 1
                # print("Izabrana je opcija 3")
                l = -1
            else:
                j = random_column
                # print("Izabrana je opcija 4")
                l = 0

            for k in range(2 - r):
                for m in range(2 - l):
                    if self.grid[i, j] != -1 and i < 9:
                        self.grid[i, j] += 1
                        # print("dodaN BROJ")
                    if j == self.columns - 1:
                        break
                    j += 1
                j = random_column + l
                # print("------------------------")
                # self.showGrid()
                # print("------------------------")
                if i == self.rows - 1:
                    break
                i += 1
            mines_set += 1
            # break

    def show_grid(self, grid):
        for row in grid:
            print(row)


class Solver(Board):
    def start_game(self):
        self.first_selected_cell_row = np.random.randint(0, 8)
        self.first_selected_cell_column = np.random.randint(0, 8)
        # self.first_selected_cell_column=0 #for testing
        # self.first_selected_cell_row=8
        print(
            "Comp chose :",
            self.first_selected_cell_row,
            " ",
            self.first_selected_cell_column,
        )
        self.create_grid()
        self.set_mines(
            firstChosen=(self.first_selected_cell_row, self.first_selected_cell_column)
        )
        self.show_grid(self.grid)

    def reveal_safe_cells(self, chosen):
        chosen_row = chosen[0]
        chosen_column = chosen[1]

        queue= Queue()

        if self.grid[chosen_row, chosen_column] == 0:
            self.user_grid[chosen_row, chosen_column] = self.grid[chosen_row, chosen_column]
            
            # find other safe cells
            if self.grid[chosen_row-1, chosen_column] == 0:
                queue.enqueue(self.grid[chosen_row-1, chosen_column])
            
            if self.grid[chosen_row+1, chosen_column] == 0:
                queue.enqueue(self.grid[chosen_row+1, chosen_column])
            
            if self.grid[chosen_row, chosen_column-1] == 0:
                queue.enqueue(self.grid[chosen_row, chosen_column-1])

            if self.grid[chosen_row, chosen_column+1] == 0:
                queue.enqueue(self.grid[chosen_row, chosen_column+1])

            #edge cases kad su 0 i 8 vrijednosti

            for i in range(3,2): # ovo provjerava za rows je li nula i dodaje u queue
                if chosen_row == 0:
                    continue
                if self.grid[chosen_row-1+i, chosen_column] == 0:
                    queue.enqueue([chosen_row-1+i, chosen_column])
                if chosen_row-1 == 7:
                    i+=5
            
            for i in range(3,2): # ovo provjerava za columns je li nula i dodaje u queue
                if chosen_column==0:
                    continue
                if self.grid[chosen_row,chosen_column-1+i] == 0:
                    queue.enqueue([chosen_row,chosen_column-1+i])
                if chosen_column-1==7:
                    i+=5
            



# b=Board()
# b.show_grid(b.grid)


user = Solver()
user.start_game()
