from metric.metric import Metric

import numpy as np
import np.fft

class WorkloadFeatures:
    
    # Number of moments to compute
    NumMoment = 4

    def __init__(self, tasks):
        # stores the first NumMoment moments
        # of the interactiveness distribution
        self.moments = None
        self.fourier = None
        self.features = None

        self.extractFeatures(tasks)


    #######################
    #      getters
    #######################        

    def getMoments(self):
        return self.moments

    def getFourier(self):
        return self.fourier

    def getFeatures(self):
        return self.features
        
    # compute moments of interactiveness
    def computeMoments(self, tasks):
        interactVec = Metric.interacMetric(tasks)
        
        # note that we work with the count measure,
        # thus the following moment computation is
        # correct
        for i in xrange(1,WorkloadFeatures.NumMoment):

            self.moments[i] = [inter**i for inter in interactVec ]

        return self.moments
    # computeMoments

    # compute the frequency and absoluted
    # corresponding to the largest coefficient
    # in absolute value
    def computeFourier(self, tasks):
        interactVec = Metric.interacMetric(tasks)

        assert len(tasks) > 0

        coeff = numpy.fft(interactVec)

        # remove frequency zero corresponding to
        # the integral of the original signal
        coeff.pop(0)

        coeff = np.abs(coeff)
        maxFreq = np.argmax(coeff)
        maxCoeff = np.max(coeff)

        self.fourier = [ maxFreq, maxCoeff ]

        return self.fourier
    # computeFourier

    def extractFeatures(self, tasks):
        moments = self.computeMoments(tasks)        
        fourier = self.computeFourier(tasks)
        
        features = moments + fourier

        norm = np.linalg.norm(features)

        # normalize the features
        # to make learning more robust
        features = features / norm

        self.features = features

        return self.features
    # extractFeatures
    
# WorkloadFeatures

