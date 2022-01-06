from grid2D import grid2D
import math

class dataGrid2D():
    def __init__(self,grid:grid2D) -> None:
        self.grid = grid
        self.data = [0.0] * self.grid._nGridPoints


    def zero(self):
        self.data = [0.0] * self.grid._nGridPoints

    def square(self):
        self.data = [x*x for x in self.data]

    def sqrt(self):
        self.data = [math.sqrt(x) for x in self.data]

    def reciprocal(self):
        for num in self.data:
            if num == 0:
                raise "exception, reciprocal divides by zero"
            num = 1/num

    def conjugate(self):
        raise NotImplementedError

    def random(self):
        raise NotImplementedError

    def randomSaurabh(self):
        raise NotImplementedError

    def norm(self):
        raise NotImplementedError
        #return math.sqrt(self.innerProduct(self))
    
    def relNorm(self):
        raise NotImplementedError

    def summation(self):
        raise NotImplementedError

    def innerProduct(self, rhs) -> float:
        raise NotImplementedError

    def dotProduct(self)-> float:
        raise NotImplementedError

    def gradient(self)-> float:
        raise NotImplementedError

    def getRealPart(self):
        raise NotImplementedError

    
