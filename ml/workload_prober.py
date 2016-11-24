##################################################
# WorkloadProber probes the (workload, parameter)
# space of a scheduler aggregating the tuples
# (workload, parameter, objVal). These tuples
# can be used to learn the mapping:
#
# workload |--> parameter.
###################################################
class WorkloadProber:

    # used to determine the unit of time
    # to collect workload data
    SliceMult = 25

    # number of samples for each alpha
    AlphaMult = 2

    def __init__(self, scheduler):
        # indicates whether the Prober
        # is probing the scheduler parameter space
        self.isProbing = False
        
        # mathematical relation (feature, alpha, objVal)
        self.relation = []

        self.scheduler = scheduler

        # initial value of scheduler parameters
        self.alpha = None

        # range for scheduler parameters
        self.alphaRange = scheduler.getAlphaRange()

        self.maxIndices = [len(range) for range\
                           in self.alphaRange]
        
        # size of the alpha space
        self.nAlpha = reduce(lambda x,y: x*y, self.maxIndices)

        self.nSamples = self.nAlpha*WorkloadProber.AlphaMult

        self.curIdices = None

        # tick window to collect workload
        # and objective function information
        # for a given fixed alpha
        self.tickWindow = scheduler.getTimeSlice()*\
                          WorkloadProber.SliceMult
    # __init__

    def getRelation(self):
        return self.relation

    def getTickWindow(self):
        return self.tickWindow

    def isProbing(self):
        return self.isProbing
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

        return tuple(alpha)
    # getCurAlpha

    def startProbing(self):
        self.isProbing = True

        self.curIdices = [0 for i in xrange(len(self.maxIndices))]

        self.relation = []
    # startProbing

    # Vary scheduler parameters
    # and store objective values
    def probe(self):

        # nothing to do
        if not self.isProbing:
            return False

        tasks = self.scheduler.getAllTaks()

        # compute the features
        # correspoding to the current
        # alpha set in the previous pass
        if self.alpha is not None:
            wFeatures = WorkloadFeatures(tasks)

        alpha = self.getCurAlpha()

        self.scheduler.setAlpha(alpha)

        objVal = Metric.objFunction(tasks)

        self.relation.append((wFeatures, alpha, objVal))
            
        if self.incCurIndices():
            self.isProbing = False

            return True
        
        return False
    # probe

# WorkloadProber
