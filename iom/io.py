# Single IO operation
class IO:

    # IO offset time is with respect to the
    # total cpu time. 
    def __init__(self, offsetTime, duration):
        self.offsetTime = offsetTime
        self.duration = duration

    def getOffsetTime(self):
        return self.offsetTime

    def getDuration(self):
        return self.duration
# IO
