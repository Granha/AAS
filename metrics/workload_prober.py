##################################################
# WorkloadProber probes the (workload, parameter)
# space of a scheduler aggregating the tuples
# (workload, parameter, objVal). These tuples
# can be used to learn the mapping:
#
# workload |--> parameter.
###################################################
from metrics.metric import Metric
from ml.workload_features import WorkloadFeatures

class WorkloadProber:

    # used to determine the unit of time
    # to collect workload data
    SliceMult = 1000

    # number of samples for each alpha
    AlphaMult = 4

    def __init__(self, scheduler):
        # indicates whether the Prober
        # is probing the scheduler parameter space
        self._isProbing = False
        
        # mathematical relation (feature, alpha, objVal)
        self.relation = []

        self.scheduler = scheduler

        # initial value of scheduler parameters
        self.alpha = None

        # range for scheduler parameters
        self.alphaRange = scheduler.getAlphaRange()

        self.maxIndices = [len(vals) for vals \
                           in self.alphaRange]
        
        # size of the alpha space
        self.nAlpha = reduce(lambda x,y: x*y, self.maxIndices)

        self.nSamples = self.nAlpha*WorkloadProber.AlphaMult

        self.nPasses = 0

        self.curIdices = None

        # tick window to collect workload
        # and objective function information
        # for a given fixed alpha
        self.tickWindow = self.getTickWindow()
    # __init__

    def getRelation(self):
        return self.relation

    def getTickWindow(self):
        assert self.scheduler.getTimeSlice() > 0
        return WorkloadProber.SliceMult*4
#        return self.scheduler.getTimeSlice()*\
#                          WorkloadProber.SliceMult
    
    def isProbing(self):
        return self._isProbing
    # getIsProbing

    def incCurIndicesAux(self, i):

        assert i >= 0 and i < len(self.maxIndices)        

        self.curIdices[i] += 1

        # carry condition
        if self.curIdices[i] == self.maxIndices[i]:
            self.curIdices[i] = 0

            if i >= 1:
                return self.incCurIndicesAux(i-1)
            elif i == 0:
                return True

        return False
    # incCurIndicesAux

    def incCurIndices(self):

        return self.incCurIndicesAux(len(self.maxIndices)-1)

    def getCurAlpha(self):

        alpha = [self.alphaRange[i][self.curIdices[i]]\
                 for i in xrange(len(self.maxIndices)) ]

        return alpha
    # getCurAlpha

    def startProbing(self):
        self._isProbing = True

        self.alpha = None

        self.nPasses = 0        

        self.curIdices = [0 for i in xrange(len(self.maxIndices))]

        self.relation = []
    # startProbing

    # Vary scheduler parameters
    # and store objective values
    def probe(self):

        # nothing to do
        if not self._isProbing:
            return False

        tasks = self.scheduler.getAllTaks()

        alpha = self.getCurAlpha()

        # first probe
        if self.alpha is None:
            self.alpha = alpha
            self.scheduler.setAlpha(alpha)
            return False

        wFeatures = WorkloadFeatures(tasks)

        objVal = Metric.objFunction(tasks,
                                    self.scheduler.getCurTime())

        self.relation.append((wFeatures, alpha, objVal))            

        isOverflow = self.incCurIndices()
        alpha = self.getCurAlpha()

        self.scheduler.setAlpha(alpha)
        self.alpha = alpha

        # end probing phase
        if isOverflow:
            self.nPasses += 1

            if self.nPasses == WorkloadProber.AlphaMult:
                self._isProbing = False
                
                return True
        
        return False
    # probe

# WorkloadProber
