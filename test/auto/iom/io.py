from iom.io import IO
import unittest

#create dummyIO
def dummyIO( ):
      io = IO(4,10)
      return io

class TestWorkloadFeatures(unittest.TestCase):
      
      def testgetOffsetTime(self):
          iosample = dummyIO( )
          self.assertEqual(iosample.getOffsetTime(), 4)
      
      def testgetDuration(self):
          iosample = dummyIO( )
          self.assertEqual(iosample.getDuration(), 10)

if __name__ == '__main__':
    unittest.main()
