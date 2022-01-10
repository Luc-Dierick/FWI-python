from ctypes import cdll
from ctypes import c_double
lib = cdll.LoadLibrary('/home/luc/Documents/FWI-python/neumann.so')
 
class Wrapper(object):
    def __init__(self):
        lib.Wrapped_cyl_neumann.restype = c_double
        lib.Wrapped_cyl_bessel_j.restype = c_double
        self.obj = lib.wrapped_new()
 
    def cyl_neumann(self, a ,b):
        return lib.Wrapped_cyl_neumann(self.obj , c_double(a),c_double(b))
    
    def cyl_bessel_j(self, a, b):
        return lib.Wrapped_cyl_bessel_j(self.obj, c_double(a), c_double(b))
      
