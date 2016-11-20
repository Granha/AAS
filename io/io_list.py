# List of single IO operations
class IOList:

    def __init__(self, ioVec):
        ioVec.sort(key=lambda io: io.getStartTime())
        
        self.ios = ioVec

    def __iter__(self):
        return self.ios.__iter__()

    def get(self, i):
        
        if i < len(self.ios):
            return self.ios[i]

        return None
        
# IOList
