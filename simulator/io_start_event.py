class IOStartEvent:

    def __init__(self, time, task, duration):
        self.time = time
        self.task = task
        self.duration = duration

    def getTime(self):
        return self.time

    def getTask(self):
        return self.task

    def getPriority(self):
        return self.time

    def getDuration(self):
        return self.duration

# IOStartEvent
