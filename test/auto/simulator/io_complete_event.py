import unittest
from simulator.io_complete_event import IOCompleteEvent
from taskm.task import Task 
from iom.io import IO
from iom.io_list import IOList

def dummyTask():
      ioList = IOList([IO(10,5),  IO(13,7)])
      t = Task("Task 2", 10, 0, 15, ioList)
      return t

class TestIOCompleteevent(unittest.TestCase):
      
      def testgetTime(self):
          T = dummyTask()
          ioc  =  IOCompleteEvent(10, dummyTask())
          self.assertEqual(ioc.getTime( ),10)
     
      def testgetPriority(self):
          T= dummyTask()
          ioc = IOCompleteEvent(9, dummyTask()) 
          self.assertEqual(ioc.getPriority(),9)

      def testgetTask(self):
          T= dummyTask()
          ioc = IOCompleteEvent(9, dummyTask())
          self.assertEqual(ioc.getTask().getCreationTime(), 0)
          self.assertEqual(ioc.getTask().getTotalCpuTime(),15)

if __name__ == '__main__':
    unittest.main()
