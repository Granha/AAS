from metrics.metric import Metric
from iom.io import IO
from iom.io_list import IOList
from task.task import Task
import unittest
import math

ERR_THRESHOLD = 1e-3

def isclose(a, b, rel_tol=ERR_THRESHOLD, abs_tol=0.0):
         return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

class TestMetricMethods(unittest.TestCase):

      def test_objFunction(self):
         ioList1 = IOList([IO(10,5),  IO(13,7)])
         ioList2 = IOList([IO(1,3),IO(2,6), IO(5,8), IO(6,8)])
         t1 = Task("Task 1", 0, 3, 20, ioList1)
         t2 = Task("Task 1", 0, 5, 40, ioList2)
         t1.setUsedCpuTime(14)
         t1.setTimesBlocked(2)
         t1.setTotalReadyWait(4)
         t1.setTimesScheduled(2)
         t2.setUsedCpuTime(7)
         t2.setTimesBlocked(4)
         t2.setTotalReadyWait(4)
         t2.setTimesScheduled(2)
         tasks = [t1, t2]
         self.assertTrue(isclose(11.1428, Metric.objFunction(tasks, 10)))
       
if __name__ == '__main__':
    unittest.main()        
      




