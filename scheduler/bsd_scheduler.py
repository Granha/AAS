####################################################
#
#          BSD Scheduler
#
# Implementation from:
# https://www.classes.cs.uchicago.edu/archive/2016/
# fall/23000-1/pintos/doc/html/pintos_7.html#SEC131
####################################################

from abstract_scheduler import AbstractScheduler
from mlfq import MLFQ
from taskm.idle_task import IdleTask

# hard parameters of BSD scheduler
Alpha = (59.0/60, 4.0, 2.0, 2.0, 4)

# BSD (concrete) scheduler
class BSDScheduler(AbstractScheduler):
    
    # Time Slice in ticks
    TimeSlice = 4

    # Priority levels
    Levels = 64

    # Priority range
    MinPri = 0
    MaxPri = 63

    Alpha1Range = [  59.0/60 ]
    Alpha2Range = [ 2, 4, 6 ]
    Alpha3Range = [ 2, 4 ]
    Alpha4Range = [ 2, 4 ]
    # Time slice
    Alpha5Range = [2, 4, 6, 8, 10 ]

    def __init__(self, alpha=Alpha, enableEuler=True):
        AbstractScheduler.__init__(self, BSDScheduler.TimeSlice,
                                   enableEuler=enableEuler)        
        self.mlfq = MLFQ(BSDScheduler.MinPri, BSDScheduler.MaxPri)
        self.processor = None
        self.idleTask = IdleTask()
        self.curTaskTicks = 0
        self.loadAvg = 0.0
        self.alpha = alpha
    # __init__

    def enqueue(self, task):
        self.mlfq.enqueue(task)

    # update scheduler interal update
    # every forth tick
    def update_forth_tick(self):
        tasks = self.mlfq.listify()

        self.mlfq.emptify()

        for task in tasks:
            recentCpu = task.getRecentCpu()
            nice = task.getNice()

            priority = BSDScheduler.MaxPri - (recentCpu/self.alpha[1]) - (nice*self.alpha[2])

            if priority > BSDScheduler.MaxPri:
                priority = BSDScheduler.MaxPri
            elif priority < BSDScheduler.MinPri:
                priority = BSDScheduler.MinPri

            priority = int(priority)

            task.setPriority(priority)

        self.mlfq.addList(tasks)
    # update_forth_tick

    # update scheduler internal state
    # every second
    def update_each_second(self):
        tasks = self.mlfq.listify()

        for task in tasks:
            recentCpu = task.getRecentCpu()
            nice = task.getNice()

            recentCpu = ((self.alpha[3]*self.loadAvg)/\
                         (self.alpha[3]*self.loadAvg +1.0))*recentCpu  + nice
            
            task.setRecentCpu(recentCpu)

        readyThreads = len(tasks)
        runningTask = self.processor.getRunningTask()

        if not runningTask.isIdleTask():
            readyThreads += 1

        self.loadAvg = self.alpha[0]*self.loadAvg + \
                       (1-self.alpha[0])*readyThreads
    # update_each_second
                
    def _timerIntr(self, ticks):
        self.curTaskTicks += 1

        runningTask = self.processor.getRunningTask()
        
        assert runningTask is not None
        assert not runningTask.isInIO()

        runningTask.incRecentCpu()

        # every forth tick
        if ticks % 4 == 0:
            self.update_forth_tick()

        # every second
        if ticks % 50 == 0:
            self.update_each_second()

        bestPriority = self.mlfq.bestPriority()
        priority = runningTask.getPriority()
        
        if self.curTaskTicks >= BSDScheduler.TimeSlice or \
           bestPriority > priority:
            self.schedule()
    # _timerIntr

    def nextToRun(self):
        if self.mlfq.isEmpty():
            return self.idleTask

        return self.mlfq.extractMin()
    # nextToRun

    def getAlphaRange(self):
        return [ BSDScheduler.Alpha1Range, 
                 BSDScheduler.Alpha2Range,
                 BSDScheduler.Alpha3Range,
                 BSDScheduler.Alpha4Range,
                 BSDScheduler.Alpha5Range ]
    # getAlphaRange

# BSDScheduler
