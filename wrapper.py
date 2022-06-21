from ctypes import cdll
from ctypes import c_double
pynq = '/home/xilinx/jupyter_notebooks/FWI_python/neuman.so' #32 bit compiled.
wsl  = '/home/lucdierick/FWI-python/neumann.so' #64 bit compiled
linux = "/home/luc/Documents/FWI-python/neumann.so" #64 bit compiled
import os

lib = cdll.LoadLibrary(os.getcwd()+"/FWI/neumann_alveo.so")
 
class Wrapper(object):
    def __init__(self):
        lib.Wrapped_cyl_neumann.restype = c_double
        lib.Wrapped_cyl_bessel_j.restype = c_double
        self.obj = lib.wrapped_new()
 
    def cyl_neumann(self, a ,b):
        return lib.Wrapped_cyl_neumann(self.obj , c_double(a),c_double(b))
    
    def cyl_bessel_j(self, a, b):
        return lib.Wrapped_cyl_bessel_j(self.obj, c_double(a), c_double(b))
