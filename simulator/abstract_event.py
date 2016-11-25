# Abstract Evetn. All concrete events
# must comply to this interface.
class AbstractEvent:

    def getTime():
        raise NotImplementedError

    def getPriority():
        raise NotImplementedError
    
# AbstractEvent
