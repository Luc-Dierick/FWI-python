from ctypes import cdll
from ctypes import c_double
lib = cdll.LoadLibrary('./neumann.so')
 
class Wrapper(object):
    def __init__(self):
        self.obj = lib.wrapped_new()
 
    def cyl_neumann(self, a ,b)->c_double:
        return c_double(lib.Wrapped_cyl_neumann(self.obj , c_double(a),c_double(b)))
    
    def cyl_bessel_j(self, a, b)->c_double:
        return c_double(lib.Wrapped_cyl_bessel_j(self.obj, c_double(a), c_double(b)))
      
