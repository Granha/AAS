###########################################################
# Modulo containing the k-Means, k-Menas++ algorithms and
# related functions.
###########################################################
from common import pointDist

import numpy as np
import random
import sys

# Given a list of points and centroids
# for each point point[i] assign the closest
# centroid using point_dist function
# store thi value in gamma[i].
def clusterAssignment(centroids, points):
    gamma = [None]*len(points)

    for i in range(0,len(points)):
        p = points[i]
        dist = [pointDist(p, centroid) for centroid in centroids]

        closest = np.argmin(dist)

        # assign cluster corresponding to closest centroid
        gamma[i] = closest
    
    return gamma
# clusterAssignment

# Given the assigment gamma of points
# to cluster determine the centroids
# by computing the avarage point of
# the points in the cluster.
def computeCentroids(k, points, gamma):
    assert len(points) > 0

    d = len(points[0])

    centroids = [None]*k

    for i in range(0,k):
        s = list(np.zeros((1,d)))
        t = 0

        for j in range(0,len(points)):

            if gamma[j] == i:
                p = points[j]
                s = np.add(p, s)
                t += 1


        assert t > 0
        m = np.divide(s, float(t))

        # centroids have no meta-information
        m = tuple(np.ndarray.tolist(m)[0])
        centroids[i] = m

    return centroids
# computeCentroids

# distortion function for the cluster
def J_avg_2(centroids, points, gamma):    
    return sum([ pointDist(points[i], centroids[gamma[i]])
                 for i in range(0,len(points))])
# J_avg_2

# Initialization of the k-means++ Algorithm
# We select centroids in a probabilistic manner
# favoring points that are far from the currently
# chosen centroids.
def kmeansppInit(k, origPoints):

    points = origPoints[:]

    centroids = []
    
    # choose the first centroid uniformly at random
    centroids.append(random.sample(points,1)[0])

    points.remove(centroids[0])
    
    for i in range(1,k):

        prob = [None]*len(points)
        for j in range(0,len(points)):
            # compute the mininum distance from j-th point to the
            # centroids
            prob[j] = min([pointDist(points[j],m) for m in centroids])

        t = sum(prob)
        # normalize probability
        prob = map(lambda x: x/t, prob)
    
        # choose a position drawn from prob
        pos = np.random.choice(range(0,len(prob)), p=prob)

        centroids.append(points[pos])
        points.remove(centroids[i])

    return centroids
# kmeansppInit

def kmeansAux(k, points, EPS, flag=True):
    # Recall that the k-means and k-means++ only differs
    # in the initialization
    if not flag:
        # choose k centroids uniformly at random
        centroids = random.sample(points,k)
    else:
        centroids = kmeansppInit(k,points)

    gamma = clusterAssignment(centroids,points)

    curDist = J_avg_2(centroids, points, gamma)
    prevDist = None

    firstTime = True

    distortion = [ curDist ]
    
    while firstTime or abs(prevDist - curDist) > EPS:
        firstTime = False
        
        centroids = computeCentroids(k, points, gamma)
        gamma = clusterAssignment(centroids,points)

        prevDist = curDist
        curDist = J_avg_2(centroids, points, gamma)
        distortion.append(curDist)

    return centroids, gamma, distortion
# kmeans

def kmeans(k, points, EPS, flag=True, robustness=3):
    """
    k-means++ and k-means Algorithms (default is k-means++)

    Args:  
        k: number of clusters points, list of 2-tupples
           corresponding to point in R^2 
        EPS: stopping codition correspoding to the minimum 
             distortion reduction
        flag: Boolean if False runs K-Means if True runs K-Means++
        robustness: number of times to run K-Means/K-Means++ so that the
                    least distortion solution is returned

    Returns:  (centroids, gamma, distortion) tuple
          centroids: list of k centroids
          gamma: a list such that gamma[i] contains
                the cluster assignment for point points[i]
          distortion: list of J_avg^2 for each cluster found
                      indexed by iteration
    """
    centroids, gamma, distortion = kmeansAux(k, points, EPS, flag)

    for i in xrange(robustness-1):

        c, g, d = kmeansAux(k, points, EPS, flag)

        if d < distortion:
            centroids, gamma, distortion = (c, g, d)

    return centroids, gamma, distortion
# kmeans
