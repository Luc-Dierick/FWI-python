// compile commands:
// g++ -std=c++17 -c -fPIC neumann.cpp -o neumann.o
// g++ -fPIC -shared -o neumann.so neumann.o



#include <cmath>
#include <complex>

class Wrapped{
    public:
        double cyl_neumann(double a, double b){
            return std::cyl_neumann(a, b);
      
        }

        double cyl_bessel_j(double a, double b){
            return std::cyl_bessel_j(a, b);
        }

};



extern "C" {
    // __declspec(dllexport)
    Wrapped* wrapped_new() { return new Wrapped();}
    double Wrapped_cyl_neumann( Wrapped* wrapped, double a, double b){ return wrapped->cyl_neumann(a,b);}
    double Wrapped_cyl_bessel_j( Wrapped* wrapped, double a, double b){ return wrapped->cyl_bessel_j(a,b);}
}
    
// int main(){

// std::cout << "hello world" << std::endl;

// Wrapped* w = new Wrapped();

// std::cout  << w->cyl_neumann(2.53,0.23)  << std::endl;
// }