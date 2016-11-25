from abstract_scheduler import AbstractScheduler

# Basic Round Robin Scheduler
class RoundRobin(AbstractScheduler):

    # Time Slice in ticks
    TimeSlice = 4

    def __init__(self):
        AbstractScheduler.__init__(self, RoundRobin.TimeSlice)
        self.fifo = []
        self.curTaskTicks = 0
        self.setAlpha([RoundRobin.TimeSlice])

    def enqueue(self, task):
        if task is not None and \
           not task.isIdleTask():
            self.fifo.append(task)

    def start(self):
        self.schedule()

    def _timerIntr(self, ticks):
        self.curTaskTicks += 1
        
        if self.curTaskTicks >= self.getTimeSlice():
            self.schedule()

    def _block(self, task):
        self.schedule()

    def _unblock(self, task):
        self.enqueue(task)
        runningTask = self.processor.getRunningTask()

        if runningTask.isIdleTask():
            self.schedule()

    def _finishTask(self, task):
        self.schedule()

    def _createTask(self, task):
        self.enqueue(task)

        runningTask = self.processor.getRunningTask()

        if runningTask.isIdleTask():        
            self.schedule()

    def setProcessor(self, processor):
        self.processor = processor

    def nextToRun(self):
        if len(self.fifo) == 0:
            return self.idleTask

        return self.fifo.pop(0)

    def schedule(self):
        task = self.processor.premptRunningTask()
        
        self.enqueue(task)
        
        next = self.nextToRun()

        assert next is not None
        assert not next.isInIO()

        self.curTaskTicks = 0
        
        self.processor.runTask(next)
    # schedule

    def getAlphaRange(self):
        # Possible Time Slice values for Round Robin
        return [[2, 4, 6, 8, 10, 12, 16, 20, 40]]
        
# RoundRobin
