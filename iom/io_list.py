# List of single IO operations
class IOList:

    # IOs are sorted by offset time
    def __init__(self, ioVec):
        ioVec.sort(key=lambda io: io.getOffsetTime())
        
        self.ios = ioVec

    def __iter__(self):
        return self.ios.__iter__()

    def get(self, i):        
        if i < len(self.ios):
            return self.ios[i]

        return None

    def prettyPrint(self, start=0):
        print "-"*5 + "[IOList]"+ "-"*5
        ios = self.ios[start:]
        for io in ios:
            io.prettyPrint()
        print "-"*15
# IOList
