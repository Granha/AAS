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
            curTime = self.getTime()
            ellapsed =  curTime - self.startTimeCurTask
            runningTask.prempt(curTime=curTime,
                               ellapsedCpuTime=ellapsed)

        self.runningTask = None
        self.startTimeCurTask = 0
        
        return runningTask

    def runTask(self, task):
        curTime = self.getTime()
        self.startTimeCurTask = curTime
        task.schedule(curTime)
        self.runningTask = task

    def setTime(self, time):
        self.cpuTime = time

    def setTicks(self, ticks):
        self.cpuTicks = ticks

# Processor
