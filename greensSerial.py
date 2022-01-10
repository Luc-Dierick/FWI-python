from grid2D import grid2D
from dataGrid2D import dataGrid2D
import math
import copy

class greensRect2DCpu(dataGrid2D):
    def __init__(self, grid:grid2D, gFunc, source,receiver, k:float) -> None:
        self.grid = grid
        self.G_func = gFunc
        self.source =source
        self.receiver = receiver
        self.k = k
        self.gRecv = []
        
        self.nx = self.grid.getGridDimensions()
        self.gVol = [complex(0)] * ((2 * self.nx[1] - 1) * (2 * self.nx[0] - 1))

        self.createGreensVolume()

        self.createGreensRecv()
        # self.createGreensVolumeAnKit()

        # self.createGreensRect2D()

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
                index = (nx[1]+i-1)*(2*nx[0]-1)+(nx[0]+j-1)
                self.gVol[index] = val*vol
                

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

    
    def createGreensVolumeAnKit(self):
        vol = self.grid.getCellVolume()
        nx1 = self.grid.getGridDimensions()
        dx = self.grid.getCellDimensions()
        x_min = self.grid.getGridStart()
        nx = nx1[0]
        nz = nx1[1]

    def createGreensRecv(self):
        vol = self.grid.getCellVolume()
        for i in range(self.receiver.count):
            x_receiver = self.receiver.xRecv[i][0]
            z_receiver = self.receiver.xRecv[i][1]

            G_bound = dataGrid2D(self.grid)

            nx = self.grid.getGridDimensions()
            dx = self.grid.getCellDimensions()
            x_min = self.grid.getGridStart()

            G_bound = dataGrid2D(self.grid)
            
            for j in range(nx[1]):
                z = x_min[1] + (j+0.5)*dx[1]
                nx_j = nx[0] * j
                for t in range(nx[0]):
                    x = x_min[0]  + (0.5+t)*dx[0]
                    G_bound.data[nx_j + t] = vol * self.G_func(self.k, math.sqrt((x-x_receiver)**2 + (z-z_receiver)**2))

            self.gRecv.append(copy.deepcopy(G_bound))


    def deleteGreensRecv(self):
        self.gRecv = []

    def getReceiverCont(self, iRecv):
        return copy.deepcopy(self.gRecv[iRecv])
