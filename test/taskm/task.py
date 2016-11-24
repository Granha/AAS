from iom.io import IO
from iom.io_list import IOList
from taskm.task import Task

import unittest

class TestTask(unittest.TestCase):

    def testInteralState(self):        
        io1 = IO(6,2)
        io2 = IO(8,3)
        ioList = IOList([io1, io2])

        name = 'Task 1'
        priority = 1
        creationTime = 0
        totalCpuTime = 10
        
        task = Task(name=name, priority=priority,
                    creationTime=creationTime,
                    totalCpuTime=totalCpuTime, ioList=ioList)

        #######################
        #   Test constructor
        #######################
        self.assertEqual(task.getName(), name)
        self.assertEqual(task.getPriority(), priority)
        self.assertEqual(task.getCreationTime(), creationTime)
        self.assertEqual(task.getTotalCpuTime(), totalCpuTime)
        self.assertEqual(task.getIOList(), ioList)
        
        ##########################
        #   Check Deafult Values
        ##########################
        self.assertEqual(task.getUsedCpuTime(), 0)
        self.assertEqual(task.getNice(), 0)
        self.assertEqual(task.getRecentCpu(), 0)
        self.assertEqual(task.getTimesBlocked(), 0)
        self.assertEqual(task.getAvgBlocking(), 0)
        self.assertEqual(task.getAvgReadyWait(), 0)

        self.assertTrue(task.stillHasIO())
        self.assertEqual(task.getNextIO(), io1)
        self.assertEqual(task.popNextIO(), io1)
        self.assertTrue(task.stillHasIO())
        self.assertEqual(task.getNextIO(), io2)
        self.assertEqual(task.popNextIO(), io2)
        self.assertFalse(task.stillHasIO())
        self.assertEqual(task.popNextIO(), None)
        self.assertFalse(task.isInIO())        
        self.assertFalse(task.isIdleTask())
        
        task.reset()
        #######################################
        #  After reset should revisit all IOs
        #######################################
        self.assertTrue(task.stillHasIO())
        self.assertEqual(task.getNextIO(), io1)
        self.assertEqual(task.popNextIO(), io1)
        self.assertTrue(task.stillHasIO())
        self.assertEqual(task.getNextIO(), io2)
        self.assertEqual(task.popNextIO(), io2)
        self.assertFalse(task.stillHasIO())
        self.assertEqual(task.popNextIO(), None)        

        amount = 13
        usedCpuTime = task.getUsedCpuTime()
        for i in xrange(5):
            task.incUsedCpuTime(amount)
            usedCpuTime += amount
            self.assertEqual(task.getUsedCpuTime(), usedCpuTime)

        ######################
        # usedCpu increment
        ######################
        usedCpuTime = 0
        task.setUsedCpuTime(usedCpuTime)
        self.assertEqual(task.getUsedCpuTime(), usedCpuTime)        
        task.incUsedCpuTime(1)
        usedCpuTime += 1
        self.assertEqual(task.getUsedCpuTime(), usedCpuTime)
        task.incUsedCpuTime(1)
        usedCpuTime += 1
        self.assertEqual(task.getUsedCpuTime(), usedCpuTime)

        ######################
        # recentCpu increment
        ######################        
        recentCpu = 0
        task.setRecentCpu(recentCpu)
        self.assertEqual(task.getRecentCpu(), recentCpu)
        task.incRecentCpu()
        recentCpu += 1
        self.assertEqual(task.getRecentCpu(), recentCpu)
        task.incRecentCpu()
        recentCpu += 1
        self.assertEqual(task.getRecentCpu(), recentCpu)

        ###########################
        # timesScheduled increment
        ###########################
        timesScheduled = 0
        task.setTimesScheduled(timesScheduled)
        self.assertEqual(task.getTimesScheduled(), timesScheduled)
        task.incTimesScheduled()
        timesScheduled += 1
        self.assertEqual(task.getTimesScheduled(), timesScheduled)
        task.incTimesScheduled()
        timesScheduled += 1
        self.assertEqual(task.getTimesScheduled(), timesScheduled)

        priority = 10
        task.setPriority(priority)
        self.assertEqual(task.getPriority(), priority)

        recentCpu = 15
        task.setRecentCpu(recentCpu)
        self.assertEqual(task.getRecentCpu(), recentCpu)

        nice = -8
        task.setNice(nice)
        self.assertEqual(task.getNice(), nice)

        usedCpuTime = 7
        task.setUsedCpuTime(usedCpuTime)
        self.assertEqual(task.getUsedCpuTime(), usedCpuTime)

        self.assertEqual(task.getRemainingCpuTime(),
                         task.getTotalCpuTime() - usedCpuTime)

        timesBlocked = 3
        task.setTimesBlocked(timesBlocked)
        self.assertEqual(task.getTimesBlocked(), timesBlocked)

        totalReadyWait = 32
        task.setTotalReadyWait(totalReadyWait)
        self.assertEqual(task.getTotalReadyWait(), totalReadyWait)

        timesScheduled = 4
        task.setTimesScheduled(timesScheduled)
        self.assertEqual(task.getTimesScheduled(), timesScheduled)

        self.assertEqual(task.getAvgBlocking(),
                         float(timesBlocked)/usedCpuTime)

        self.assertTrue(abs(task.getAvgReadyWait()-
                            float(totalReadyWait)/timesScheduled) < 1e-3)

        amount = 5
        task.incTotalReadyWait(amount)
        totalReadyWait += amount
        self.assertEqual(task.getTotalReadyWait(), totalReadyWait)

        self.assertTrue(abs(task.getAvgReadyWait()-
                            float(totalReadyWait)/timesScheduled) < 1e-3)
    # testInteralState

# TestTask

if __name__ == '__main__':
    unittest.main()
