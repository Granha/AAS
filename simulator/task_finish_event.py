class TaskFinishEvent:

    def __init__(self, time, task):
        self.time = time
        self.task = task

    def getTime(self):
        return self.time

    def getTask(self):
        return self.task

    def getPriority(self):
        return self.time

# TaskFinishEvent
