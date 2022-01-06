import math
from dataGrid2D import dataGrid2D
from grid2D import grid2D
from greensSerial import greensRect2DCpu
from wrapper import Wrapper



class FiniteDifferenceForwardModel():
    def __init__(self,grid,source,receiver,freq,fmInput) -> None:
        
        self.wrapper = Wrapper()

        self.grid = grid
        self.source = source
        self.receiver = receiver
        self.freq = freq
        self.fmInput = fmInput

        self.vkappa = []
        self.Greens = []
        self.vpTot = []
        self.residual = []

        self.createKappa(self.freq,self.source,self.receiver)
        self.createGreens()

    def createGreens(self):
        for i in range(self.freq.count):
            self.Greens.append(greensRect2DCpu(self.grid,self.helmholtz2D, self.source,self.receiver,self.freq.k[i]))

  
    def helmholtz2D(self,k,r):
        value_r = 0.0
        value_i = 0.0 
        if r != 0.0:
            value_r = -0.25 * self.wrapper.cyl_neumann(0.0,k*r).value * k *k
            value_i = 0.25 * self.wrapper.cyl_bessel_j(0.0,k*r).value * k * k
        c = complex(value_r,value_i)
        return c
        
  
    def calcTotalField(self, G, chiEst, Pinit):
        pass

    def applyKappa(self, CurrentPressureFieldSerial, pData):
        pass

    def createKappa(self,freq,source, receiver):
        for i in range(freq.count*source.count*receiver.count):
            self.vkappa.append(dataGrid2D(self.grid))

    def createPTot(self,freq,source):
        for i in range(freq.count):
            for j in range(source.count):
                self.vpTot.append(dataGrid2D(self.Greens.getReceivercont(j) / (self.freq.k[i] * self.freq.k[j] *self.grid.getCellVolume())))


    def calculateKappa(self):
        pass

    def calculatePTot(self, chiEst):
        pass

    def getResidualGradient(res, kRes):
        pass

    def getGrid(self):
        return self.grid

    def getSource(self):
        return self.source

    def getReceiver(self):
        return self.receiver
    
    def getFreq(self):
        return self.freq



