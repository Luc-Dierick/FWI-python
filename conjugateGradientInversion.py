
from finiteDifferenceForwardModel import FiniteDifferenceForwardModel
from regularization import RegularisationParameters
from dataGrid2D import dataGrid2D
import numpy as np

class ConjugateGradientInversion():
    
    def __init__(self, costCalculator, forwardModel, invInput):
        self.forwardModel = forwardModel
        self.costCalculator = costCalculator
        self.cgInput = invInput
        self.grid = forwardModel.getGrid()
        self.sources = forwardModel.getSource()
        self.receivers = forwardModel.getReceiver()
        self.frequencies = forwardModel.getFreq()
        self.chiEstimate = dataGrid2D(self.grid)


    def calculateCost(self, pData, pDataEst, eta):
        return eta * self.l2NormSquared(self.complex_sub(pData,pDataEst))

    def l2NormSquared(self, a):
        initialvalue = 0.0
        for i in a:
            initialvalue += (i.real * i.real + i.imag * i.imag)

        return initialvalue

    def complex_sub(self,a,b):
        for i in range(len(a)):
            a[i] -= b[i]
        return a

    def complex_add(self,a,b):
        for i in range(len(a)):
            a[i] += b[i]
        return b

    def reconstruct(self, pData, gInput):

        # Initialization of variables
        eta = 1.0 / self.calculateCost(pData, [0.0]* len(pData), 1.0)

        self.chiEstimate.zero()
        isConverged = False
        tolerance = 0.001
        counter = 1


        # Initialize conjugate gradient parameters
        gradientCurrent = dataGrid2D(self.grid)
        gradientPrevious = dataGrid2D(self.grid)

        residualCurrent = 0.0
        residualPrevious = 0.0
        alpha = 0.0

        regularisationCurrent = RegularisationParameters(dataGrid2D(self.grid))
        regularisationPrevious = RegularisationParameters(dataGrid2D(self.grid))

        regularisationPrevious.bSquared.zero()

        # Update contrast-function first time
        pDataEst = self.forwardModel.calculatePressureField(self.chiEstimate)

        
        residualVector = self.sub(pData, pDataEst)

        
        residualCurrent = self.calculateCost(pData, pDataEst, eta)

        zeta = self.calculateUpdateDirection(residualVector, gradientCurrent, eta)
        alpha = self.calculateStepSize(zeta, residualVector)


        self.chiEstimate = self.chiEstimate + (alpha * zeta)
        
        gradientPrevious = gradientCurrent
        residualPrevious = residualCurrent


        # main loop

        for i in range(gInput["max"]):
            # Calculate the pressure data from chiEstimate
            pDataEst = forwardModel.calculatePressureField(self.chiEstimate)
            residualVector = self.sub(pData, pDataEst)

            # Check residual
            residualCurrent = self.calculateCost(pData, pDataEst, eta)
            isConverged = (residualCurrent < tolerance)
            
            if isConverged:
                break

            # Initializae Regularisation Parameters
            # Note: deltaAmplification decreases the step size for increasing iteration step
            deltaAmplification = 1.0

            self.calculateRegularisationParameters(regularisationPrevious, regularisationCurrent, deltaAmplification)
            zeta = self.calculateUpdateDirectionRegularisation(residualVector, gradientCurrent, gradientPrevious, eta, regularisationCurrent, regularisationPrevious, zeta, residualPrevious)
            alpha = self.calculateStepSizeRegularisation(regularisationPrevious, regularisationCurrent, residualVector, eta, residualPrevious, zeta)
            
            self.chiEstimate = self.chiEstimate + (alpha * zeta)

            # save regularisation variables for next iteration
            gradientPrevious = gradientCurrent
            residualPrevious = residualCurrent
            self.chiEstimate.gradient(regularisationCurrent.gradientChi)
            self.calculateRegularisationErrorFunctional(regularisationPrevious, regularisationCurrent)

            regularisationPrevious.deltaSquared = regularisationCurrent.deltaSquared
            regularisationPrevious.bSquared = regularisationCurrent.bSquared

            # update counter
            counter+=1

        return self.chiEstimate

    def calculateStepSize(self, zeta, residualVector):
        alphaNumerator = 0.0
        alphaDenominator = 0.0
            
        kappaTimesZeta = self.forwardModel.calculatePressureField(zeta)

        for i in range(len(kappaTimesZeta)):
            alphaNumerator += (np.conjugate(residualVector[i])*kappaTimesZeta[i]).real
            alphaDenominator += (np.conjugate(kappaTimesZeta[i])*kappaTimesZeta[i]).real
        
        print(alphaNumerator)
        print(alphaDenominator)

        alpha = alphaNumerator / alphaDenominator

        return alpha

    def calculateUpdateDirection(self, residualVector, gradientCurrent, eta):
        kappaTimesResidual = dataGrid2D(self.grid)
        self.getUpdateDirectionInformation(residualVector, kappaTimesResidual)
        gradientCurrent =  dataGrid2D(self.mult(eta,kappaTimesResidual.getRealPart()))

        return gradientCurrent

    def getUpdateDirectionInformation(self, residualVector, kappaTimesResidual):
        kappaTimesResidual.zero()
        kappa = self.forwardModel.getKernel()
        for i in range(self.frequencies.count):
            l_i = i * self.receivers.count * self.sources.count
            for j in range(self.receivers.count):
                l_j = j* self.receivers.count
                for k in range(self.receivers.count):
                    dummy = kappa[l_i + l_j + k]
                    dummy.conjugate()

                    kappaTimesResidual = kappaTimesResidual + (dummy * residualVector[l_i + l_j + k])

    def sub(self,a,b):
        for i in range(len(a)):
            a[i] -= b[i]

        return a

    def mult(self,a,b):
        for i in b:
            i *= a

        return b
            
            

        
            





