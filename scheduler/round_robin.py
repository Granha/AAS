from abstract_scheduler import AbstractScheduler

# Basic Round Robin Scheduler
class RoundRobin(AbstractScheduler):

    # Time slice in ticks
    TimeSlice = 4
    
    # Possible values for time slice
    TimeSliceRange = [2, 4, 6, 8, 10, 12, 16, 20, 40]

    def __init__(self, enableEuler=True):
        AbstractScheduler.__init__(self, RoundRobin.TimeSlice,
                                   enableEuler=enableEuler)
        self.fifo = []
        self.curTaskTicks = 0
        self.setAlpha([RoundRobin.TimeSlice])
    # __init__

    def enqueue(self, task):
        if task is not None and \
           not task.isIdleTask():
            self.fifo.append(task)
    # enqueue

    def _timerIntr(self, ticks):
        self.curTaskTicks += 1
        
        if self.curTaskTicks >= self.getTimeSlice():
            self.schedule()
    # _timerIntr

    def nextToRun(self):
        if len(self.fifo) == 0:
            return self.idleTask

        return self.fifo.pop(0)
    # nextToRun

    def getAlphaRange(self):
        return [ RoundRobin.TimeSliceRange ]
        
# RoundRobin
