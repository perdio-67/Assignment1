import numpy as np
import copy 


#Rookie to Rockstar Full-Stack Intern
#Assignemt1

# Name  : Mohammed Al Sayed
# Email : m.alsayed2018@outlook.com

#Notes:
    # Some classes aren't needed but only were added as requested.
    # This approach is not the most effecient one, can be enhanced with more work and time.
    # I added few additional not needed functions just for my own interest.
    # I'm aware of the assumption that x<=y<1000 but chosen to make it open
    # All classes are in one file and that file is this.

class Dimention():

    def __init__(self, x, y):
        # Checking inputs type to be integers
        if not isinstance(x, int):
            raise TypeError("x must be of type integer")
        if not isinstance(y, int):
            raise TypeError("y must be of type integer")
        # Creating a list of dimensions
        self.dimension = (x,y)
    
    # function to scan the user for input
    def readDimension(self):
        print("**Setting up Dimesnions**")
        x = int(input('Enter Width(x)  : '))
        y = int(input('Enter Height(y) : '))
        self.dimension = (x,y)

    # overriding the print function
    def __str__(self):
        return "Width  = "+str(self.dimension[0])+"\nHeight = "+str(self.dimension[1])
    
class Grid():
    def __init__(self, dim = Dimention(6,6), auto=True):
        # Automatic generation of generation zero grid.
        if auto:
            # checking for input "dim" type
            if not isinstance(dim, Dimention):
                raise TypeError("dim must be of type Dimension")
            # writing it this ways is not dynamic cause this way it will only accept one class as dimensions,
            # but for the sake of using our Dimension class I'm forcing one type.
    
            # creating the grid of size dim as a numpy array of random 1s and 0s. 
            self.grid = np.random.random_sample((dim.dimension[1], dim.dimension[0]))+.5
            self.grid = self.grid.astype(int)

        # Manual generation of generation zero grid.
        else:
            dim.readDimension()
            # Generating a grid with the specified dimensions and dilling it with zeros
            self.grid = np.zeros((dim.dimension[1], dim.dimension[0]), dtype=int)
            print("Grid Width = ["+str(dim.dimension[0])+"], Height = ["+str(dim.dimension[1])+"].")
            print("**Setting up Grid cells**")
            # first loop, that will go line by line
            for i in range(dim.dimension[1]):
                # scan input from user for each line
                line = input('Enter Line '+str(i)+' :')
                if len(line)!=dim.dimension[0]:
                    raise TypeError("given string of length ["+str(len(x))+"] Expected length ["+str(dim.dimension[0])+"].")
                # Second loop, that will go number by number within the line  
                for j in range(dim.dimension[0]):
                    # Check each number in the line to be either 0 or 1
                    if line[j] !='0' and line[j]!='1':
                        raise TypeError("Given ["+str(line[j])+"], expected [0] or [1].")
                    # Assign the new cell value to the grid
                    self.grid[i][j] = line[j]
            print("\nEntered Grid is: ")
            print(self.grid)
    
    def countOfGreens(self, point):
        # assigning i and j : y, x
        i,j = point 
        # I'm going to slice the gird around the given point so all cells be treated the same
        # max() is being used for corners and sides so there can't be negative values.
        sliceGrid = self.grid[max(0,i-1):i+2,max(0,j-1):j+2]
        # counting number of 1s(nonzeros) in the sliced grid.
        greens = np.count_nonzero(sliceGrid)
        # checking the the point to subtract from greens a point.
        if self.grid[i,j]==1:
            greens -=1 
        # returning the counted nighbors 
        return greens


    def __str__(self):
        return str(self.grid)

class GreenVsRed():

    def __init__(self, mainGrid=Grid):
        if not isinstance(mainGrid, Grid):
            raise TypeError("grid must be of type Grid")
        self.mainGrid = mainGrid

    def nexGeneration(self, grid=None, N=1):
        # There are many ways to do this function, I will try and do it by eliminating
        # as much as i can of if statments.
        # 1 is green
        # 0 is red
        if grid is None:
            grid = self.mainGrid

        newGrid = copy.deepcopy(grid)

        #First loop for the number of generations
        for g in range(N):
            # creating a copy of the most recent mainGrid  as a reference for the newGrid
            ref = copy.deepcopy(newGrid)
            # second loop for the height y
            for i in range(ref.grid.shape[0]):  
                # third loop for the width x
                for j in range(ref.grid.shape[1]): 
                    greens = ref.countOfGreens((i,j))
                    #print("greens = "+str(greens)+" reds = "+str(reds))
                    # checking the first rule
                    if ref.grid[i,j]==0 and greens in [3,6]:
                        # Updating the cell value
                        newGrid.grid[i,j]=1

                    # i will ignore the second rule since it's already embedded in rule one.
                    # i will ignore the fourth rule since it's already embeded in rule three.

                    # chcecking the fourth rule
                    elif ref.grid[i,j]==1 and greens not in [2,3,6]:
                        # Updating the cell value
                        newGrid.grid[i,j]=0
        # return the new grid
        return newGrid
   
    def greenOcurencess(self, point, N, grid = None):
        # check if there is a grid input from user else assign the exsisted one.
        if grid is None:
            grid = self.mainGrid
        # set the counter to 0
        greenCount = 0
        # creating a copy if the main grid to edit.
        tempGrid = copy.deepcopy(grid)
        # loop for N iterations
        for i in range(N):
            # get the new grid
            tempGrid  = self.nexGeneration(tempGrid)
            # check if it's green to add 1 to the counter
            if tempGrid.grid[point[1],point[0]]== 1:
                greenCount +=1 
        # Return the counted ocurenceses
        return greenCount
    
    # function that reads point and N from the user
    def manualTest(self):
        self.mainGrid = Grid(auto=False)
        print("**Setting up point and N**")
        x = int(input('Enter Width(x)       : '))
        y = int(input('Enter Height(y)      : '))
        N = int(input('Enter N(Generations) : '))
        print("Result = "+str(self.greenOcurencess((x,y), N)))

    def test(self):
        #setting up variables
        # Creating the grid of the first example
        grid1 = Grid()
        grid1.grid = np.array([[0,0,0],[1,1,1],[0,0,0]])
        # Creating the grid of the second example
        grid2 = Grid()
        grid2.grid = np.array([[1,0,0,1],[1,1,1,1],[0,1,0,0],[1,0,1,0]])
        # creating point1, N1 for example1
        point1 = (1,0)
        N1     = 10
        # creating point2, N2 for example
        point2 = (2,2)
        N2     = 15
        # starting the test
        # start the counter for example1
        print(grid1.grid)
        print("Example1 result = "+str(self.greenOcurencess(point1, N1, grid1)))
        # start the counter for example2
        print(grid2.grid)
        print("Example2 result = "+str(self.greenOcurencess(point2, N2, grid2)))

if __name__ == "__main__":
    gVr = GreenVsRed(Grid(auto= True))
    # automated testing
    gVr.test()
    # manual testing
    #gVr.manualTest()
