class Sources():
    def __init__(self, xMin,xMax,count) -> None:
        self.count = count
        self.xSrc = []
        self.xMin = xMin
        self.xMax = xMax
        self.dx = self.calculateDistance(xMin,xMax)
        
        for i in range(count):
            sourceArray = [0.0]*2
            for j in range(2):
                sourceArray[j] = xMin[j] + i * self.dx[j]
            self.xSrc.append(sourceArray)
    
    def calculateDistance(self, xMin,xMax)->list:
        dx = [0.0]*2
        for i in range(2):
            dx[i] = (xMax[i] - xMin[i]) / (self.count -1) 

        return dx

