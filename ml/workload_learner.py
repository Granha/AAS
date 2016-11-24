##################################################
# WorkloadLearner probes the parameter space of
# a scheduler and learn dynamically the best
# parameters for a given workload.
###################################################
class WorkloadLearner:

    # used to determine the unit of time
    # to collect workload data
    SliceMult = 25

    # number of samples for each alpha
    AlphaMult = 2

    def __init__(self, scheduler):
        # indicates whether the Learning
        # is probing the scheduler parameter space
        self.isProbing = False
        
        # mapping from workload feature and scheduler
        # parameter to objective value
        self.mapping = []

        self.scheduler = scheduler

        # initial value of scheduler parameters
        self.alpha = None

        # range for scheduler parameters
        self.alphaRange = scheduler.getRange()

        self.maxIndices = [len(range) for range\
                           in self.alphaRange]
        
        # size of the alpha space
        self.nAlpha = reduce(lambda x,y: x*y, self.maxIndices)

        self.nSamples = self.nAlpha*WorkloadLearner.AlphaMult

        self.curIdices = None

        # tick window to collect workload
        # and objective function information
        # for a given fixed alpha
        self.tickWindow = scheduler.getTimeSlice()*\
                          WorkloadLearner.SliceMult
    # __init__

    def incCurIndicesAux(self, i):

        assert i >= 0 and i < len(self.maxIndices)

        self.curIdices[i] += 1
        
        # carry condition
        if self.curIdices[i] == self.maxIndices[i]:
            self.curIdices[i] = 0

            if i > 1:
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

        self.mapping = []        
    # startProbing

    # Vary scheduler parameters
    # and store objective values
    def probe(self):               

        if not self.isProbing:
            return

        if self.alpha is not None:
            wFeatures = WorkloadFeatures(tasks)

        alpha = self.getCurAlpha()

        self.scheduler.setAlpha(alpha)

        objVal = Metric.objFunction(tasks)

        (wFeatures, alpha, objVal)
            
        if self.incCurIndices():
            self.isProbing = False

            return True        
        
        return False
    # probeScheduler

    # Use Neural Network (ELM) to learn
    # the best mapping from workload
    # features to parameter
    # (prior to this phase sufficient
    # data must have been collected)
    def learn(self):
        
        return None

# WorkloadLearner

