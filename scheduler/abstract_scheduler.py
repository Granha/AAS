# Abstract Scheduler. All concrete scheduler
# must comply to this interface.
class AbstractScheduler:

    def getTimeSlice():
        return None

    def timerIntr():
        return None

    def ioStart():
        return None

    def ioEnd():
        return None

# AbstractScheduler
