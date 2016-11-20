# Abstract Scheduler. All concrete scheduler
# must comply to this interface.
class AbstractScheduler:

    def start():
        return None

    def timerIntr():
        return None

    def block(task):
        return None

    def unblock(task):
        return None

    def finishTask(task):
        return None

    def createTask(task):
        return None

    def setProcessor(processor):
        return None
    
# AbstractScheduler
