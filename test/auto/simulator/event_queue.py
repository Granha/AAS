from iom.io import IO
from iom.io_list import IOList
from taskm.task import Task
from simulator.workload import Workload
from simulator.event_queue import EventQueue
from simulator.io_start_event import IOStartEvent
import unittest


def dummyTasks( ):

        ioList1 = IOList([IO(10,5),  IO(13,7)])
        ioList2 = IOList([])

        # high priority IO instensive task
        t1 = Task("Task 1", 0, 3, 20, ioList1)

        # low priority CPU intensive task
        t2 = Task("Task 2", 10, 6, 15, ioList2)

        w = Workload([t1, t2])

        return w



class TestEventQueque(unittest.TestCase):
      
      def testgetSize(self):
          T = dummyTasks()
          q  =  EventQueue(T.getInitialEvents())
          self.assertEqual(q.getSize(),2)
     
      def testisEmpty(self):
          T = dummyTasks()
          q  =  EventQueue(T.getInitialEvents())
          self.assertFalse(q.isEmpty())
          q.extractMin()
          q.extractMin()
          self.assertTrue(q.isEmpty())

      def testgetMin(self):
          T = dummyTasks()
          q  =  EventQueue(T.getInitialEvents())
          m = q.getMin()
          self.assertEqual(m.getPriority(),3)

      def testaddEvent(self):
          T = dummyTasks()
          q  =  EventQueue(T.getInitialEvents())
          io = IO(10,5)
          io_start = IOStartEvent(5,io,5)
          q.addEvent(io_start)
          self.assertEqual(q.getSize(),3)
          q.extractMin()
          self.assertEqual(q.getMin().getPriority(),5)

if __name__ == '__main__':
    unittest.main()
