import argparse
import numpy as np
import json


from grid2D import grid2D
from sources import Sources
from receivers import Receivers
from frequenciesGroup import frequenciesGroup
from finiteDifferenceForwardModel import FiniteDifferenceForwardModel
from conjugateGradientInversion import ConjugateGradientInversion

def main():

    arguments = parse_args()
    
    print(arguments)
   
    referencePressureData = []

    with open(arguments.dir+"output/"+input_data["fileName"]+"InvertedChiToPressure.txt") as f:
        for line in f:
            c = line.split(",")
            referencePressureData.append(complex(float(c[0]),float(c[1])))

    inverse = ConjugateGradientInversion(None,model,input_data)
    
    input_data["max"] = 50

    chi = inverse.reconstruct(referencePressureData, input_data)
    
    with open(arguments.dir+"output/chi_result.txt","w") as f:
        for i in chi.data:
            f.write(str(i)+"\n")

def parse_args():
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
    return parser.parse_args()




if __name__ == '__main__':
    main()

