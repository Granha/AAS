# Processor (single core, at least for now)
class Processor:

    def __init__(self):
        self.cpuTime = 0
        self.cpuTicks = 0
        self.tickCurTask = 0
        self.runningTask = None

    def getRunningTask():
        return self.runningTask

    # Prempt running task of NOP
    # if no task is running
    def premptRunningTask():
        runningTask = self.runningTask

        if runningTask is not None:
            runningTask.incUsedCpuTime(self.tickCurTask)

        self.runningTask = None
        self.tickCurTask = 0
        
        return runningTask

    def runTask(task):
        self.tickCurTask = 0
        self.runningTask = task

    def setTime(self, time):
        self.cpuTime = time

    def setTicks(self, ticks):
        self.cpuTicks = ticks

# Processor
