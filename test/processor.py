from simulator.processor import Processor
from iom.io import IO
from iom.io_list import IOList
from taskm.task import Task 
import unittest

def dummyTask():
      ioList = IOList([IO(10,5),  IO(13,7)])
      t = Task("Task 2", 10, 0, 15, ioList)
      return t

class TestProcessor(unittest.TestCase):
      
      def testrunTask(self):
          T = dummyTask()
          P = Processor()
          P.setTime(10)
          P.runTask(T)
          self.assertEqual(P.getRunningTask().getCreationTime(), 0 )
          self.assertEqual(P.getRunningTask().getTotalCpuTime(),15)
      
      def testsetTime(self):
          P= Processor()
          P.setTime(50)
          self.assertEqual(P.getTime(),50) 

      def testsetTicks(self):
          P= Processor()
          P.setTicks(10)
          self.assertEqual(P.getTicks(),10)
      
      def testPremptRunningtask(self):
          T = dummyTask()
          P = Processor()
          P.setTime(10)
          P.runTask(T)
          self.assertEqual(P.getRunningTask().getCreationTime(), 0 )
          self.assertEqual(P.getRunningTask().getTotalCpuTime(),15)
          P.setTime(20)
          P.premptRunningTask()
          self.assertEqual(P.runningTask, None)
          self.assertEqual(T.usedCpuTime, 10)

if __name__ == '__main__':
    unittest.main()
