from iom.io import IO
from iom.io_list import IOList
from taskm.task import Task
from workload import Workload
from io_generator import IOGenerator
import numpy as np
import random
import logging

class WorkloadGenerator:

    def __init__(self, num_jobs, rate_jobs, rate_io, mean_job_time,
                 mean_io_time, sd_job_time, sd_io_time, time_unit):
        self.state = None
        self.num_jobs = num_jobs
        self.rate_jobs = rate_jobs
        self.rate_io = rate_io
        self.mean_job_time = mean_job_time
        self.mean_io_time = mean_io_time
        self.sd_job_time = sd_job_time
        self.sd_io_time = sd_io_time
        self.time_unit = time_unit
        self.work_load_list = None
    # __init__

    # dummy generator for initial tests
    @staticmethod    
    def dummyGen():

        ioList1 = IOList([IO(10,5),  IO(13,7)])
        ioList2 = IOList([])

        # high priority IO instensive task
        t1 = Task("Task 1", 0, 3, 20, ioList1)

        # low priority CPU intensive task
        t2 = Task("Task 2", 10, 0, 15, ioList2)

        w = Workload([t1, t2])

        return w
    # dummyGen
   
    def generateWorkload(self):
       W =[]
       logging.basicConfig(filename='example.log',level=logging.DEBUG)
       creation_Time = 0
       i=0
       TotalCPUTime = np.random.normal(self.mean_job_time,self.sd_job_time)
       TotalCPUTime = round(TotalCPUTime*self.time_unit) 
       logging.info('Task'+str(i)+":Creation Time:"+str(creation_Time)+":Total CPU time:"+str(TotalCPUTime))
       IO = IOGenerator( self.rate_io, TotalCPUTime, self.mean_io_time, self.sd_io_time, self.time_unit)
       iolist = IOList( IO.generateIOEvent())
       T = Task("Task 0", 0, np.abs(creation_Time), np.abs(TotalCPUTime), iolist)
       W.append(T)

       for i in xrange(self.num_jobs):
          creation_Time = round(random.expovariate(self.rate_jobs)*self.time_unit)+W[-1].creationTime
          TotalCPUTime =  np.random.normal(self.mean_job_time,self.sd_job_time)
          TotalCPUTime = round(TotalCPUTime*self.time_unit)
          logging.info('Task'+str(i)+":Creation Time:"+str(creation_Time)+":Total CPU time:"+str(TotalCPUTime))
          IO = IOGenerator( self.rate_io, TotalCPUTime, self.mean_io_time, self.sd_io_time, self.time_unit)
          iolist = IOList( IO.generateIOEvent())
          T = Task("Task "+str(i), 0, np.abs(creation_Time), np.abs(TotalCPUTime), iolist)
          W.append(T)
       self.work_load_list = W
       w =Workload(W)
       return w
   # generateWorkload

# WorkloadGenerator
