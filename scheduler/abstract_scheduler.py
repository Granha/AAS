from ml.euler import Euler
from taskm.idle_task import IdleTask

# Abstract Scheduler. All concrete scheduler
# must comply to this interface.
class AbstractScheduler:

    def __init__(self, timeSlice):
        # callbacks to be executed at each
        # timer interrupt
        self.callbacks = []

        # list containing all tasks
        self.tasks = []

        # scheduler parameters by convetion alpha[-1] is the time
        # slice
        self.alpha = [timeSlice]

        # processor on which tasks are going to be scheduled
        self.processor = None

        self.idleTask = IdleTask()

        self.euler = Euler(self)
    # __init__

    def start(self):
        """
        Start scheduler execution.
        """
        raise NotImplementedError

    def timerIntr(self, ticks):
        self.processCallbacks(ticks)
        self._timerIntr(ticks)

    def _timerIntr(self, ticks):
        raise NotImplementedError

    def block(self, task):
        task.block()

        self._block(task)

    def _block(self, task):
        raise NotImplementedError        

    def unblock(self, task):
        curTime = self.processor.getTime()

        task.unblock(curTime)

        self._unblock(task)

    def _unblock(self, task):
        raise NotImplementedError
    
    def createTask(self, task):
        self.tasks.append(task)
        self._createTask(task)

    def _createTask(self, task):
        raise NotImplementedError

    def finishTask(self, task):
        assert task in self.tasks
        self.tasks.remove(task)
        
        self._finishTask(task)

    def _finishTask(self, task):
        raise NotImplementedError

    def setProcessor(self, processor):
        self.processor = processor

    def getTimeSlice(self):
        # convention that the last parameter
        # is always the time slice
        return self.alpha[-1]

    def getAlpha(self):
        return self.alpha

    def setAlpha(self, alpha):
        self.alpha = alpha

    def getAlphaRange(self):
        # this is scheduler dependent
        raise NotImplementedError        

    def registerTimerCallBack(self, callback):
        assert callback not in self.callbacks

        self.callbacks.append(callback)

    def processCallbacks(self, ticks):

        for callback in self.callbacks:
            callback(ticks)
    # processCallbacks

    def getAllTaks(self):
        return self.tasks

    def getCurTime(self):
        return self.processor.getTime()
# AbstractScheduler
