import numpy as np
import matplotlib.pyplot as plt
import json
import copy

l = [10, 100, 500]

win = "D:/Dask/FWI-python"
win = "."
num = ""

total_time = []
gridpoints = []

estimated_100 = [2.002, 2.002, 2.002]
estimated_20 = [1.857, 1.857, 1.857]

total_power = []
total_energy = [] #This is the execution time * power
execution_time = []
total_object = []
total_ambient = []
idle_power = []
idle_ambient = []
idle_object = []
memory = []

execution_timeGPU = [0.18665,3.87273/10,19.0606/50]
execution_timePY = [0.45947837829589844,3.07403302192688/10, 11.48944640159607/50]
gpu_power = []
gpu_idle_power = []

total_power_20 = []
total_energy_20 = [] #This is the execution time * power
execution_time_20 = []
total_object_20 = []
total_ambient_20 = []
idle_power_20 = []
idle_ambient_20 = []
idle_object_20 = []
memory_20 = []


gpu = []
with open(f"{win}/experiments/output_1000_303025.log", "r") as f:
    next(f)
    for line in f:
        gpu.append(float(line[:-2]))
np_gpu = np.array(gpu)
max = np.max(np_gpu)
min = np.min(np_gpu)
print(f"3030 max: {max} min: {min}")

gpu = []
with open(f"{win}/experiments/output_1000_505025.log", "r") as f:
    next(f)
    for line in f:
        gpu.append(float(line[:-2]))
np_gpu = np.array(gpu)
max = np.max(np_gpu)
min = np.min(np_gpu)
print(f"5050 max: {max} min: {min}")

with open(f"{win}/experiments/output_20000.log", "r") as f:
    next(f)
    for line in f:
        gpu.append(float(line[:-2]))
np_gpu = np.array(gpu)
max = np.max(np_gpu)
min = np.min(np_gpu)
print(f"2k max: {max} min: {min}")

for i in l:

    gpu = []
    with open(f"{win}/experiments/output_{i*10}.log","r") as f:
        next(f)
        for line in f:
            gpu.append(float(line[:-2]))
    np_gpu =  np.array(gpu)
    max = np.max(np_gpu)
    min = np.min(np_gpu)
    gpu_power.append(np.mean(np_gpu[np_gpu>=(max-1.5)]))
    gpu_idle_power.append(np.mean(np_gpu[np_gpu<=(min+1.5)]))
    data = np.loadtxt(f"{win}/experiments/300_100_{i*10}.txt")
    data_t = data.T #get transpose
    memory.append(np.mean(data_t[4]))
    execution_time.append(np.mean(data_t[0])/(i/10))



    data_host = np.loadtxt(f"{win}/experiments/300_100_{i*10}_host.txt")
    data_host_t = data_host.T
    total_power.append(np.mean(data_host_t[0]))
    total_object.append(np.mean(data_host_t[1]))
    total_ambient.append(np.mean(data_host_t[2]))
    idle_power.append(np.mean(data_host_t[3]))
    idle_object.append(np.mean(data_host_t[4]))
    idle_ambient.append(np.mean(data_host_t[5]))
    total_energy.append(execution_time[-1] * total_power[-1])


    ################### 20 #######################

    data_20 = np.loadtxt(f"{win}/experiments/300_20_{i*10}.txt")
    data_t_20 = data_20.T #get transpose
    memory_20.append(np.mean(data_t_20[4]))
    execution_time_20.append(np.mean(data_t_20[0])/(i/10))

    data_host_20 = np.loadtxt(f"{win}/experiments/300_20_{i*10}_host.txt")
    data_host_t_20 = data_host_20.T
    total_power_20.append(np.mean(data_host_t_20[0]))
    total_object_20.append(np.mean(data_host_t_20[1]))
    total_ambient_20.append(np.mean(data_host_t_20[2]))
    idle_power_20.append(np.mean(data_host_t_20[3]))
    idle_object_20.append(np.mean(data_host_t_20[4]))
    idle_ambient_20.append(np.mean(data_host_t_20[5]))
    total_energy_20.append(execution_time_20[-1] * total_power_20[-1])


# print(f"average memory: {memory}")
# print(f"average memory: {memory_20}")
# print(gpu_power)
print(execution_time_20)
print(execution_time)

labels = ["Z1 High utilization", "Z1 Low utilization", "Z1 Est. High Utilization", "Z1 Est. Low Utilization","Quadro T1000 "]
plt.title("Total Energy over gridpoints")
plt.xlabel("Gridpoints")
plt.ylabel("Energy in (Joules/100Gridpoints)")

plt.plot([x*10 for x in l],total_energy,"-bo")
plt.plot([x*10 for x in l],total_energy_20,"-ro")
plt.plot([x*10 for x in l],np.multiply(estimated_100,execution_time),"-y")
plt.plot([x*10 for x in l],np.multiply(estimated_20,execution_time_20),"-g")
plt.plot([x*10 for x in l],np.multiply(gpu_power,execution_timeGPU),"-o")
plt.legend(labels)
plt.show()

plt.clf()

plt.title("Execution times over gridpoints")
plt.xlabel("Gridpoints")
plt.ylabel("Execution time (s)")

plt.plot([x*10 for x in l],execution_time,"-bo")
plt.plot([x*10 for x in l],execution_time_20,"-ro")
plt.plot([x*10 for x in l],execution_timeGPU,"-yo")
plt.legend(["Z1 High Utilization","Z1 Low Utilization","Quadro P1000"])
plt.show()

plt.clf()

plt.title("Total Power over gridpoints")
plt.xlabel("Gridpoints")
plt.ylabel("Power in Watt")

plt.plot([x*10 for x in l],total_power,"-bo")
plt.plot([x*10 for x in l],total_power_20,"-ro")
plt.plot([x*10 for x in l],estimated_100,"-y")
plt.plot([x*10 for x in l],estimated_20,"-g")
plt.plot([x*10 for x in l],gpu_power,"-o")
plt.legend(labels)
plt.show()

plt.clf()


plt.ylabel("Temperature in Celsius")
plt.xlabel("Gridpoints")
plt.title("Ambient temperature over gridpoints")
plt.plot([x*10 for x in l],total_ambient,"-bo")
plt.plot([x*10 for x in l],total_ambient_20,"-ro")
plt.legend(labels)
plt.show()
plt.clf()

plt.legend(labels)
plt.ylabel("Temperature in Celsius")
plt.xlabel("Gridpoints")
plt.title("Object temperature over gridpoints")
plt.plot([x*10 for x in l],total_object,"-bo")
plt.plot([x*10 for x in l],total_object_20,"-ro")
plt.legend(labels)
plt.show()
plt.clf()

plt.legend(labels)
plt.ylabel("Power in Watt")
plt.xlabel("Gridpoints")
plt.title("Idle total power over gridpoints")
plt.plot([x*10 for x in l],idle_power,"-bo")
plt.plot([x*10 for x in l],idle_power_20,"-ro")
plt.plot([x*10 for x in l],estimated_100,"-y")
plt.plot([x*10 for x in l],estimated_20,"-g")
plt.plot([x*10 for x in l],gpu_idle_power,"-o")
plt.legend(labels)
plt.show()
plt.clf()

plt.legend(labels)
plt.ylabel("Temperature in Celsius")
plt.xlabel("Gridpoints")
plt.title("Idle Object temperature over gridpoints")
plt.plot([x*10 for x in l],idle_object,"-bo")
plt.plot([x*10 for x in l],idle_object_20,"-ro")
plt.legend(labels)
plt.show()
plt.clf()

plt.legend(labels)
plt.ylabel("Temperature in Celsius")
plt.xlabel("Gridpoints")
plt.title("Idle Ambient temperature over gridpoints")
plt.plot([x*10 for x in l],idle_ambient,"-bo")
plt.plot([x*10 for x in l],idle_ambient_20,"-ro")
plt.legend(labels)
plt.show()
plt.clf()

plt.legend(labels)
plt.ylabel("Memory in MegaBytes")
plt.xlabel("Gridpoints")
plt.title("Memory over gridpoints")
plt.plot([x*10 for x in l],memory,"-bo")
plt.plot([x*10 for x in l],memory_20,"-ro")
plt.legend(labels)
plt.show()



#
# def plot_time():
#     # plt.yticks([0,50,100,150,200,250],labels=["0","50","100","150","200","250"])
#     #
#     # plt.plot(np.linspace(0,10000,len(total_time[0])), total_time[0], "-bo")
#     # plt.yticks([0,50,100,150,200,250],labels=["0","50","100","150","200","250"])
#     # plt.plot(np.linspace(0,10000,len(total_time[1])), total_time[1], "-ro")
#     # plt.yticks([0,50,100,150,200,250],labels=["0","50","100","150","200","250"])
#     #
#     # plt.plot(np.linspace(0,10000,len(total_time[2])), total_time[2], "-yo")
#     # plt.yticks([0,50,100,150,200,250],labels=["0","50","100","150","200","250"])
#     #
#     # plt.plot(np.linspace(0,10000,len(total_time[3])), total_time[3], "-go")
#     # plt.yticks([0,50,100,150,200,250],labels=["0","50","100","150","200","250"])
#
#     plt.title("4 versions of FWI")
#     plt.xlabel("Gridpoints")
#     plt.ylabel("Time (s)")
#     plt.yticks([0,50,100,150,200,250],labels=["0","50","100","150","200","250"])
#
#     plt.plot(gridpoints[0],total_time[0],"-o")
#     plt.yticks([0,50,100,150,200,250],labels=["0","50","100","150","200","250"])
#     plt.plot(gridpoints[1], total_time[1],"-o")
#     plt.yticks([0,50,100,150,200,250],labels=["0","50","100","150","200","250"])
#     plt.plot(gridpoints[2], total_time[2],"-o")
#     plt.yticks([0,50,100,150,200,250],labels=["0","50","100","150","200","250"])
#     plt.plot(gridpoints[3], total_time[3],"-o",)
#
#     plt.yticks([0, 50, 100, 150, 200, 250], labels=["0", "50", "100", "150", "200", "250"])
#     plt.plot(cppgrid[:-2], cpptime[:-2], "-o", )
#
#     plt.yticks([0,50,100,150,200,250],labels=["0","50","100","150","200","250"])
#     plt.plot(gridpoints[3], mock, "-o",linestyle="dashed")
#
#     plt.yticks([0, 50, 100, 150, 200, 250], labels=["0", "50", "100", "150", "200", "250"])
#     plt.legend(["1 node", "2 nodes","4 nodes", "CPU Python","CPU C++","30 nodes"])
#     # plt.legend(["CPU"])
#     plt.show()
#
# def plot_iterations():
#     plt.plot(gridpoints[3], total_time[3],"-o")
#     plt.plot(gridpoints[3], iterations[0],"-o")
#     plt.xlabel("Gridpoints")
#     plt.ylabel("Time (s) and no. Iterations")
#     plt.title("CPU time vs iterations")
#     plt.legend(["CPU time","iterations"])
#     plt.show()
#
#
# def plot_precision():
#     plt.plot(gridpoints[0],precision[0],"-o")
#     plt.plot(gridpoints[1],precision[1],"-o")
#     plt.plot(gridpoints[2],precision[2],"-o")
#     plt.plot(gridpoints[3],precision[3],"-o")
#     plt.legend(["1 node", "2 nodes","4 nodes", "CPU"])
#     plt.title("Precision of the results")
#     plt.xlabel("Difference between result and reference")
#     plt.show()
#
# def plot_func():
#     plt.plot(gridpoints[2],func_time[2],"-o")
#     plt.plot(gridpoints[2], total_time[2], "-o")
#     plt.legend(["HW function time", "total time"])
#     plt.title("Time spent in HW functions vs total time (Node)")
#     plt.xlabel("Gridpoints")
#     plt.ylabel("Time (s)")
#     plt.show()
#
#     plt.plot(gridpoints[3], func_time[3], "-o")
#     plt.plot(gridpoints[3], total_time[3], "-o")
#     plt.legend(["HW function time", "total time"])
#     plt.title("Time spent in HW functions vs total time (CPU)")
#     plt.xlabel("Gridpoints")
#     plt.ylabel("Time (s)")
#     plt.show()
#
