from grid2D import grid2D
import math
import numpy as np

class dataGrid2D():
    def __init__(self,grid:grid2D) -> None:
        self.grid = grid
        self.data = [0.0] * self.grid._nGridPoints

    def getData(self):
        return self.data

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
        for i in self.data:
            i = np.conj(i)

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
        res = []
        for i in self.data:
            res.append(i.real)
        return res

    def __truediv__(self, rhs):
        if isinstance(rhs,dataGrid2D):
            for i in range(len(self.data)):
                self.data[i] /= rhs.data[i]
        else:
            for i in self.data:
                i /= rhs

        return self
            
    def __mul__(self,rhs):
        if isinstance(rhs,dataGrid2D):
            for i in range(len(self.data)):
                self.data[i] *= rhs.data[i]
        else:
            for i in self.data:
                i *= rhs
        return self
            
    def __sub__(self,rhs):
        if isinstance(rhs,dataGrid2D):
            for i in range(len(self.data)):
                self.data[i] -= rhs.data[i]
        else:
            for i in self.data:
                i -= rhs
        return self

    def __add__(self,rhs):
        if isinstance(rhs,dataGrid2D):
            for i in range(len(self.data)):
                self.data[i] += rhs.data[i]
        else:
            for i in self.data:
                i += rhs
        return self