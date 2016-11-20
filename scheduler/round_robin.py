from task.idle_task import IdleTask

# Basic Round Robin Scheduler
class RoundRobin:

    # Time Slice in ticks
    TimeSlice = 4

    def __init__(self):
        self.fifo = []
        self.processor = None
        self.idleTask = IdleTask()
        self.curTaskTicks = 0

    def enqueue(self, task):
        if not task.isIdleTask():
            self.fifo.append(task)

    def start():
        self.schedule()

    def timerIntr(ticks):
        self.curTaskTicks += 1
        
        if self.curTaskTicks >= TimeSlice:
            self.schedule()

    def block(task):
        self.schedule()

    def unblock(task):
        self.enqueue(task)        
        self.schedule()

    def finishTask(task):
        self.schedule()

    def createTask(task):
        self.enqueue(task)        
        self.schedule()

    def setProcessor(processor):
        self.processor = processor

    def nextToRun(self):
        if len(self.queue) == 0:
            return self.idleTask

        return self.queue.pop(0)

    def schedule(self):
        task = self.processor.premptRunningTask()
        self.enqueue(task)
        next = self.nextToRun()

        assert next is not None

        self.curTaskTicks = 0
        
        self.processor.runTask(next)        
        
# RoundRobin
