from metric.metric import Metric

import numpy.fft

class WorkloadFeatures:
    
    MaxMoment = 4

    def __init__(self):
        self.moments = []
        self.fourier = []

    # compute moments of interactiveness
    def computeMoments(self, tasks):
        interactVec = Metric.interacMetric(tasks)

        for i in xrange(1,WorkloadFeatures.MaxMoment):

            self.moments[i] = [inter**i for inter in interactVec ]
    # computeMoments

    # compute Fourier coefficients
    def computeFourier(self, tasks):

    # computeFourier
    
# WorkloadFeatures

