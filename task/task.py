class Task:

    def __init__(self, priority, createTime, totalCpuTime, ioList):
        self.priority = priority
        self.usedCpuTime = 0
        self.createTime = createTime
        self.totalCpuTime = totalCpuTime
        self.ioList = ioList    
        
# Task
