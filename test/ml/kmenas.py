from scipy.stats import multivariate_normal
from ml.common import clusterFigure
from ml.common import proj
from ml.kmeans import kmeans
from ml.kmeans import J_avg_2

import matplotlib.pyplot as plt
import numpy as np
import random
import sys
import time
import unittest

RUN_KMEANS = False

# minimum progress
EPS = 1e-3

def genData(k, m, xMax=10, yMax=10):
    """
    Generates k clusters with m points in each
    in the R^2 space. The centroids are drawn
    from the rectangle [(0,0),(xMax,yMax)] uniformly
    at random.

    Args:
        k: number of clusters
        m: number of points per cluster
        xMax: x-limit for the upper-right corner of rectangle
        yMax: y-limit for the upper-right corner of rectangle

    Returns:
        (points, centroids) where
         points: the list of all generated points
         centroid: the list of all generated centroid        
    """

    centroids = [ (xMax*random.random(), yMax*random.random()) \
                  for kk in xrange(k) ]

    dist = min([np.linalg.norm(np.array(c1)-np.array(c2))\
                for c1 in centroids\
                for c2 in centroids if c1 != c2])

    sigma = dist/4

    cov = np.multiply(np.eye(2), sigma**2)

    points = []

    for kk in xrange(0,k):
        
        points += [ multivariate_normal.rvs(mean=centroids[kk], cov=cov) \
                    for i in xrange(m) ]

    points = [ tuple(np.ndarray.tolist(point)) for point in points ]

    return points, centroids
# genData

def manualTest():
    k = 5

    points, knownCentroids = genData(k, m=100)
    
    # run k-means
    if RUN_KMEANS:
        centroids, gamma, distortion = kmeans(k, points, EPS, flag=False)

        figCluster, ax = clusterFigure('k-means Colored Cluster',
                                    points, gamma, centroids)
        figCluster.show()
    
    # run k-means++
    centroids_pp, gamma_pp, distortion  = kmeans(k, points, EPS)
    
    figCluster, ax = clusterFigure('k-means++ Colored Cluster',
                                        points, gamma_pp, centroids_pp)
    figCluster.show()
        
    plt.show()
# manualTest


# avg min l2 discrepancy (theoretically this is a minimum matching
# problem)
def compDiscrepancy(centroids1, centroids2):

    assert len(centroids1) == len(centroids2)

    dist = []
    for c1 in centroids1:

        d = min([np.linalg.norm(np.array(c1)-np.array(c2))\
                for c2 in centroids2 ])

        dist.append(d)
        
    return sum(dist)/float(len(dist))
# discrepancy

class TestKmeans(unittest.TestCase):

    # note: this a probabilistic test
    def testKmeanspp(self):
        nRuns = 3

        DISCREPANCY_THRESHOLD = 0.5
        k = 4

        for i in xrange(nRuns):
            points, knownCentroids = genData(k, m=60)

            centroids_pp, gamma_pp, distortion  = kmeans(k, points, EPS)

            discrepancy = compDiscrepancy(centroids_pp, knownCentroids)

            if discrepancy < DISCREPANCY_THRESHOLD:
                return True

        self.fail("Cluster discrepancy was high in all %d runs" % nRuns)
    # kmeanspp 

# TestKmeans

if __name__ == '__main__':
    Manual = False
    if Manual:
        manualTest()
    else:        
        unittest.main()
