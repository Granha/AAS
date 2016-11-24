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
from ml.workload_prober import WorkloadProber

class Euler:

    # 5 minutes (assuming 100 ticks is 1 second)
    CycleTicks = 5*60*100

    def __init__(self, scheduler):
        self.prober = WorkloadProber(scheduler)
        self.scheduler = scheduler
        self.elm = None

        scheduler.regiterTimerCallBack(self.timerCallBack)        
    # __init__    

    # Use Neural Network (ELM) to learn
    # the best mapping from workload
    # features to parameter
    # (prior to this phase sufficient
    # data must have been collected)
    def learn(self, relation):

        # TODO: use k++ to cluster the relation
        # values

        # TODO: learn using the ELM        
        
        return None
    # learn


    def timerCallBack(self, ticks):

        # beginning of a learning cycle
        if ticks % CycleTicks == 0:
            # probing should be long over by now
            # if it fails it means that the number
            # of ticks in a cycle is not sufficient
            assert not self.prober.isProbing

            self.prober.startProbing()

        # probing the scheduler
        elif self.prober.isProbing():

            ended = self.prober.probe()

            if ended:
                self.learn(self.prober.getRelation())

        # regular execution
        elif ticks % self.prober.getTickWindow() == 0:
            assert self.elm is not None

            wFeatures = WorkloadFeatures(tasks)

            # get the best learned scheduler
            # parameter given the past time
            # window
            alpha = self.elm.processSingle(wFeatures)

            self.scheduler.setAlpha(alpha)
    # timerCallBack

# Euler