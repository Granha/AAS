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
from metrics.metric import Metric
from metrics.workload_prober import WorkloadProber
from ml.common import closestVecEl
from ml.elm import ELM
from ml.kmeans import kmeans
from ml.workload_features import WorkloadFeatures

import numpy as np
import time

class Euler:

    # 1 minutes (assuming 100 ticks is 1 second)
    CycleTicks = 1*60*10000

    TickOffset = 20

    # Minimum progress parameter for K-Means++
    EPS = 1e-4

    # Maximum number of clusters
    K = 20

    OUTPUT_DIR = 'out/'
    FILE_PREFIX_OBJ_VA = OUTPUT_DIR + 'obj_val_'
    FILE_PREFIX_ALPHA = OUTPUT_DIR + 'alpha_'
    FILE_PREFIX_WORKLOAD = OUTPUT_DIR + 'workload_'
    SUFFIX = '.dat'
    
    def __init__(self, scheduler, enabled=True):
        self.scheduler = scheduler
        self.enabled = enabled
        self.prober = WorkloadProber(scheduler)
        self.elm = None

        self.objValFile = None
        self.alphaFile = None
        self.workloadFile = None

        self.initFiles()

        scheduler.registerTimerCallBack(self.timerCallBack)
    # __init__

    def __del__(self):

        if self.objValFile is not None:
            self.objValFile.close()

        if self.alphaFile is not None:
            self.alphaFile.close()

        if self.workloadFile is not None:
            self.workloadFile.close()
    # __del__
        
    def initFiles(self):
        assert self.objValFile is None
        assert self.alphaFile is None
        assert self.workloadFile is None
        
        status = 'enabled_'
        if not self.enabled:
            status = 'disabled_'

        time_stamp = str(time.time())
        
        name = Euler.FILE_PREFIX_OBJ_VA + status \
                          + time_stamp + Euler.SUFFIX
        self.objValFile = open(name, "w")
        
        name = Euler.FILE_PREFIX_ALPHA + status \
                         + time_stamp + Euler.SUFFIX
        self.alphaFile = open(name, "w")
        
        name = Euler.FILE_PREFIX_WORKLOAD + status \
                            + time_stamp + Euler.SUFFIX
        self.workloadFile = open(name, "w")        
    # initFiles

    def collectStat(self, ticks):
        tasks = self.scheduler.getAllTaks()

        alpha = self.scheduler.getAlpha()

        wFeatures = WorkloadFeatures(tasks)
        features = wFeatures.getFeatures()

        objVal = Metric.objFunction(tasks,
                                    self.scheduler.getCurTime())
        
        self.objValFile.write("%d %f\n" % (ticks, objVal))
        self.alphaFile.write("%d %s\n" % (ticks, str(alpha)))
        self.workloadFile.write("%d %s\n" % (ticks, str(features)))        
    # collectStact

    # Use Neural Network (ELM) to learn
    # the best mapping from workload
    # features to parameter
    # (prior to this phase sufficient
    # data must have been collected)
    def learn(self, relation):
        assert self.enabled

        ###########################
        #      Clustering
        ###########################
        k = Euler.K
        points = [ features.getFeatures() \
                   for (features, alpha, objVal) in relation ]

        centroids, gamma, distortion = kmeans(k, points, Euler.EPS)
        k = len(centroids)

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
            mapping.append((relation[minIndex][0],
                            relation[minIndex][1]))

        #######################
        #     Learning
        #######################
        self.elm = ELM()
            
        inData = np.array([m[0].getFeatures() for m in mapping ])
        outData = np.array([m[1] for m in mapping ])
        
        self.elm.train(inData, outData)        
    # learn

    def timerCallBack(self, ticks):
        if ticks % self.prober.getTickWindow() \
           == Euler.TickOffset:
            self.collectStat(ticks)

        if not self.enabled:
            return

        # beginning of a learning cycle
        if ticks % Euler.CycleTicks == 0:
            # probing should be long over by now
            # if it fails it means that the number
            # of ticks in a cycle is not sufficient
            assert not self.prober.isProbing()

            self.prober.startProbing()

        # probing the scheduler
        elif self.prober.isProbing() and \
             ticks % self.prober.getTickWindow() \
             == Euler.TickOffset:

            isDone = self.prober.probe()

            if isDone:
                self.learn(self.prober.getRelation())

        # regular execution, we tune scheduling parameter
        # according to learned mapping
        elif self.elm is not None and \
             ticks % self.prober.getTickWindow() == \
             Euler.TickOffset:

            assert self.elm is not None

            tasks = self.scheduler.getAllTaks()

            wFeatures = WorkloadFeatures(tasks)
            features = wFeatures.getFeatures()

            # get the best learned scheduler
            # parameter given the past time
            # window
            alpha = self.elm.processSingle(features)
            alphaRange = self.scheduler.getAlphaRange()

            # adjust continuous values returned by the
            # neural network to valid values in the
            # range of alpha
            alpha = [ closestVecEl(alpha[i],alphaRange[i])\
                      for i in xrange(len(alpha)) ]

            self.scheduler.setAlpha(alpha)
    # timerCallBack

# Euler
