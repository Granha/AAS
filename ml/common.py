###########################################################
#            Modulo with utility functions
###########################################################

import matplotlib.colors
import matplotlib.pyplot as plt
import numpy as np
import random

# l_2 distance squared between two points
# the last entry contains a pointer to
# the original data
def pointDist(a,b):
    diff = np.subtract(a, b)

    return np.linalg.norm(diff)**2
# pointDist

def pointDim(points):
    assert len(points) > 0

    return len(points[0])
# points

# from a list of points return the projections on
# the i-coordinate
def proj(i, points):
    return [ p[i] for p in points ]

def getRGBList(k):
    start = 10
    end = 254

    inc = (end-start)/k

    assert inc > 0

    iRange = range(start, end+1, inc)
    
    colorSpace = [ (r/255.0,g/255.0,b/255.0) for r in iRange\
                   for g in iRange\
                   for b in iRange ]
                
    samples = random.sample(colorSpace, k)

    return samples
# getRGBList

def getClusters(points, gamma):
    k = len(gamma)
    assert k > 0
    
    clusters = [None]*k
    
    # group points in clusters
    for i in xrange(k):
        clusters[i] = [p for p,g in
                      zip(points,gamma) if g == i]

    return clusters
# getClusters
                                      
def clusterFigure(title, points, gamma, centroids):
    k = len(centroids)
                   
    d = pointDim(points)
    
    # TODO: dimensionality reduction
    
    figCluster = plt.figure()
    figCluster.suptitle(title, fontweight='bold')
    
    ax = figCluster.add_subplot(111)
                   
    ax.set_xlabel('x coordinate')
    ax.set_ylabel('y coordinate')
                   
    clusters = getClusters(points, gamma)
        
    colors = getRGBList(k)
    
    # mark centroids
    for i in xrange(k):
        ax.plot(proj(0, clusters[i]), proj(1, clusters[i]),
                'o', color=colors[i])
        ax.plot(proj(0, [centroids[i]]), proj(1, [centroids[i]]),
                's', color=(0,0,0))

    return figCluster, ax
# clusterFigure

def closestVecEl(x, vec):
    diff = [ np.abs(x-el) for el in vec ]

    i = np.argmin(diff)

    return vec[i]
# closestVecEl

    
