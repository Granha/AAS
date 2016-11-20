class EventQueue:

    def __init__(self, events):
        self.queue = heapq.heapify(creationEvents)

    def getSize(self):
        return len(self.queue)

    def isEmpty(self):
        
        if len(self.queue) == 0:
            return True
        
        return False

    def addEvent(self, event):
        heapq.heappush(self.queue, (event.getPriority(), event))

    def extractMin(self):
        return heapq.heappop(self.queue)

    def getMin(self):
        if len(self.queue) == 0:
            return None

        return self.queue[0]

# EventQueue
