############################################
# Standard Idle Task used by schedulers to
# always have a runnable task
############################################

from task import Task

class IdleTask(Task):

    def __init__(self):
        Task.__init__(self, "Idle", -1, 0, -1, [])

    def isIdleTask(self):
        return True

# IdleTask
