# Processor (single core, at least for now)
class Processor:

    def __init__(self):
        self.cpuTime = 0
        self.cpuTicks = 0
        self.startTimeCurTask = 0
        self.runningTask = None
        self.startUsedCpuTime = None

    def getTime(self):
        return self.cpuTime

    def getTicks(self):
        return self.cpuTicks
    
    def getRunningTask(self):
        return self.runningTask

    def updateRunningTask(self):
        runningTask = self.runningTask

        if runningTask is not None:
            curTime = self.getTime()
            ellapsed =  curTime - self.startTimeCurTask
            assert ellapsed >= 0
            usedCpuTime = self.startUsedCpuTime + ellapsed
            runningTask.setUsedCpuTime(usedCpuTime)            
    # updateRunningTask

    # Prempt running task of NOP
    # if no task is running
    def premptRunningTask(self):
        runningTask = self.runningTask

        if runningTask is not None:
            self.updateRunningTask()
            curTime = self.getTime()
            runningTask.prempt(curTime)

        self.runningTask = None
        self.startTimeCurTask = 0
        
        return runningTask

    def runTask(self, task):
        curTime = self.getTime()
        self.startTimeCurTask = curTime
        task.schedule(curTime)
        self.runningTask = task
        self.startUsedCpuTime = task.getUsedCpuTime()

    def setTime(self, time):
        assert time >= self.cpuTime
        
        self.cpuTime = time

    def setTicks(self, ticks):
        self.cpuTicks = ticks

# Processor
