import unittest
from simulator.io_start_event import IOStartEvent
from taskm.task import Task 
from iom.io import IO
from iom.io_list import IOList

def dummyTask():
      ioList = IOList([IO(10,5),  IO(13,7)])
      t = Task("Task 2", 10, 5, 15, ioList)
      return t

class TestIOStartevent(unittest.TestCase):
      
      def testgetTime(self):
          T = dummyTask()
          ioc  =  IOStartEvent(10, dummyTask(), 50)
          self.assertEqual(ioc.getTime( ),10)
     
      def testgetPriority(self):
          T= dummyTask()
          ioc = IOStartEvent(9, dummyTask(),60) 
          self.assertEqual(ioc.getPriority(),9)

      def testgetTask(self):
          T= dummyTask()
          ioc = IOStartEvent(9, dummyTask(), 50)
          self.assertEqual(ioc.getTask().getCreationTime(), 5)
          self.assertEqual(ioc.getTask().getTotalCpuTime(),15)

      def testgetDuration(self):
          T= dummyTask()
          ioc = IOStartEvent(9, dummyTask(), 50)
          self.assertEqual(ioc.getDuration(),50)

if __name__ == '__main__':
    unittest.main()
