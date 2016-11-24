############################################
# Standard Idle Task used by schedulers to
# always have a runnable task
############################################

from task import Task

class IdleTask(Task):

    def __init__(self):
        Task.__init__(self, name="Idle", priority=-1, creationTime=0,
                      totalCpuTime=-1, ioList=[])

    def isIdleTask(self):
        return True

# IdleTask
