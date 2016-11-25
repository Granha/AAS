# Processor (single core, at least for now)
class Processor:

    def __init__(self):
        self.cpuTime = 0
        self.cpuTicks = 0
        self.startTimeCurTask = 0
        self.runningTask = None

    def getTime(self):
        return self.cpuTime

    def getTicks(self):
        return self.cpuTicks
    
    def getRunningTask(self):
        return self.runningTask

    # Prempt running task of NOP
    # if no task is running
    def premptRunningTask(self):
        runningTask = self.runningTask

        if runningTask is not None:
            ellapsed =  self.getTime() - self.startTimeCurTask
            runningTask.incUsedCpuTime(ellapsed)

        self.runningTask = None
        self.startTimeCurTask = 0
        
        return runningTask

    def runTask(self, task):
        self.startTimeCurTask = self.getTime()
        self.runningTask = task

    def setTime(self, time):
        self.cpuTime = time

    def setTicks(self, ticks):
        self.cpuTicks = ticks

# Processor
