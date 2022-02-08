import argparse
import numpy as np
import json


from .grid2D import grid2D
from .sources import Sources
from .receivers import Receivers
from .frequenciesGroup import frequenciesGroup
from .finiteDifferenceForwardModel import FiniteDifferenceForwardModel
from .conjugateGradientInversion import ConjugateGradientInversion

class Pre_processor():
    def __init__(self):
        self.dir = "/home/xilinx/jupyter_notebooks/PYNQ-FWI/FWI_python/arm/"
    
    def process(self,accelerated=False):
        print("Inverting observed data into modelled data...")

        self.pre_process()
        self.dir = "/home/xilinx/jupyter_notebooks/PYNQ-FWI/FWI_python/accelerated/"
        self.pre_process()
        
        print("Succesfully inverted Observed data into Modelled data!")
        
    def pre_process(self):
        inputfile = open(self.dir+"input/GenericInput.json")

        input_data = json.load(inputfile)

        grid = grid2D([input_data["reservoirTopLeft"]["x"],input_data["reservoirTopLeft"]["z"]], [input_data["reservoirBottomRight"]["x"],input_data["reservoirBottomRight"]["z"]],[input_data["ngrid"]["x"],input_data["ngrid"]["z"]])
        source = Sources([input_data["sourcesTopLeft"]["x"],input_data["sourcesTopLeft"]["z"]], [input_data["sourcesBottomRight"]["x"],input_data["sourcesBottomRight"]["z"]], input_data["nSources"])
        receiver = Receivers([input_data["receiversTopLeft"]["x"],input_data["receiversTopLeft"]["z"]], [input_data["receiversBottomRight"]["x"],input_data["receiversBottomRight"]["z"]], input_data["nSources"])
        freq = frequenciesGroup(input_data["Freq"],input_data["c_0"])

        magnitude = source.count * freq.count * receiver.count

        model = FiniteDifferenceForwardModel(grid,source,receiver,freq,None,accelerated=False,gridsize=100,resolution=300)

        #pre_processing
        chi = []
        with open(self.dir+"input/10x10_100CPU.txt","r") as f:
            for line in f:
                chi.append(float(line))

        ref = model.calculatePressureField(chi)

        with open(self.dir+"output/10x10_100CPUInvertedChiToPressure.txt","w") as f:
            for i in ref:
                f.write(str(i.real)+","+str(i.imag))
                f.write("\n")
                
        with open(self.dir+"output/chi_ref_10x10_100CPU.txt","w")as f:
            for i in chi:
                f.write(str(i)+"\n")
        
