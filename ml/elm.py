# Extreme Learning Machine Neural Network
# with single output

import numpy as np

class ELM:    

    def __init__(self):
        """
        Extreme Learning Machine Constructor

        Args:
             n: number of inputs (without constant)
             k: number of neurons in the output layer
             m: number of neurons in the first layer
             actFunc: activation function of first layer neurons
        """
        self.n = None
        self.k = None
        self.m = None

        # first layer activation function
        self.activationFunc = None
        
        # first layer neuron coefficients
        self.inputLayer = None

        # second layer neuron coefficients
        self.outputLayer = None


    def initELM(self, n=0, k=0, m=200, actFunc=np.tanh):
        self.n = n
        self.k = k
        self.m = m

        # first layer activation function
        self.activationFunc = activationFunc
        
        # first layer neuron coefficients
        self.inputLayer = self.randData(m, n+1)

        # second layer neuron coefficients
        self.outputLayer = None    


    def randData(self, l, d):
        """
        Initialize a l d-dimension unit vector
        in a matrix lxd. It is used to create
        the feature reservoir.
        
        Args:
            l: number of vectors
            d: dimension of each unit vector

        Returns:
            lxd matrix
        """
        if l <= 0 or d <=0:
            return None
        
        M = np.zeros((l,d))

        for i in xrange(l):
            
            # generate random unit vector in R^d
            vec = [np.random.normal(0,1) for j in xrange(d)]
            norm = np.linalg.norm(vec)
            vec = vec / norm

            M[i,:] = vec

        return M
    # randData

    def processSingleInputLayer(self, data):
        """
        From a single input compute the output of the neurons
        in the first layer. 
        """

        assert self.inputLayer is not None

        outVec = self.activationFunc(np.matmul(self.inputLayer, data))

        return outVec
    # processSingleInputLayer
        

    def processInputLayer(self, inData):
        """
        From a list of inputs compute the outputs of the neurons
        in the first layer.
        """
        (l,n) = np.size(inData)

        outM = np.zeros((l,self.m))

        for i in xrange(l):
            outM[i,:] = self.processSingleInputLayer(inData[i,:])

        return outM
    # processInputLayer

    def train(self, inData, outData):
        (l,n) = np.size(inData)
        (p,k) = np.size(outData)

        assert l == p

        self.initELM(n, k)

        self.outputLayer = np.zeros(k, m+1)

        # add constant input
        inData = np.column_stack([np.ones((l,1)), inData])

        outInputLayer = self.processInputLayer(inData)

        # add constant input
        outInputLayer = np.column_stack([np.ones((l,1)),
                                         outInputLayer])

        # use least squares to compute the best in l_2
        # coefficients for the output layer
        for kk in xrange(k):
            self.outInputLayer[kk,:] = np.linalg.lstsq(outInputLayer,
                                                       outData[:,kk])
    # train

    def processSingle(self, data):

        assert self.outputLayer is not None

        outInputLayer = self.processSingleInputLayer(data)

        # add constant input
        outInputLayer = np.column_stack([np.ones((l,1)),
                                         outInputLayer])

        out = np.dot(self.outputLayer, outInputLayer)

        return out
    # processSingle

    def process(self, inData):
        (l,n) = np.size(inData)

        outM = np.zeros((l,self.k))

        for i in xrange(l):
            outM[i,:] = self.processSingle(inData[i,:])
            
        return outM
    # process

    def test(self, inData, outData):
        (l,n) = np.size(inData)
        (p,k) = np.size(outData)

        assert l == p
        assert l > 0

        outM = self.process(inData)

        total = 0.0

        for i in xrange(l):
            total += (np.linalg.norm(outM[i,:] - outData[i,:]))**2
                    
        # mean square error
        mse = total/ l

        return mse
    # test

# ELM
