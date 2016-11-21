from abstract_scheduler import AbstractScheduler
from mlfq import MLFQ

# BSD (concrete) scheduler
class BSDScheduler(AbstractScheduler):

    # Time Slice in ticks
    TimeSlice = 4

    # Priority levels
    Levels = 64

    # Priority range
    MinPri = 0
    MaxPri = 63

    def __init__(self):
        self.mlfq = MLFQ(MinPri, MaxPri)
        self.processor = None
        self.idleTask = IdleTask()
        self.curTaskTicks = 0
        self.loadAvg = 0.0

    def enqueue(self, task):
        self.mlfq.enqueue(task)

    def start(self):
        self.schedule()

    # update scheduler interal update
    # every forth tick
    def update_forth_tick(self):
        tasks = self.mlfq.listify()

        self.mlfq.empitfy()

        for task in tasks:
            recentCpu = task.getRecentCpu()
            nice = task.getNice()

            priority = BSDScheduler.MaxPri - (recentCpu/4.0) - (nice*2)

            if priority > BSDScheduler.MaxPri:
                priority = BSDScheduler.MaxPri
            elif priority < BSDScheduler.MinPri:
                priority = BSDScheduler.MinPri                

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

            recentCpu = ((2*self.loadAvg)/(2*self.loadAvg +1.0))*recentCpu + nice
            task.setRecentCpu(recentCpu)

        readyThreads = len(tasks)
        runningTask = self.processor.getRunningTask()

        if not runningTask.isIdleTask():
            readyThreads += 1

        self.loadAvg = (59.0/60)*self.loadAvg + (1.0/60)*readyThreads
                
    def timerIntr(self, ticks):
        self.curTaskTicks += 1

        runningTask = self.processor.getRunningTask()

        assert runningTask is not None

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

    def block(self, task):
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
        if self.mlfq.isEmpty():
            return self.idleTask

        return self.mlfq.extractMin()

    def schedule(self):
        task = self.processor.premptRunningTask()
        
        self.enqueue(task)
        
        next = self.nextToRun()

        assert next is not None

        self.curTaskTicks = 0
        
        self.processor.runTask(next)        

# BSDScheduler
