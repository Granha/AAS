# Abstract Scheduler. All concrete scheduler
# must comply to this interface.
class AbstractScheduler:

    def start(self):
        return None

    def timerIntr(self):
        return None

    def block(self, task):
        return None

    def unblock(self, task):
        return None

    def finishTask(self, task):
        return None

    def createTask(self, task):
        return None

    def setProcessor(self, processor):
        return None

    def getTimeSlice(self):
        return None

    def getAlpha(self):
        return None

    def setAlpha(self):
        return None

    def getAlphaRange(self):
        return None

# AbstractScheduler
