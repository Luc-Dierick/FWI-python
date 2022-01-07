from dataGrid2D import dataGrid2D


class RegularisationParameters():
    def __init__(self,grid:dataGrid2D):
        self.deltaSquared = 0.0
        self.errorFunctional = 1.0
        self.gradientChi = [grid,grid]
        self.gradientChiNormSquared = grid
        self.b = grid
        self.bSquared = grid
        self.gradient = grid



    