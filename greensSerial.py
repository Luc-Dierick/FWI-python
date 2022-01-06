from grid2D import grid2D
from dataGrid2D import dataGrid2D
import math

class greensRect2DCpu():
    def __init__(self, grid:grid2D, gFunc, source,receiver, k:float) -> None:
        self.grid = grid
        self.G_func = gFunc
        self.source =source
        self.receiver = receiver
        self.k = k
       
        
        self.nx = self.grid.getGridDimensions()
        self.gVol = [complex(128)] * int((2*self.nx[1]-1) * (2*self.nx[0]-1))

        self.createGreensVolume()
        self.createGreensRecv()
        self.createGreensRect2D()

    def createGreensRect2D(self,G,dx,nx,gFunc,k):
        vol = dx[0]*dx[1]
        for i in range(-nx[1] + 1, nx[1]):
            z = i * dx[1]
            for j in range(-nx[0] + 1, nx[0]):
                x = j * dx[0]
                r = math.sqrt(z**2 + x**2)
                G[(nx[1] + i - 1) * 2 * nx[0] + (nx[0] + j - 1)] = gFunc(k, r) * vol


    def createGreensVolume(self):
        vol = self.grid.getCellVolume()
        nx = self.grid.getGridDimensions()
        dx = self.grid.getCellDimensions()

        for i in range(-nx[1] + 1,nx[1]):
            z = i * dx[1]
            for j in range(-nx[0]+1,nx[0]):
                x = j*dx[0]
                r = math.sqrt(z**2 + x**2)
                val = self.G_func(self.k,r)
                self.gVol[(nx[1]+i-1)*(2*nx[0]-1)+(nx[0]+j-1)] = val*vol
                

    def contractWithField(self,x):
        assert(self.grid == x.getGrid())
        nx = self.grid.getDimension()
        outputField = self.contractGreensRect2D(self.gVol,x, nx, 2*nx[0] -1)
        return outputField


    def contractGreensRect(self,G,x,testField,nx,ldG):
        inputFieldData = x.getData()
        outputFieldData = [0.0]* testField.getNumberOfGridPoints()

        for i in range(0,nx[1]):
            for j in range(0,nx[1]):
                outputFieldData[(nx[1] - i - 1) * nx[0] + (nx[0] -j -1)] = 0.0
                for k in range(0,nx[1]):
                    for l in range(0,nx[0]):
                        outputFieldData[(nx[1]-i-1) * (nx[0]-j-1)] += G[(i+k) *ldG + j + l] * inputFieldData[k*nx[0] +l]
        testField = outputFieldData

    
    def setGreensFunction(self, greensFunctionField, func):
        raise NotImplementedError

    
    def createGreensVolumeAnKit(self):
        raise NotImplementedError

    def createGreensRecv(self):
        raise NotImplementedError

    def deleteGreensRecv(self):
        raise NotImplementedError

    def getReceiver(self, iRecv):
        raise NotImplementedError