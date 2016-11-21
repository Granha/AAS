class Task:

    def __init__(self, name, priority, creationTime,
                 totalCpuTime, ioList):
        self.name = name
        self.priority = priority
        self.usedCpuTime = 0
        self.creationTime = creationTime
        self.totalCpuTime = totalCpuTime
        self.ioList = ioList
        self.nextIO = 0
        self.boolIsInIO = False
        self.nice = 0
        self.recentCpu = 0
        self.timesBlocked = 0
        self.totalReadyWait = 0
        self.timesScheduled = 0

    ######################
    #     getters
    ######################
    def getName(self):
        return self.name

    def getPriority(self):
        return self.priority

    def getUseCpuTime(self):
        return self.usedCpuTime

    def getCreationTime(self):
        return self.creationTime

    def getTotalCpuTime(self):
        return self.totalCpuTime

    def getIOList(self):
        return self.ioList

    def getRecentCpu(self):
        return self.recentCpu

    def getNice(self):
        return self.nice

    def getTimesBlocked(self):
        return self.timesBlocked

    def getTotalReadyWait(self):
        return self.totalReadyWait

    def getTimesScheduled(self):
        return self.timesScheduled

    def getAvgBlocking(self):
        return float(self.getTimesBlocked)/\
            self.getUseCpuTime()

    def getAvgReadyWait(self):
        return float(self.getTotalReadyWait())/\
            self.getTimesScheduled()

    def getRemainingCpuTime(self):
        return self.totalCpuTime - self.usedCpuTime

    def getNextIO(self):
        return self.ioList.get(self.nextIO)

    #######################
    #      setters
    #######################
    def setPriority(self, priority):
        self.priority = priority
    
    def setRecentCpu(self, recentCpu):
        self.recentCpu = recentCpu

    def setNice(self, nice):
        self.nice = nice

    ############################
        
    def incRecentCpu(self):
        self.recentCpu += 1

    def incTimesBlocked(self):
        self.timesBlocked += 1

    def incTimesScheduled(self):
        self.timesScheduled += 1        

    #######################
    #   Scheduler methods
    #######################

        
    ##########################
    #   Simulator methods
    ##########################
    def isInIO(self):
        return self.boolIsInIO
    
    def setInIO(self, val):
        self.boolIsInIO = val
    
    def popNextIO(self):
        io = self.getNextIO()
        
        if io is not None:
            self.nextIO += 1

        return io

    def stillHasIO(self):

        if self.getNextIO() is not None:
            return True

        return False

    #################################
    #    Shared methods between
    #    Simulator and Scheduler
    #################################
    def incUsedCpuTime(self, amount):
        self.usedCpuTime += amount

    # Reset internal state
    def reset(self):
        self.nextIO = 0

    def isIdleTask(self):
        return False
# Task
