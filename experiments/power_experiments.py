import numpy as np
import matplotlib.pyplot as plt
import json
import copy

l = [10, 100, 500]

num = ""

total_time = []
gridpoints = []

estimated_100 = [2.002, 2.002, 2.002]
estimated_20 = [1.857, 1.857, 1.857]

total_power = []
total_object = []
total_ambient = []
idle_power = []
idle_ambient = []
idle_object = []
memory = []

total_power_20 = []
total_object_20 = []
total_ambient_20 = []
idle_power_20 = []
idle_ambient_20 = []
idle_object_20 = []
memory_20 = []

for i in l:
    data = np.loadtxt(f"D:/Dask/FWI-python/experiments/300_100_{i*10}.txt")
    data_t = data.T #get transpose
    memory.append(np.mean(data_t[4]))

    data_host = np.loadtxt(f"D:/Dask/FWI-python/experiments/300_100_{i*10}_host.txt")
    data_host_t = data_host.T
    total_power.append(np.mean(data_host_t[0]))
    total_object.append(np.mean(data_host_t[1]))
    total_ambient.append(np.mean(data_host_t[2]))
    idle_power.append(np.mean(data_host_t[3]))
    idle_object.append(np.mean(data_host_t[4]))
    idle_ambient.append(np.mean(data_host_t[5]))


    ################### 20 #######################

    data_20 = np.loadtxt(f"D:/Dask/FWI-python/experiments/300_20_{i*10}.txt")
    data_t_20 = data_20.T #get transpose
    memory_20.append(np.mean(data_t_20[4]))

    data_host_20 = np.loadtxt(f"D:/Dask/FWI-python/experiments/300_20_{i*10}_host.txt")
    data_host_t_20 = data_host_20.T
    total_power_20.append(np.mean(data_host_t_20[0]))
    total_object_20.append(np.mean(data_host_t_20[1]))
    total_ambient_20.append(np.mean(data_host_t_20[2]))
    idle_power_20.append(np.mean(data_host_t_20[3]))
    idle_object_20.append(np.mean(data_host_t_20[4]))
    idle_ambient_20.append(np.mean(data_host_t_20[5]))

print(f"average memory: {memory}")
print(f"average memory: {memory_20}")

labels = ["High utilization", "Low utilization", "Estimated power High", "Estimated power low"]
plt.title("Total power over gridpoints")
plt.xlabel("Gridpoints")
plt.ylabel("Power in Watt")

plt.plot([x*10 for x in l],total_power,"-bo")
plt.plot([x*10 for x in l],total_power_20,"-ro")
plt.plot([x*10 for x in l],estimated_100,"-y")
plt.plot([x*10 for x in l],estimated_20,"-g")
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
