import math

class frequenciesGroup():

    def __init__(self,freqStruct, c_0) -> None:
        self.count = freqStruct["nTotal"]
        self.c_0 = c_0
        self.dFreq = (freqStruct["max"]-freqStruct["min"]) / (max(int(freqStruct["nTotal"]),2)-1)
        self.freq = []
        self.k = []
        for i in range(int(freqStruct["nTotal"])):
            self.freq.append(freqStruct["min"] + i * self.dFreq)
            self.k.append(2.0*math.pi*self.freq[i]/self.c_0)