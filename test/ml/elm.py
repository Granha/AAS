from ml.elm import ELM

import numpy as np
import unittest

ERR_THRESHOLD = 1e-10

def computeOutput(inData, funcVec):
    (l, n) = np.shape(inData)
    k = len(funcVec)

    assert l > 0 and n > 0 and k > 0

    outM = np.zeros((l,k))

    for i in xrange(l):
        data = inData[i,:]

        outM[i,:] = [funcVec[kk](data[0], data[1], data[2]) \
                     for kk in xrange(k) ]

    return outM
# computeOutput

class TestELM(unittest.TestCase):

    def testTrain1(self):
        elm = ELM()

        inTrainData = elm.randData(400, 3)
        inTestData = elm.randData(200, 3)

        # test whether neural network can
        # learn the functions
        func1 = lambda x,y,z: x**2 + 2*y + z**3
        func2 = lambda x,y,z: x+10*y + z
        func3 = lambda x,y,z: x**2+ y**2 + z**2

        funcVec = [ func1, func2, func2 ]

        outTrainData = computeOutput(inTrainData, funcVec)
        outTestData  = computeOutput(inTestData, funcVec)

        elm.train(inTrainData, outTrainData)
        mse = elm.test(inTestData, outTestData)
        
        # fails if the mean squared error
        # is too large
        assert mse < ERR_THRESHOLD
    # testTrain


    def testTrain2(self):
        elm = ELM()

        # very large training set
        inTrainData = elm.randData(1000, 3)
        inTestData = elm.randData(500, 3)

        # test whether neural network can
        # learn a single complex function
        func1 = lambda x,y,z: np.sqrt(np.sin(x)**2+ np.tanh(y**2 + z**2))

        funcVec = [ func1 ]

        outTrainData = computeOutput(inTrainData, funcVec)
        outTestData  = computeOutput(inTestData, funcVec)

        elm.train(inTrainData, outTrainData)
        mse = elm.test(inTestData, outTestData)
        
        # fails if the mean squared error
        # is too large
        assert mse < ERR_THRESHOLD
    # testTrain    

# TestELM

if __name__ == '__main__':
    unittest.main()
