#!/usr/bin/env python

# A script that reads in a file and a integer that determines the maximum
# line length, and then pretty-prints the file by distributing the words
# to lines as evenly as possible. It utilizes dynamic programming and
# runs in O(n^3) time.
#
# Zafer Cesur

import sys
import numpy as np

def justify(words, L):
    """
    Require: An list containing words and an integer L that determines the
             maximum length.

    Ensure: A partition of words
    """
    # Compute cumulative sum of word lengths
    csum = np.cumsum([len(w) for w in words]).tolist()
    csum.insert(0,0)

    # Define a function that computes the length of a line consisting
    # of words[i,...,j]
    line_len = lambda i,j: csum[j+1]-csum[i]+(j-i)

    # Allocate dynamic programming tables
    min_slack = np.zeros((len(words), len(words)))
    split_pt = np.zeros((len(words), len(words)))

    # For each 0<=i<=j<=n-1, compute the length of a line consisting of
    # words[i,...,j] and insert the indices into a list which is sorted 
    # at the end
    h = sorted([(line_len(i,j), (i,j)) \
    for i in xrange(len(words)) \
    for j in xrange(i, len(words))])

    # Fill out the tables based on recursive definition
    for idx in xrange(len(h)):
        l, (i,j) = h[idx]
        if l <= L:
            min_slack[i, j] = (L-l)**2
            split_pt[i, j] = -1
        else:
            min_slack[i, j] = float("inf")
            for k in xrange(i, j):
                curPartition = min_slack[i, k] + min_slack[k+1, j]
                if curPartition < min_slack[i, j]:
                    min_slack[i, j] = curPartition
                    split_pt[i, j] = k

    # Recursively retrieves the split points for words[i,...,j] from split_pt
    def split(i,j):
        k = int(split_pt[i,j])
        if k < 0:
            return [(i,j+1)] # We return j+1 since array slicing is exclusive
        
        return split(i,k) + split(k+1,j)

    # Return an array containing the lines
    return [words[slice(*idx)] for idx in split(0, len(words)-1)]

def main():
    # Input
    L = int(sys.argv[1])
    fin = open(sys.argv[2])
    words = fin.read().split()

    assert all(len(w) < L for w in words), \
    "The length of one of the words in your text exceeds the maximum line length."
   
    lines = justify(words, L)
    for i in xrange(len(lines)):
        print ' '.join(lines[i])

if __name__ == '__main__':
    main()
