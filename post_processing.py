import csv
import argparse
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from skimage.transform import resize

class Post_processor():
    def __init__(self):
        self.output =  "/home/xilinx/jupyter_notebooks/PYNQ-FWI/FWI_python/accelerated"
        self.run_number = 0
        
    def readRunName(self, path):
        parameter_file = open(path + "/output/lastRunName.txt", "r")
        return parameter_file.readline()

    def readParameter(self, label, path):
        run_name = self.readRunName(path)
        parameter_file = open(path + "/output/" + run_name + ".pythonIn", "r")
        line = [x for x in parameter_file if label in x ][0]
        return line.split()[-1]

    def filename(self, path, prefix = "", suffix = ".txt"):
        runName = self.readRunName(path)
        filename = path + "/output/" + prefix + runName + suffix
        return filename


    def process(self):
        # Enter here the name of the case folder you want to post process
        self.outputPath = self.output
        self.run_number = self.run_number 

        print("Started post processing")

        # Read run parameters from files
        nxt = int(self.readParameter(label="nxt", path = self.outputPath))
        nzt = int(self.readParameter(label="nzt", path = self.outputPath))

        nxt_original = int(self.readParameter(label="nxt_original", path = self.outputPath))
        nzt_original = int(self.readParameter(label="nzt_original", path = self.outputPath))

        # Start image set up for original image
        self.chi1 = np.genfromtxt(self.filename(path = self.outputPath, prefix = "chi_ref_"))
        self.chi1 = self.chi1.reshape((nzt_original, nxt_original))

        # Start image set up for reconstructed image
        self.chi2 = np.genfromtxt(self.filename(path = self.outputPath, prefix = "chi_est_"))
        self.chi2 = self.chi2.reshape((nzt, nxt))

        # We upscale the smaller image to avoid information loss
        self.chi1_original = self.chi1
        self.chi2_original = self.chi2
        if nxt_original > nxt:
            self.chi2 = resize(self.chi2, (nzt_original, nxt_original), mode='reflect')
            nxt = nxt_original
            nzt = nzt_original
        elif (nxt > nxt_original):
            self.chi1 = resize(self.chi1, (nzt, nxt), mode='reflect')
            nxt_original = nxt
            nzt_original = nzt

        # We compute the error per pixel, the square mean of the original image and the mse
        diff_chi = self.chi2-self.chi1
        mse = (np.square(diff_chi)).mean()
        square_mean_original = (np.square(self.chi1)).mean()
        avg_relative_error = np.sqrt(mse)/np.sqrt(square_mean_original)*100
        total_seconds = self.readParameter("time", path = self.outputPath)

#         print("The MSE (mean square error) is:       " + str(mse), flush = True)
#         print("The average relative error is:        " + str(avg_relative_error), flush = True)
#         print("Execution time in seconds:            " + total_seconds, flush = True)

        # Set the minimum and maximum values to chi
        self.v_min = self.chi1.min()
        self.v_max = self.chi1.max()
        
        return self.chi1_original, self.chi2_original, self.v_min, self.v_max, diff_chi
       
    def plot_original(self):
        #####################################
        #### Create plots of dummy image ####
        #####################################

        plt.clf()
        plt.plot()
        plt.title("Chi values in original reservoir")
        plt.imshow(self.chi1_original, interpolation='nearest', vmin=self.v_min, vmax=self.v_max)
        plt.colorbar()
        plt.show()
        
#         plt.savefig(self.filename(path = self.outputPath, suffix = "DummyImage.png"), dpi=400, bbox_inches='tight')
            
    def plot_reconstructed(self):
        #############################################
        #### Create plots of reconstructed image ####
        #############################################

        plt.clf()
        plt.plot()
        plt.title("Chi values in reconstructed reservoir")
        plt.imshow(self.chi2_original, interpolation='nearest', vmin=self.v_min, vmax=self.v_max)
        plt.colorbar()
        plt.show()
        
#         plt.savefig(self.filename(path = self.outputPath, suffix = "Result.png"), dpi=400, bbox_inches='tight')

#############################################################
####  Create plots of offset between dummy and real data ####
#############################################################

# plt.clf()
# plt.plot()
# plt.title("difference between chi values")
# plt.imshow(np.abs(diff_chi), interpolation='nearest')
# plt.colorbar()

# plt.savefig(filename(path = outputPath, suffix = "ChiDifference.png"), dpi=400, bbox_inches='tight')

#######################################
####  Create plot of the residuals ####
#######################################
# reader_residual = csv.reader(open(filename(path=outputPath, suffix = "Residual.log")), delimiter=',')
# dummy_variable_reader_pr = list(reader_residual)
# reader_residual_array = np.array(dummy_variable_reader_pr).astype("float")

# plt.clf()
# residuals = []
# [residuals.append(val[0]) for val in reader_residual_array]
# residuals.insert(0, None)

# plt.plot(residuals)
# plt.ylabel("Residual")
# plt.grid(True)
# plt.savefig(filename(path = outputPath, suffix="Residual.png"), dpi=400)

# print("The pictures have been generated with Python", flush = True)