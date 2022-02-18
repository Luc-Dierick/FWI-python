class Receivers():
    def __init__(self, xMin,xMax,count) -> None:
        self.count = count
        self.xRecv = []
        self.xMin = xMin
        self.xMax = xMax
        self.dx = self.calculateDistance(xMin,xMax)
        
        for i in range(count):
            receiverArray = [0.0]*2
            for j in range(2):
                receiverArray[j] = xMin[j] + i * self.dx[j]
            self.xRecv.append(receiverArray)
    
    def calculateDistance(self, xMin,xMax)->list:
        dx = [0.0]*2
        for i in range(2):
            dx[i] = (xMax[i] - xMin[i]) / (self.count -1) 

        return dx

