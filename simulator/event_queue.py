import heapq

class EventQueue:

    def __init__(self, events):
        heapq.heapify(events)
        self.queue = events

    def getSize(self):
        return len(self.queue)

    def isEmpty(self):
        
        if len(self.queue) == 0:
            return True
        
        return False

    def addEvent(self, event):
        heapq.heappush(self.queue, (event.getPriority(), event))

    def getMin(self):
        if len(self.queue) == 0:
            return None

        return self.queue[0][1]        

    def extractMin(self):
        return heapq.heappop(self.queue)[1]

# EventQueue
