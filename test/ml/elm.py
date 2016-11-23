from ml.elm import ELM

import numpy as np

def computeOutput(inData, funcVec):
    (l, n) = np.size(inData)
    k = len(funcVec)

    assert l > 0 and n > 0 and k > 0

    outM = np.zeros((l,k))

    for i in xrange(l):
        data = inData[i,:]

        [funcVec[kk](data) for kk in xrange(k) ]

    return outM
            

if __name__ == '__main__':

    elm = ELM()

    inTrainData = elm.randData(400, 3)
    inTestData = elm.randData(400, 3)

    func1 = lambda x,y,z: x**2 + 2*y + z**3
    func2 = lambda x,y,z: x+10*y + z
    func3 = lambda x,y,z: x**2+ y**2 + z**2

    funcVec = [ func1, func2, func2 ]

    outTrainData = computeOutput(inTrainData, funcVec)
    outTestData  = computeOutput(inTestData, funcVec)


