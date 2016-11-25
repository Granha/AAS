import unittest
from simulator.timer_event import TimerEvent
from taskm.task import Task 
from iom.io import IO
from iom.io_list import IOList


class TestTimerEvent(unittest.TestCase):
      
      def testgetTime(self):
          tc  =  TimerEvent(10)
          self.assertEqual(tc.getTime( ),10)
     
      def testgetPriority(self):
          tc = TimerEvent(9) 
          self.assertEqual(tc.getPriority(),9)


if __name__ == '__main__':
    unittest.main()
