class Task:

    def __init__(self, name, priority, creationTime, totalCpuTime, ioList):
        self.name = name
        self.priority = priority
        self.usedCpuTime = 0
        self.creationTime = creationTime
        self.totalCpuTime = totalCpuTime
        self.ioList = ioList
        self.nextIO = 0
        self.boolIsInIO = False

    ######################
    #     getters
    ######################
    def getName(self):
        return self.name

    def getPriority(self):
        return priority

    def getUseCpuTime(self):
        return self.usedCpuTime

    def getCreationTime(self):
        return self.creationTime

    def getTotalCpuTime(self):
        return self.totalCpuTime

    def getIOList(self):
        return self.ioList

    def getRemainingCpuTime(self):
        return self.totalCpuTime - self.usedCpuTime

    def getNextIO(self):
        return self.ioList.get(self.nextIO)

    #######################

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
