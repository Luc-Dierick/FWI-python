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

    arguments.dir ="/home/lucdierick/FWI-python/default/"
    
    inputfile = open(arguments.dir+"input/GenericInput.json")


    input_data = json.load(inputfile)

    grid = grid2D([input_data["reservoirTopLeft"]["x"],input_data["reservoirTopLeft"]["z"]], [input_data["reservoirBottomRight"]["x"],input_data["reservoirBottomRight"]["z"]],[input_data["ngrid"]["x"],input_data["ngrid"]["z"]])
    source = Sources([input_data["sourcesTopLeft"]["x"],input_data["sourcesTopLeft"]["z"]], [input_data["sourcesBottomRight"]["x"],input_data["sourcesBottomRight"]["z"]], input_data["nSources"])
    receiver = Receivers([input_data["receiversTopLeft"]["x"],input_data["receiversTopLeft"]["z"]], [input_data["receiversBottomRight"]["x"],input_data["receiversBottomRight"]["z"]], input_data["nReceivers"])
    freq = frequenciesGroup(input_data["Freq"],input_data["c_0"])

    magnitude = source.count * freq.count * receiver.count

    model = FiniteDifferenceForwardModel(grid,source,receiver,freq,None)
    
    #pre_processing
    chi = []
    with open(arguments.dir+"input/"+input_data["fileName"]+".txt","r") as f:
        for line in f:
            chi.append(float(line))
        
    ref = model.calculatePressureField(chi)
    
    with open(arguments.dir+"output/"+input_data["fileName"]+"InvertedChiToPressure.txt","w") as f:
        for i in ref:
            f.write(str(i.real)+","+str(i.imag))
            f.write("\n")
    
    
    referencePressureData = []
    with open(arguments.dir+"output/"+input_data["fileName"]+"InvertedChiToPressure.txt") as f:
        for line in f:
            c = line.split(",")
            referencePressureData.append(complex(float(c[0]),float(c[1])))

    inverse = ConjugateGradientInversion(None,model,input_data)
    input_data["max"] = 10000
    
    import time
    start_time = time.time()
    print("started")
    chi, iter = inverse.reconstruct(referencePressureData, input_data)
    
    total_t = time.time()-start_time
    
    print(f"dot: {model.dot_time} upd: {inverse.updtime} func: {model.dot_time + inverse.updtime}")
    
    with open(arguments.dir+"output/"+input_data["fileName"]+"STATS.txt","w") as f:
        f.write(f"{total_t},{model.dot_time},{inverse.updtime},{iter}")
        
    with open(arguments.dir+"output/"+input_data["fileName"]+"RES.txt","w") as f:
        for i in chi.data:
            f.write(str(i)+"\n")
        

 


def parse_args():
    #configure argument parser
    parser = argparse.ArgumentParser()

    # Input arguments
    parser.add_argument("-b", "--bin", type=str, required=False, default="./bin/",
                        help="Path to bin folder containing the app executables")

    parser.add_argument("-d", "--dir", type=str, required=False, default="./experiment/",
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

