#!/usr/bin/env python

# A script that finds the optimal bitonic tour given n points in the Euclidean
# plane. It utilizes dynamic programming and runs in O(n^2) time.
#
# Zafer Cesur

import numpy as np

def min_bitonic_tour(pts):
    """
    Require: A list containing coordinates of points in the Euclidean plane.
             We assume that no two points share the same x coordinate.

    Ensure: A list containing the edges of the optimal bitonic tour.
            Note that the edges are represented by 2 indices where the index
            corresponds to the rank of the point in the unique left-to-right
            ordering of points.
    """
    # Euclidean distance
    d = lambda x,y: ((pts[x][0]-pts[y][0])**2+(pts[x][1]-pts[y][1])**2)**(1./2)
    
    # DP tables
    D = np.zeros((len(pts), len(pts)))
    N = np.zeros((len(pts), len(pts)), dtype='int8')

    # Given D(i,j), computes D(i,j)+d(j,i+1) and stores it in N(i+1,i).
    # In other words, given a tree defined by the leaf nodes i and j,
    # computes the cost of the tree given by the leaf nodes i and i+1.
    def update_min_node(i,j):
        cur_cost = D[i,j]+d(j,i+1)
        
        if N[i+1,i] is not 0:
            best_min_node = N[i+1,i]
            best_cost = D[i,best_min_node]+d(best_min_node,i+1)

            if cur_cost < best_cost:
                N[i+1,i] = j
        else:
            N[i+1,i] = j

    # Fill out the tables
    for j in xrange(len(pts)):
        for i in xrange(j+1,len(pts)):
            if (i,j) is (1,0):
                D[i,j] = d(i,j)
            elif i is not j+1:
                D[i,j] = D[i-1,j] + d(i, i-1)
            else:
                min_node = N[i,j]
                D[i,j] = D[i-1,min_node] + d(min_node,i)

            if i+1<len(pts):
                update_min_node(i,j)

    # Construct the tour using the tables
    tour = [(len(pts)-1,len(pts)-2)]
    cur_leaves = (len(pts)-1,len(pts)-2)
    while cur_leaves != (0,0):
        if cur_leaves[0] == cur_leaves[1]+1:
            new_leaf = N[cur_leaves]
        else:
            new_leaf = cur_leaves[0]-1
        tour.append((cur_leaves[0],new_leaf))
        cur_leaves = (cur_leaves[1],new_leaf)

    return tour

def main():
    pts = [(0,0),(10,5),(12,-5),(22,0)]
    print min_bitonic_tour(pts)

if __name__ == '__main__':
    main()
