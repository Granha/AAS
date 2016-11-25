import unittest
from simulator.task_finish_event import TaskFinishEvent
from taskm.task import Task 
from iom.io import IO
from iom.io_list import IOList

def dummyTask():
      ioList = IOList([IO(10,5),  IO(13,7)])
      t = Task("Task 2", 10, 6, 15, ioList)
      return t

class TestTaskFinishEvent(unittest.TestCase):
      
      def testgetTime(self):
          T = dummyTask()
          tf  =  TaskFinishEvent(10, dummyTask())
          self.assertEqual(tf.getTime( ),10)
     
      def testgetPriority(self):
          T= dummyTask()
          tf = TaskFinishEvent(9, dummyTask()) 
          self.assertEqual(tf.getPriority(),9)

      def testgetTask(self):
          T= dummyTask()
          tf = TaskFinishEvent(9, dummyTask())
          self.assertEqual(tf.getTask().getCreationTime(), 6)
          self.assertEqual(tf.getTask().getTotalCpuTime(),15)

if __name__ == '__main__':
    unittest.main()
