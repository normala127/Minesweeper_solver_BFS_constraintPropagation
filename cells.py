import numpy as np

class Queue:
    def __init__(self):
        self.queue=[]
    def enqueue(self, item):
        self.queue.append(item)
    def dequeue(self):
        if self.isEmpty():
            return
        else:
            self.queue.pop(0)
    def peek(self):
        return self.queue[0]
    def peekEnd(self):
        return self.queue[-1]
    def isEmpty(self):
        return len(self.queue)==0
    def size(self):
        return len(self.queue)

class Cell:
    def __init__(self, state, visability="N"):
        self.cell_state = state
        self.cell_visability = visability

#possible_states = {"Mine": -1, "Safe": 0, "Number": 1, "Not shown": 'N',}
#cell_hidden = 'N'

class Board:
    def __init__(self, dimension = (9, 9)):
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

    def set_mines(self, firstChosen): #vjerovatno moze krace omg
        mines_set = 0
        while mines_set < self.numnber_of_mines:
            while True:
                random_column = np.random.randint(0, 9)
                random_row = np.random.randint(0, 9)
                # random_column = 0 #for testing
                # random_row = 8
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

# b=Board()
# b.show_grid(b.grid)

user = Solver()
user.start_game()
