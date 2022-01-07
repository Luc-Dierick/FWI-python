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
        self.magnitude = self.source.count * self.freq.count * self.receiver.count

        self.vkappa = []
        self.Greens = []
        self.vpTot = []
        self.residual = []

        self.createKappa(self.freq,self.source,self.receiver)
        self.createGreens()
        
        self.createPTot(freq,source)
        self.calculateKappa()


    def getKernel(self):
        return self.vkappa

    def createGreens(self):
        for i in range(self.freq.count):

            rect = greensRect2DCpu(self.grid,self.helmholtz2D, self.source,self.receiver,self.freq.k[i])
            self.Greens.append(rect)


    def helmholtz2D(self,k,r):
        value_r = 0.0
        value_i = 0.0 
        if r != 0.0:
            print(self.wrapper.cyl_neumann(0.0,k*550.626793).value * k * k )
            
            value_r = -0.25 * self.wrapper.cyl_neumann(0.0,k*r).value * k *k
            value_i = 0.25 * self.wrapper.cyl_bessel_j(0.0,k*r).value * k * k
        c = complex(value_r,value_i)
        return c
        
  
    def calcTotalField(self, G, chiEst, Pinit):
        raise NotImplementedError

   

    def createKappa(self,freq,source, receiver):
        for i in range(freq.count*source.count*receiver.count):
            self.vkappa.append(dataGrid2D(self.grid))

    def createPTot(self,freq,source):
        for i in range(freq.count):
            for j in range(source.count):
                vp = self.Greens[i].getReceiverCont(j)
                self.vpTot.append(vp)
       
    def calculateKappa(self):
        for i in range(self.freq.count):
            li = i * self.receiver.count * self.source.count
            for j in range(self.receiver.count):
                lj = j * self.source.count
                for k in range(self.source.count):
                    d =  self.Greens[i].getReceiverCont(j) 
                    v = self.vpTot[i * self.source.count + k]
                    self.vkappa[li+lj+k] = d*v

    def calculatePressureField(self, chiEst):
        #second function
        return self.applyKappa(chiEst)
        
    def applyKappa(self, CurrentPressureFieldSerial):
        kOperator = []
        for i in range(self.magnitude):
            kOperator.append(self.dotProduct(self.vkappa[i],CurrentPressureFieldSerial))
        return kOperator

    def calculatePTot(self, chiEst):
        raise NotImplementedError

    def getResidualGradient(res, kRes):
        raise NotImplementedError

    def getGrid(self):
        return self.grid

    def getSource(self):
        return self.source

    def getReceiver(self):
        return self.receiver
    
    def getFreq(self):
        return self.freq


    def dotProduct(self, lhs, rhs):
        sum = 0
        if isinstance(rhs,dataGrid2D):
            rhsData = rhs.getData()
        else:
            rhsData = rhs
        for i in range(lhs.grid.getNumberOfGridPoints()):

            sum += lhs.data[i] * rhsData[i]

        return sum