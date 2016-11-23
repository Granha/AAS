from io.io_list import IOList
from ml.workload_features import WorkloadFeatures
from task.task import Task

import numpy as np
import unittest

ERR_THRESHOLD = 1e-3

def dummyTasks():
    ioList1 = IOList([])
    ioList2 = IOList([])

    # high priority IO instensive task
    t1 = Task("Task 1", 0, 3, 20, ioList1)
    
    usedCpuT1 = 10
    timesBlockedT1 = 8
    timesScheduledT1 = 8

    t1.setUsedCpuTime(usedCpuT1)
    t1.setTimesBlocked(timesBlockedT1)
    t1.setTimesScheduled(timesScheduledT1)
        
    # low priority CPU intensive task
    t2 = Task("Task 2", 10, 0, 15, ioList2)

    usedCpuT2 = 9
    timesBlockedT2 = 3
    timesScheduledT2 = 4

    t2.setUsedCpuTime(usedCpuT2)
    t2.setTimesBlocked(timesBlockedT2)
    t2.setTimesScheduled(timesScheduledT2)

    return [t1, t2]
# dummyTasks

class TestWorkloadFeatures(unittest.TestCase):

    def testCreation(self):
        tasks = dummyTasks()

        wFeatures = WorkloadFeatures(tasks)

        features = wFeatures.getFeatures()

        # check length of feature vector
        self.assertTrue(len(features), WorkloadFeatures.NumMoment + 2)

        # check if features are normalized
        self.assertTrue(np.abs(np.linalg.norm(features)-1) < ERR_THRESHOLD)
    # testCreation

# TestWorkloadFeatures

if __name__ == '__main__':
    unittest.main()
