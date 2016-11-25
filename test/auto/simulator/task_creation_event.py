import unittest
from simulator.task_creation_event import TaskCreationEvent
from taskm.task import Task 
from iom.io import IO
from iom.io_list import IOList

def dummyTask():
      ioList = IOList([IO(10,5),  IO(13,7)])
      t = Task("Task 2", 10, 5, 15, ioList)
      return t

class TestTaskCreationEvent(unittest.TestCase):
      
      def testgetTime(self):
          T = dummyTask()
          tc  =  TaskCreationEvent(10, dummyTask())
          self.assertEqual(tc.getTime( ),10)
     
      def testgetPriority(self):
          T= dummyTask()
          tc = TaskCreationEvent(9, dummyTask()) 
          self.assertEqual(tc.getPriority(),9)

      def testgetTask(self):
          T= dummyTask()
          tc = TaskCreationEvent(9, dummyTask())
          self.assertEqual(tc.getTask().getCreationTime(), 5)
          self.assertEqual(tc.getTask().getTotalCpuTime(),15)

if __name__ == '__main__':
    unittest.main()
