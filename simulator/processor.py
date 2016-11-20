# Processor (single core, at least for now)
class Processor:

    def __init__(self):
        self.cpuTime = 0
        self.cpuTicks = 0
        self.tickCurTask = 0
        self.runningTask = None

    def getRunningTask():
        return self.runningTask

    def premptRunningTask():
        runningTask = self.runningTask

        runningTask.incUsedCpuTime(self.tickCurTask)

        self.runningTask = None
        self.tickCurTask = 0
        return self.runningTask

    def runTask(task):
        self.runningTask = task
        self.tickCurTask = 0

    def setTime(self, time):
        self.cpuTime = time

    def setTicks(self, ticks):
        self.cpuTicks = ticks

# Processor
