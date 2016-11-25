from metrics.metric import Metric
from numpy.fft import fft

import numpy as np

class WorkloadFeatures:
    
    # Number of moments to compute
    NumMoment = 4

    def __init__(self, tasks):
        # stores the first NumMoment moments
        # of the interactiveness distribution
        self.moments = [ None for i in \
                         xrange(WorkloadFeatures.NumMoment)]
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

        # use the counting measure        
        n = len(interactVec)        
        
        # note that we work with the count measure,
        # thus the following moment computation is
        # correct
        for i in xrange(1,WorkloadFeatures.NumMoment+1):

            self.moments[i-1] = sum([inter**i for inter \
                                     in interactVec ])/float(n)

        return self.moments
    # computeMoments

    # compute the frequency and absoluted
    # corresponding to the largest coefficient
    # in absolute value
    def computeFourier(self, tasks):
        interactVec = Metric.interacMetric(tasks)

        assert len(tasks) > 0

        coeff = list(fft(interactVec))

        # frequency zero corresponding to
        # the integral of the original signal
        coeff[0] = 0

        coeff = np.abs(coeff)
        maxFreq = np.argmax(coeff)
        maxCoeff = np.max(coeff)

        n = float(len(coeff)) 
        
        self.fourier = [ maxFreq/n, maxCoeff ]

        return self.fourier
    # computeFourier

    def extractFeatures(self, tasks):
        interactVec = Metric.interacMetric(tasks)
        
        moments = self.computeMoments(tasks)        
        fourier = self.computeFourier(tasks)

        norm = np.linalg.norm(moments)        
        moments = moments / (norm + 1e-15)

        norm = np.linalg.norm(fourier)
        fourier = fourier / (norm + 1e-15)
        
        features = moments.tolist() + fourier.tolist()

        # Idea to improve the feature vector
        # if necessary
        #nWeaklyInter = len([inter for inter in interacMetric if inter >= 1.0/4])

        #nInter = len([inter for inter in interacMetric if inter >= 1.0/2])                

        norm = np.linalg.norm(features)

        # normalize the features
        # to make learning more robust
        features = features / (norm + 1e-15)

        self.features = features

        return self.features
    # extractFeatures
    
# WorkloadFeatures

