# Multi-level Feedback Queue
class MLFQ:

    def __init__(self, minPri, maxPri):
        self.queues = [ [] for i in xrange(Levels) ]
        self.minPri = minPri
        self.maxPri = maxPri        

    def enqueue(self, task):
        
        if task is None or \
           task.isIdleTask():
            return

        priority = task.getPriority()
        
        assert (self.minPri <= priority) and (priority <= self.maxPri)
        
        self.queues[priority].append(task)

    def isEmpty(self):
        total = sum([len(queue) for queue in self.queues ])

        if total >= 1:
            return False

        return True

    # lower priority values correspond to
    # higher priority
    def extractMin(self):

        for queue in self.queues:
            
            if len(queue) > 0:
                return queue.pop(0)

        return None

    def bestPriority(self):
        
        for i in xrange(self.queues):
            
            queue = self.queues[i]
            
            if len(queue) > 0:
                return i

        return None

    def listify(self):
        return [ task for queue in self.queue for task in queue]

    def empitfy(self):
        self.queues = [ [ ] for i in xrange(Levels) ]

    def addList(self, tasks):
        
        for task in tasks:
            self.enqueue(task)
        
# MLFQ
        
