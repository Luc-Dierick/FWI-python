import math
from FWI.dataGrid2D import dataGrid2D
from FWI.grid2D import grid2D
from FWI.greensSerial import greensRect2DCpu
from FWI.wrapper import Wrapper
import copy
from pynq import allocate
import numpy as np
import time


class FiniteDifferenceForwardModel():
    def __init__(self,grid,source,receiver,freq,fmInput,accelerated,gridsize=200, resolution=250,dotprod=None,update=None,A=None,B=None,C=None) -> None:
        
        self.wrapper = Wrapper()

        self.grid = grid
        self.source = source
        self.receiver = receiver
        self.freq = freq
        self.fmInput = fmInput
        self.magnitude = self.source.count * self.freq.count * self.receiver.count
        self.gridsize = gridsize
        self.resolution = resolution
        if self.magnitude < self.resolution:
            self.magnitude = self.resolution
        self.vkappa = []
        self.Greens = []
        self.vpTot = []
        self.residual = []
        
        self.createGreens()
        self.createKappa(self.freq,self.source,self.receiver)
        self.createPTot(freq,source)
        self.calculateKappa()
        
        self.accelerated = accelerated
        if self.accelerated:
            #set up DMAs
            self.dotprod = dotprod
            self.update = update
                      
            #set up buffers
            self.kappa_buffer_PL = A
            self.CurrentPressureFieldSerial_buffer_PL = B
            self.kOperator_buffer_PL = C
            self.kappa_buffer_PL[:] = np.array([np.array(x.data) for x in self.vkappa])[:]

       
        self.dot_time = 0


    def getKernel(self):
        return copy.deepcopy(self.vkappa)

    def createGreens(self):
        for i in range(self.freq.count):

            rect = greensRect2DCpu(self.grid,self.helmholtz2D, self.source,self.receiver,self.freq.k[i])
            self.Greens.append(rect)


    def helmholtz2D(self,k,r):
        value_r = 0.0
        value_i = 0.0 
        if r != 0.0:          
            value_r = -0.25 * self.wrapper.cyl_neumann(0.0, k*r) * k * k
            value_i = 0.25 * self.wrapper.cyl_bessel_j(0.0, k*r) * k * k
        c = complex(value_r,value_i)
        return c

    def calcTotalField(self, G, chiEst, Pinit):
        raise NotImplementedError

    def createKappa(self,freq,source, receiver):
        for i in range(self.magnitude):
            self.vkappa.append(dataGrid2D(self.grid))

    def createPTot(self,freq,source):
        for i in range(freq.count):
            for j in range(source.count):
                vp = self.Greens[i].getReceiverCont(j) / (self.freq.k[i]**2 * self.grid.getCellVolume())
                self.vpTot.append(vp)
       
    def calculateKappa(self):
        for i in range(self.freq.count):

            li = i * self.receiver.count * self.source.count

            for j in range(self.receiver.count):

                lj = j * self.source.count

                for k in range(self.source.count):
                    
                    d = self.Greens[i].getReceiverCont(j)
                    v = self.vpTot[i * self.source.count + k]

                    self.vkappa[li+lj+k] = copy.deepcopy(d*v)
  


    def calculatePressureField(self, chiEst):
        #second function
        return self.applyKappa(chiEst)

        
    def applyKappa(self, CurrentPressureFieldSerial):
        start_time = time.time()
        kOperator = []
        cur = CurrentPressureFieldSerial
        if isinstance(CurrentPressureFieldSerial,dataGrid2D):
            cur = CurrentPressureFieldSerial.data   
            
        if self.accelerated:
            self.CurrentPressureFieldSerial_buffer_PL[:] = cur[:]
            self.dotProduct_HW(self.kappa_buffer_PL, self.CurrentPressureFieldSerial_buffer_PL, self.kOperator_buffer_PL)
            kOperator[:] = self.kOperator_buffer_PL[:]
        else:
            for i in range(self.magnitude):
                kOperator.append(np.dot(self.vkappa[i].data,cur))

        self.dot_time += time.time()-start_time

        return kOperator

    def dotProduct_HW(self,matrix_in, vector_in, out):
        
        matrix_in.sync_to_device()
        vector_in.sync_to_device()
        self.dotprod.call(matrix_in,vector_in,out)
        out.sync_from_device()       
    
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

