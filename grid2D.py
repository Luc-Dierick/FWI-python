

class grid2D():

    def __init__(self, x_min:list, x_max:list, nx:list):
        self._xMin = x_min
        self._xMax = x_max 
        self._nx = [int(x) for x in nx]
        self._dx = [None]*2 
        self._dx[0] = (self._xMax[0] - self._xMin[0])/self._nx[0]
        self._dx[1] = (self._xMax[1] - self._xMin[1])/self._nx[1]
        self._nGridPoints = int(self._nx[0]*self._nx[1])
        self._cellVolume = self._dx[0] *self._dx[1]
        
    def __eq__(self,rhs):
        if(self._xMin != rhs._xMin or self._xMax != rhs._xMax or self._nx != rhs._nx or self._dx != rhs._dx):
            return False;
        else:
            return True;
        
    def getGridDimensions(self):
        return self._nx

    def getCellDimensions(self):
        return self._dx

    def getGridStart(self):
        return self._xMin

    def getGridEnd(self):
        return self._xMax

    def getNumberOfGrindPoints(self):
        return self._nGridPoints

    def getCellVolume(self):
        return self._cellVolume

    def getDomainArea(self):
        return (self._xMax[0] - self._xMin[0]) * (self._xMax[1] - self._xMin[1])
