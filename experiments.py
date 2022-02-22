import json
import numpy
import os
import copy

genericinput = "./experiment/input/GenericInput.json"

f = open(genericinput)

input = json.load(f)

for i in range(2000,10000,1000):

    cur = input
    filename = "10x"+str(i*10)+"_"+str(i*100)+"CPU"
    cur["fileName"] = filename
    cur["ngrid_original"]["z"] = str(i*10)
    cur["ngrid"]["z"] = str(i*10)
    with open(genericinput, "w") as f:
        succes = json.dump(cur, f)
    
    with open("./experiment/input/"+filename+".txt","w") as f:
        for i in range(i*100):
            f.write("2.214532871972316741e-01\n")
        
    os.system('python3 main.py')
    
    dfz
