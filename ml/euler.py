######################################################################
#
# Euler System is the central piece of the Machine Learning module
# (ML). It dynamicaly probes the parameter space of a scheduler and
# learns the best parameters given a workload. Internally, a workload
# is represented a a feature vector, and the approximate mapping from
# a workload to scheduler parameters yielding the best objective value
# is provided by a Neural Network. More precisely, we use an Extrem
# Learning Machine (ELM) due to its training efficient.
#
######################################################################
from ml.elm import ELM
from ml.kmeans import kmeans
from ml.workload_prober import WorkloadProber

class Euler:

    # 5 minutes (assuming 100 ticks is 1 second)
    CycleTicks = 5*60*100

    # Minimum progress parameter for K-Means++
    EPS = 1e-3

    # Number of
    K = 10
    
    def __init__(self, scheduler):
        self.prober = WorkloadProber(scheduler)
        self.scheduler = scheduler
        self.elm = None

        scheduler.registerTimerCallBack(self.timerCallBack)        
    # __init__    

    # Use Neural Network (ELM) to learn
    # the best mapping from workload
    # features to parameter
    # (prior to this phase sufficient
    # data must have been collected)
    def learn(self, relation):

        ###########################
        #      Clustering
        ###########################
        k = Euler.K
        points = [ features.getFeatures() \
                   for (features, alpha, objVal) in relation ]

        print points
        import sys
        sys.exit(1)

        centroids, gamma, distortion = kmeans(k, points, Euler.EPS)

        ###############################
        #    Learning pre-processing
        ###############################
        n = len(points)
        clusters = [None]*k
    
        # group points in clusters
        for i in xrange(k):
            clusters[i] = [j for g,j in
                           zip(gamma, range(n)) if g == i]

        mapping = []
        
        for i in xrange(k):

            objVals = [relation[j][2] for j in clusters[i]]
            l = np.argmin(objVals)
            minIndex = clusters[i][l]

            # workload features -> alpha (scheduler parameters
            mapping.append((relation[minIndex][0], relation[minIndex][1]))

        #######################
        #     Learning
        #######################
        self.elm = ELM()
            
        inData = [ m[0] for m in mapping ]
        outData = [ m[1] for m in mapping ]

        self.elm.train(inData, outData)
        
        return None
    # learn

    def timerCallBack(self, ticks): 

        # beginning of a learning cycle
        if ticks % Euler.CycleTicks == 0:
            # probing should be long over by now
            # if it fails it means that the number
            # of ticks in a cycle is not sufficient
            assert not self.prober.isProbing()

            self.prober.startProbing()

        # probing the scheduler
        elif self.prober.isProbing():

            isDone = self.prober.probe()

            if isDone:
                self.learn(self.prober.getRelation())

        # regular execution, we tune scheduling parameter
        # according to learned mapping
        elif self.elm is not None and \
             ticks % self.prober.getTickWindow() == 0:

            assert self.elm is not None

            tasks = self.scheduler.getAllTaks()

            wFeatures = WorkloadFeatures(tasks)

            # get the best learned scheduler
            # parameter given the past time
            # window
            alpha = self.elm.processSingle(wFeatures)

            self.scheduler.setAlpha(alpha)
    # timerCallBack

# Euler
