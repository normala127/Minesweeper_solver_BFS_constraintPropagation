import numpy as np
class Cell:
    def __init__(self, state):
        self.cellState=state

possibleStates={
    "Mine":-1,
    "Safe":0,
    "Number":1
}
#just to see
a=3
cellHidden=True

class Board:
    def __init__(self, dimension=(9,9)):
        self.rows=dimension[0]
        self.columns=dimension[1]
        self.cell=Cell(0)
        self.numnberOfMines=10
    
    def createGrid(self):
        self.grid=np.array([[self.cell.cellState]*9 for i in range(self.rows)])
        print("No of rows ", len(self.grid))
        print("No of columns ", len(self.grid[0]))
        print(self.grid[1,1])
        self.setMines()
    
    def setMines(self):
        minesSet=0
        while minesSet < self.numnberOfMines:
            while True:
                randomColumn=np.random.randint(0,9)
                randomRow=np.random.randint(0,9)
                #randomColumn=0 for testing
                #randomRow=8
                if self.grid[randomRow,randomColumn]!=-1:
                    self.grid[randomRow,randomColumn]=-1
                    print("Row " ,randomRow, "Column " , randomColumn)
                    break
                
            #adjusting the hints 
            if randomRow!=0:
                i=randomRow-1
                print("Izabrana je opcija 1")
                r=-1
            else:
                i=randomRow
                print("Izabrana je opcija 2")
                r=0
                
            if randomColumn!=0:
                j=randomColumn-1
                print("Izabrana je opcija 3")
                l=-1
            else:
                j=randomColumn
                print("Izabrana je opcija 4")
                l=0

            for k in range(2-r):
                for m in range(2-l):
                    if self.grid[i,j] !=-1 and i<9:
                        self.grid[i,j] +=1
                        print("dodaN BROJ")
                    if j==self.columns-1:
                        break
                    j+=1
                j=randomColumn+l
                print("------------------------")
                self.showGrid()
                print("------------------------")
                if i==self.rows-1:
                    break
                i+=1
            minesSet+=1

        
    def showGrid(self):
        for row in self.grid:
            print(row)


b=Board()
b.createGrid()

b.showGrid()

#grid=[[0]*9 for i in range(9)]
#for row in grid:
#    print(row)