from typing import List
from grid2D import grid2D
import math
import numpy as np
import copy

class dataGrid2D():
    def __init__(self,grid:grid2D,datatype=np.float64) -> None:
        self.grid = grid
        self.data = np.zeros(shape=self.grid._nGridPoints,dtype=datatype) #[0.0] * self.grid._nGridPoints
        self.datatype = datatype
    def getData(self):
        return self.data

    def zero(self):
        self.data =  np.zeros(shape=self.grid._nGridPoints,dtype=self.datatype)

    def square(self):
        self.data = np.square(self.data)

    def sqrt(self):
        self.data = np.sqrt(self.data)

   
    def conjugate(self):
        self.data = np.conj(self.data)
    
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
        return np.sum(self.data)

    def innerProduct(self, rhs) -> float:
        prod = 0.0
        for i in range(len(self.data)):
            prod+= (self.data[i]*np.conj(rhs.data[i])).real
        
        return prod

    def dotProduct(self)-> float:
        raise NotImplementedError

    def gradient(self, gradientField):
        
        gradientField[0].data = gradientField[0].data.astype(self.data.dtype)
        gradientField[1].data = gradientField[1].data.astype(self.data.dtype)
        nx = self.grid.getGridDimensions()
        dx = self.grid.getCellDimensions()

        for i in range(nx[1]):
            for j in  range(nx[0]):
                index = i * nx[0] + j
                gradientDx = None
                if(j == 0):
                    gradientDx = (self.data[i * nx[0] + j + 2] - 4 * self.data[i * nx[0] + j + 1] + 3 * self.data[i * nx[0] + j]) / (-2.0 * dx[0])
                elif(j == nx[0] - 1):
                    gradientDx = (self.data[i * nx[0] + j - 2] - 4 * self.data[i * nx[0] + j - 1] + 3 * self.data[i * nx[0] + j]) / (2.0 * dx[0])
                else:
                    gradientDx = (self.data[i * nx[0] + j + 1] - self.data[i * nx[0] + j - 1]) / (2.0 * dx[0])
                
                gradientField[0].data[index] = copy.deepcopy(gradientDx)

                gradientDz = None
                if(i == 0):
                    gradientDz = (self.data[(i + 2) * nx[0] + j] - 4 * self.data[(i + 1) * nx[0] + j] + 3 * self.data[i * nx[0] + j]) / (-2.0 * dx[1])
                elif(i == nx[1] - 1):
                    gradientDz = (self.data[(i - 2) * nx[0] + j] - 4 * self.data[(i - 1) * nx[0] + j] + 3 * self.data[i * nx[0] + j]) / (2.0 * dx[1])
                else:
                    gradientDz = (self.data[(i + 1) * nx[0] + j] - self.data[(i - 1) * nx[0] + j]) / (2.0 * dx[1])
                gradientField[1].data[index] = copy.deepcopy(gradientDz)

   
    def getRealPart(self):
        res = []
        for i in self.data:
            res.append(i.real)
        return res

    def __truediv__(self, rhs):
        res = dataGrid2D(self.grid)
        if isinstance(rhs,dataGrid2D):
            res.data = np.true_divide(self.data, rhs.data)
        else:
            res.data = np.true_divide(self.data,rhs)
            
        return res
            
    def __mul__(self,rhs):
        res = dataGrid2D(self.grid)
        if isinstance(rhs,dataGrid2D):
            res.data = np.multiply(self.data,rhs.data)
        else:
            res.data = np.multiply(self.data,rhs)
        return res
            
    def __sub__(self,rhs):
        res = dataGrid2D(self.grid)
        if isinstance(rhs,dataGrid2D):
            res.data = np.subtract(self.data,rhs.data)
        else:
            res.data = np.subtract(self.data, rhs)
        return res

    def __add__(self,rhs):
        res = dataGrid2D(self.grid)
        if isinstance(rhs,dataGrid2D):
            res.data = np.add(self.data, rhs.data)
        else:
            if isinstance(rhs,List):
                res.data = np.add(self.data,rhs)
            else:
                res.data = np.add(self.data,rhs)

        return res
