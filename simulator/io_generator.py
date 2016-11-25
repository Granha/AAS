from iom.io import IO

import random
import numpy as np
import logging

class IOGenerator:
    
    def __init__(self, rate, total_time, mean_io_time, sd_io_time,
                 time_unit):
            self.rate = rate
            self.total_time= total_time
            self.mean_io_time = mean_io_time
            self.sd_io_time = sd_io_time
            self.time_unit = time_unit
    # __init__
            
    def generateIOEvent(self):
        list_io =[]
        IOOffset = round(random.expovariate(self.rate)*self.time_unit)
        logging.basicConfig(filename='example.log',level=logging.DEBUG)
        i= 0
        
        while(IOOffset <= self.total_time):
           IOcompletiontime = np.abs(round(np.random.normal(self.mean_io_time,
                                                            self.sd_io_time)*self.time_unit))
           iotask = IO(IOOffset, IOcompletiontime)
           
           logging.info('IO task'+str(i)+":Offset Time:"+ \
                        str(IOOffset)+":Completion Time:"+str(IOcompletiontime))
           
           list_io.append(iotask)
           i=i+1
           IOOffset = IOOffset + np.abs(round(random.expovariate(self.rate)*self.time_unit))
           
        return list_io
    # generateIOEvent
    
# IOGenerator
