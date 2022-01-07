from ctypes import cdll
from ctypes import c_double
lib = cdll.LoadLibrary('/home/luc/Documents/FWI-python/neumann.so')
 
class Wrapper(object):
    def __init__(self):
        self.obj = lib.wrapped_new()
 
    def cyl_neumann(self, a ,b)->c_double:
        res = c_double(lib.Wrapped_cyl_neumann(self.obj , c_double(a),c_double(b)))
        print(res)
        return res
    
    def cyl_bessel_j(self, a, b)->c_double:
        return c_double(lib.Wrapped_cyl_bessel_j(self.obj, c_double(a), c_double(b)))
      
