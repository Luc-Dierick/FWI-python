from grid2D import grid2D
from sources import Sources
from receivers import Receivers
from frequenciesGroup import frequenciesGroup
from finiteDifferenceForwardModel import FiniteDifferenceForwardModel
from conjugateGradientInversion import ConjugateGradientInversion
import argparse

import json

parser = argparse.ArgumentParser()

# Input arguments
parser.add_argument("-data", type=list")


dir = "/home/xilinx/jupyter_notebooks/PYNQ-FWI/FWI_python/default/"

inputfile = open(dir + "input/GenericInput.json")

input_data = json.load(inputfile)

grid = grid2D([input_data["reservoirTopLeft"]["x"], input_data["reservoirTopLeft"]["z"]],
              [input_data["reservoirBottomRight"]["x"], input_data["reservoirBottomRight"]["z"]],
              [input_data["ngrid"]["x"], input_data["ngrid"]["z"]])
source = Sources([input_data["sourcesTopLeft"]["x"], input_data["sourcesTopLeft"]["z"]],
                 [input_data["sourcesBottomRight"]["x"], input_data["sourcesBottomRight"]["z"]],
                 input_data["nSources"])
receiver = Receivers([input_data["receiversTopLeft"]["x"], input_data["receiversTopLeft"]["z"]],
                     [input_data["receiversBottomRight"]["x"], input_data["receiversBottomRight"]["z"]],
                     input_data["nSources"])
freq = frequenciesGroup(input_data["Freq"], input_data["c_0"])

magnitude = source.count * freq.count * receiver.count

model = FiniteDifferenceForwardModel(grid, source, receiver, freq, None,False)

referencePressureData = arguments.data

inverse = ConjugateGradientInversion(None, model, input_data)
input_data["max"] = 50

import time
start_time = time.time()
chi = inverse.reconstruct(referencePressureData, input_data)

total_time = time.time() - start_time


res = {
    "chi": chi.data,
    "time": total_time
}

out = open("output.txt","w")
json.dump(res,out)  
