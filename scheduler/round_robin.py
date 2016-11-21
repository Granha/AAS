from abstract_scheduler import AbstractScheduler
from task.idle_task import IdleTask

# Basic Round Robin Scheduler
class RoundRobin(AbstractScheduler):

    # Time Slice in ticks
    TimeSlice = 4

    def __init__(self):
        self.fifo = []
        self.processor = None
        self.idleTask = IdleTask()
        self.curTaskTicks = 0

    def enqueue(self, task):        
        if task is not None and \
           not task.isIdleTask():
            self.fifo.append(task)

    def start(self):
        self.schedule()

    def timerIntr(self, ticks):
        self.curTaskTicks += 1
        
        if self.curTaskTicks >= RoundRobin.TimeSlice:
            self.schedule()

    def block(self, task):
        task.incTimesBlocked()
        
        self.schedule()

    def unblock(self, task):
        self.enqueue(task)        
        self.schedule()

    def finishTask(self, task):
        self.schedule()

    def createTask(self, task):
        self.enqueue(task)        
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

        self.curTaskTicks = 0
        
        self.processor.runTask(next)        
        
# RoundRobin
