from iom.io_list import IOList
from iom.io import IO
import unittest

#create dummyIOList
def dummyIOList( ):
      io1 = IO(4,10)
      io2 = IO(2,10)
      io3 = IO(8,30)
      io4 = IO(5,40)
      io5 = IO(7,19)
      return [io1, io2, io3, io4, io5]

class TestWorkloadFeatures(unittest.TestCase):
      
      def testget(self):
          iolistsample = IOList(dummyIOList( ))
          self.assertEqual(iolistsample.get(0).getOffsetTime(), 2) 
          self.assertEqual(iolistsample.get(1).getOffsetTime(), 4)
          self.assertEqual(iolistsample.get(2).getOffsetTime(), 5)
          self.assertEqual(iolistsample.get(3).getOffsetTime(), 7)
          self.assertEqual(iolistsample.get(4).getOffsetTime(), 8)

if __name__ == '__main__':
    unittest.main()
