import argparse
import numpy as np
import json
import time

from FWI_python.grid2D import grid2D
from FWI_python.sources import Sources
from FWI_python.receivers import Receivers
from FWI_python.frequenciesGroup import frequenciesGroup
from FWI_python.finiteDifferenceForwardModel import FiniteDifferenceForwardModel
from FWI_python.conjugateGradientInversion import ConjugateGradientInversion


class Processor():
    def __init__(self,accelerated=False):
        self.accelerated = accelerated
       
    def process(self,dir,d_vector_I_dma,d_matrix_IO_dma,u_vector_I_dma,u_kappa_IO_dma):
               
        inputfile = open(dir+"input/GenericInput.json")
        input_data = json.load(inputfile)
        print(input_data)
        input_data["max"] = 50

        grid = grid2D([input_data["reservoirTopLeft"]["x"],input_data["reservoirTopLeft"]["z"]], [input_data["reservoirBottomRight"]["x"],input_data["reservoirBottomRight"]["z"]], [input_data["ngrid"]["x"],input_data["ngrid"]["z"]])
        source = Sources([input_data["sourcesTopLeft"]["x"],input_data["sourcesTopLeft"]["z"]], [input_data["sourcesBottomRight"]["x"],input_data["sourcesBottomRight"]["z"]], input_data["nSources"])
        receiver = Receivers([input_data["receiversTopLeft"]["x"],input_data["receiversTopLeft"]["z"]], [input_data["receiversBottomRight"]["x"],input_data["receiversBottomRight"]["z"]], input_data["nSources"])
        freq = frequenciesGroup(input_data["Freq"],input_data["c_0"])

        magnitude = source.count * freq.count * receiver.count

        referencePressureData = []

        with open(dir+"output/"+input_data["fileName"]+"InvertedChiToPressure.txt") as f:
            for line in f:
                c = line.split(",")
                referencePressureData.append(complex(float(c[0]),float(c[1])))

        model = FiniteDifferenceForwardModel(grid,source,receiver,freq,None,self.accelerated,d_vector_I_dma,d_matrix_IO_dma,u_vector_I_dma,u_kappa_IO_dma)

        inverse = ConjugateGradientInversion(None,model,input_data)

        start_time = time.time()
        chi_estimate = inverse.reconstruct(referencePressureData, input_data)

        print(f"Dotproduct time ConjugateGradient: {inverse.dot_time}")
        print(f"Dotproduct time FiniteDifference: {model.dot_time}")
        print(f"UpdateGradient time: {inverse.updtime}")
        
        print(f"Total time: {time.time()-start_time}")
 
        with open(dir+"output/chiRes_compare.txt","w") as f:
            for i in chi_estimate.data:
                f.write(str(i)+"\n")
    
    def parse_args(self):
        #configure argument parser
        parser = argparse.ArgumentParser()

        # Input arguments
        parser.add_argument("-b", "--bin", type=str, required=False, default="./bin/",
                            help="Path to bin folder containing the app executables")

        parser.add_argument("-d", "--dir", type=str, required=False, default="./default/",
                            help="Path to the folder containing input/output folders")

        parser.add_argument("--post-dir", type=str, required=False, default="./",
                            help="Path to the folder containing postProcessing-python3.py")

        parser.add_argument("-p", "--preprocess", type=str, required=False, default="FiniteDifference",
                            choices=["FiniteDifference", "Integral","FiniteDifferenceOpenMP", "FiniteDifferenceMPI","FiniteDifferenceDataParallelCpp"],
                            help="Choice of ForwardModel for PreProcess")

        parser.add_argument("-f", "--forward", type=str, required=False, default="FiniteDifference",
                            choices=["FiniteDifference", "Integral","FiniteDifferenceOpenMP", "FiniteDifferenceMPI","FiniteDifferenceDataParallelCpp"],
                            help="Choice of ForwardModel for Process")

        parser.add_argument("-i", "--inversion", type=str, required=False, default="ConjugateGradient",
                            choices=["ConjugateGradient", "GradientDescent", "Evolution", "Random", "StepAndDirection","ConjugateGradientMPI","ConjugateGradientOpenMP","ConjugateGradientDataParallelCpp"],
                            help="Choice of inversion method for Process *StepAndDirection is deprecated*")

        parser.add_argument("--step-dir", type=str, required=False, default="ConjugateGradient",
                            choices=["ConjugateGradient", "GradientDescent"],
                            help="Used only if -i=StepAndDirection. Desired StepDirection")

        parser.add_argument("--step-size", type=str, required=False, default="ConjugateGradient",
                            choices=["ConjugateGradient", "ConjugateGradientRegularization", "BorzilaiBorwein", "Fixed"],
                            help="Used only if -i=StepAndDirection. Desired StepSize")

        #parse the input arguments
        return parser