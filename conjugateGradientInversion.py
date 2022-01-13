
from numpy.lib.function_base import gradient
from finiteDifferenceForwardModel import FiniteDifferenceForwardModel
from regularization import RegularisationParameters
from dataGrid2D import dataGrid2D
import numpy as np
import copy

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
        self.magnitude = self.frequencies.count * self.sources.count * self.receivers.count

    def calculateCost(self, pData, pDataEst, eta):
        return eta * self.l2NormSquared(np.subtract(pData,pDataEst))

    def l2NormSquared(self, a):
        initialvalue = 0.0
        for i in a:
            initialvalue += (i.real * i.real + i.imag * i.imag)

        return initialvalue

    def complex_add(self,a,b):
        for i in range(len(a)):
            a[i] += b[i]
        return b

    def reconstruct(self, pData, gInput):

        # Initialization of variables
        eta = 1.0 / self.calculateCost(pData, [0.0]* len(pData), 1.0)

        self.chiEstimate.zero()
        isConverged = False
        tolerance = 9.99*10**-7
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

        
        residualVector = np.subtract(pData, pDataEst)

        
        residualCurrent = self.calculateCost(pData, pDataEst, eta)

        zeta = gradientCurrent = copy.deepcopy(self.calculateUpdateDirection(residualVector, gradientCurrent, eta))
        alpha = self.calculateStepSize(zeta, residualVector)


        self.chiEstimate = self.chiEstimate + (np.multiply(alpha, zeta))
        
        gradientPrevious = copy.deepcopy(gradientCurrent)
        residualPrevious = copy.deepcopy(residualCurrent)


        # main loop

        for i in range(gInput["max"]):
            # Calculate the pressure data from chiEstimate
            pDataEst = self.forwardModel.calculatePressureField(self.chiEstimate)
            residualVector = np.subtract(pData, pDataEst)

            # Check residual
            residualCurrent = self.calculateCost(pData, pDataEst, eta)
            isConverged = (residualCurrent < tolerance)
            
            if isConverged:
                break

            # Initializae Regularisation Parameters
            # Note: deltaAmplification decreases the step size for increasing iteration step
            deltaAmplification = 100 / (int(i) + 1.0)

            

            self.calculateRegularisationParameters(regularisationPrevious, regularisationCurrent, deltaAmplification)
            zeta, gradientCurrent, gradientPrevious = self.calculateUpdateDirectionRegularisation(residualVector, gradientCurrent, gradientPrevious, eta, regularisationCurrent, regularisationPrevious, zeta, residualPrevious)
            alpha = self.calculateStepSizeRegularisation(regularisationPrevious, regularisationCurrent, residualVector, eta, residualPrevious, zeta)
            
            self.chiEstimate = self.chiEstimate + (zeta * alpha)

            # save regularisation variables for next iteration
            gradientPrevious = copy.deepcopy(gradientCurrent)
            residualPrevious = copy.deepcopy(residualCurrent)
            self.chiEstimate.gradient(regularisationCurrent.gradientChi)
            self.calculateRegularisationErrorFunctional(regularisationPrevious, regularisationCurrent)

            regularisationPrevious.deltaSquared = copy.deepcopy(regularisationCurrent.deltaSquared)
            regularisationPrevious.bSquared = copy.deepcopy(regularisationCurrent.bSquared)

            print("LOOP :"+ str(counter))
            # update counter
            counter+=1

        return self.chiEstimate


    def calculateRegularisationErrorFunctional(self, regularisationPrevious, regularisationCurrent):
        gradientChiNormsquaredCurrent = (regularisationCurrent.gradientChi[0]* regularisationCurrent.gradientChi[0])+(regularisationCurrent.gradientChi[1]*regularisationCurrent.gradientChi[1])

        integral = (gradientChiNormsquaredCurrent + regularisationPrevious.deltaSquared) / (regularisationPrevious.gradientChiNormSquared + regularisationPrevious.deltaSquared)

        regularisationPrevious.errorFunctional = (1.0 / (self.grid.getDomainArea())) * integral.summation() * self.grid.getCellVolume()

    def calculateKappaTimesZeta(self, zeta, kernel):
        kappa = self.forwardModel.getKernel()
        for i in range(self.magnitude):
            kernel[i] = self.dotProduct(kappa[i], zeta)
        
        return kernel

    def dotProduct(self,a,b):
        prod = 0.0
        for i in range(len(a.data)):
            prod += a.data[i] * b.data[i]
        return prod

    def calculateStepSizeRegularisation(self, regularisationPrevious, regularisationCurrent, residualVector, eta, fDataPrevious, zeta):
        kappaTimesZeta = [0] *(self.frequencies.count * self.sources.count * self.receivers.count)

        kappaTimesZeta = self.calculateKappaTimesZeta(zeta, kappaTimesZeta)

        a0 = fDataPrevious

        a1 = 0.0
        a2 = 0.0

        for i in range(len(kappaTimesZeta)):
            a1 += -2.0 * eta * (np.conjugate(residualVector[i])*kappaTimesZeta[i]).real
            a2 += eta * (np.conjugate(kappaTimesZeta[i])*kappaTimesZeta[i]).real
        

        bGradientChiSquaredXDirection = regularisationCurrent.b * regularisationPrevious.gradientChi[0] * regularisationCurrent.b * regularisationPrevious.gradientChi[0]
        bGradientChiSquaredZDirection = regularisationCurrent.b * regularisationPrevious.gradientChi[1] * regularisationCurrent.b *regularisationPrevious.gradientChi[1]
       
        b0 = ((bGradientChiSquaredXDirection.summation() + bGradientChiSquaredZDirection.summation()) + regularisationPrevious.deltaSquared * regularisationCurrent.bSquared.summation()) * self.grid.getCellVolume()

        gradientZeta = [dataGrid2D(self.grid),dataGrid2D(self.grid)]
        zeta.gradient(gradientZeta)

        bGradientZetabGradientChiX = regularisationCurrent.b * gradientZeta[0] * regularisationCurrent.b * regularisationPrevious.gradientChi[0]
        bGradientZetabGradientChiZ = regularisationCurrent.b * gradientZeta[1] * regularisationCurrent.b * regularisationPrevious.gradientChi[1]
        b1 = 2.0 * (bGradientZetabGradientChiX.summation() + bGradientZetabGradientChiZ.summation()) * self.grid.getCellVolume()

        bTimesGradientZetaXdirection = regularisationCurrent.b * gradientZeta[0]
        bTimesGradientZetaZdirection = regularisationCurrent.b * gradientZeta[1]
        bTimesGradientZetaXdirection.square()
        bTimesGradientZetaZdirection.square()
        b2 = (bTimesGradientZetaXdirection.summation() + bTimesGradientZetaZdirection.summation()) * self.grid.getCellVolume()

        derA = 4.0 * a2 * b2
        derB = 3.0 * (a2 * b1 + a1 * b2)
        derC = 2.0 * (a2 * b0 + a1 * b1 + a0 * b2)
        derD = a1 * b0 + a0 * b1

        return self.findRealRoolFromCubic(derA, derB, derC, derD)

    def findRealRoolFromCubic(self, a,b,c,d):
        f = ((3.0 * c / a) - (b**2 / a**2)) / 3.0
        g = ((2.0 * b**3 / a**3) -(9.0*b*c / a**2) + (27.0 * d/a)) / 27.0
        h = (g**2 / 4.0) + f**3  / 27.0
        r = -(g/2.0) + np.sqrt(h)
        s = np.cbrt(r)
        t = -(g/2.0) - np.sqrt(h)
        u = np.cbrt(t)

        realRoot = s + u - (b / (3.0 * a))

        return realRoot



    def calculateUpdateDirectionRegularisation(self,residualVector, gradientCurrent, gradientPrevious, eta, regularisationCurrent, regularisationPrevious, zeta, residualPrevious):
            kappaTimesResidual = dataGrid2D(self.grid)
            kappaTimesResidual.zero()
            kappaTimesResidual = self.getUpdateDirectionInformation(residualVector, kappaTimesResidual)
            gradientCurrent = (regularisationCurrent.gradient * residualPrevious) + np.multiply(eta*regularisationPrevious.errorFunctional, kappaTimesResidual.getRealPart());   

            if not isinstance(gradientPrevious,dataGrid2D):
                temp = dataGrid2D(self.grid)
                temp.data = gradientPrevious
                gradientPrevious = temp
            
            gamma = gradientCurrent.innerProduct(np.subtract(gradientCurrent,gradientPrevious)) / gradientPrevious.innerProduct(gradientPrevious);   
            if not isinstance(zeta, dataGrid2D):
                temp = dataGrid2D(self.grid)
                temp.data = zeta
                zeta = temp
                
            res = gradientCurrent + (zeta*gamma)
            return res, gradientCurrent, gradientPrevious

    def calculateRegularisationParameters(self, regularisationPrevious, regularisationCurrent, deltaAmplification):
        self.chiEstimate.gradient(regularisationPrevious.gradientChi)
        
        regularisationPrevious.gradientChiNormSquared = (regularisationPrevious.gradientChi[0] * regularisationPrevious.gradientChi[0]) + (regularisationPrevious.gradientChi[1] * regularisationPrevious.gradientChi[1])

        regularisationCurrent.bSquared = self.calculateWeightingFactor(regularisationPrevious);   
        regularisationCurrent.b = copy.deepcopy(regularisationCurrent.bSquared)
        regularisationCurrent.b.sqrt()

        regularisationCurrent.deltaSquared = self.calculateSteeringFactor(regularisationPrevious, regularisationCurrent, deltaAmplification);   
        regularisationCurrent.gradient = self.calculateRegularisationGradient(regularisationPrevious)


    def calculateWeightingFactor(self,regularisationPrevious):
        bsquared = regularisationPrevious.gradientChiNormSquared + regularisationPrevious.deltaSquared
        bsquared.data = np.reciprocal(bsquared.data)
        bsquared.data = [x * (1.0/self.grid.getDomainArea()) for x in bsquared.data]
        return bsquared

    def calculateSteeringFactor(self,regularisationPrevious, regularisationCurrent, deltaAmplification):
        bTimesGradientChiXSquared = regularisationCurrent.b * regularisationPrevious.gradientChi[0]
        bTimesGradientChiXSquared.square()
        bTimesGradientChiZSquared = regularisationCurrent.b* regularisationPrevious.gradientChi[1]
        bTimesGradientChiZSquared.square()

        bTimesGradientChiNormSquared = (bTimesGradientChiXSquared + bTimesGradientChiZSquared).summation()
        bSquaredSummed = 0
        [bSquaredSummed := bSquaredSummed + x for x in regularisationCurrent.bSquared.data]
        res = deltaAmplification * 0.5 * bTimesGradientChiNormSquared / bSquaredSummed
        return res

    def calculateRegularisationGradient(self,regularisationPrevious):
        temporaryGradient = [dataGrid2D(self.grid),dataGrid2D(self.grid)]

        bSquaredTimesGradientChiX = regularisationPrevious.bSquared * regularisationPrevious.gradientChi[0]
        bSquaredTimesGradientChiX.gradient(temporaryGradient)
        gradientBSquaredTimesGradientChiX = temporaryGradient[0]

        bSquaredTimesGradientChiZ = regularisationPrevious.bSquared * regularisationPrevious.gradientChi[1]
        bSquaredTimesGradientChiZ.gradient(temporaryGradient)
        gradientBSquaredTimesGradientChiZ = temporaryGradient[1]

        return gradientBSquaredTimesGradientChiX + gradientBSquaredTimesGradientChiZ

    def calculateStepSize(self, zeta, residualVector):
        alphaNumerator = 0.0
        alphaDenominator = 0.0
            
        kappaTimesZeta = self.forwardModel.calculatePressureField(zeta)

        for i in range(len(kappaTimesZeta)):
            alphaNumerator += (np.conjugate(residualVector[i])*kappaTimesZeta[i]).real
            alphaDenominator += (np.conjugate(kappaTimesZeta[i])*kappaTimesZeta[i]).real
        
        alpha = alphaNumerator / alphaDenominator

        return alpha

    def calculateUpdateDirection(self, residualVector, gradientCurrent, eta):
        kappaTimesResidual = dataGrid2D(self.grid)
        kappaTimesResidual = self.getUpdateDirectionInformation(residualVector, kappaTimesResidual)
        gradientCurrent =  np.multiply(eta,kappaTimesResidual.getRealPart())

        return gradientCurrent

    def mult_list(self,a ,b):
        res = [0] * len(b)
        for i in range(len(b)):
            res[i] = b[i] * a
        return res

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
    
                    kappaTimesResidual = kappaTimesResidual + np.multiply(residualVector[l_i + l_j + k],dummy.data)
        return kappaTimesResidual



        
            





