from simulator.task_creation_event import TaskCreationEvent

class Workload:

    def __init__(self, tasks):
        # restore task state first
        for tasks in tasks:
            task.reset()

        self.tasks = tasks

    def getCreationEvents(self):
        events = []

        for task in self.tasks:
            creationTime = task.getCreationTime()
            creationEvent = TaskCreationEvent(creationTime, task)
            events.append((creationTime.priority(), creationEvent))

        return events

# Workload
