from task_creation_event import TaskCreationEvent

class Workload:

    def __init__(self, tasks):
        # restore task state first
        for task in tasks:
            task.reset()

        self.tasks = tasks

    def getInitialEvents(self):
        events = []

        for task in self.tasks:
            creationTime = task.getCreationTime()
            creationEvent = TaskCreationEvent(creationTime, task)
            events.append((creationEvent.getPriority(), creationEvent))

        return events

# Workload
