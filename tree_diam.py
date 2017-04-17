#!/usr/bin/env python

# A script that finds the diameter of a tree, which is defined as the
# maximum length of a shortest path. It runs in O(n+m) time, i.e., in
# time linear in the number of vertices and edges, which is equivalent
# to O(n) for trees.
#
# The main idea used in the algorithm is that the longest path through
# any root node is found by taking 2 children that have the largest
# height. Also note that a tree's diameter is at least as big as its
# children's diameters, or equivalently, the proper sub-tree with the
# largest diameter is the lower bound for a tree's diameter.
#
# Zafer Cesur

class Tree(object):
    def __init__(self, value, children=[]):
        self.value = value
        self.children = children
    def __repr__(self, level=0):
        """Print the tree in level-order (when read from left to right)"""
        ret = "\t"*level+repr(self.value)+"\n"
        for child in self.children:
            ret += child.__repr__(level+1)
        return ret
    def isLeaf(self):
        return True if len(self.children) is 0 else False

def find_diam(node):
    """
    Require: A tree (equivalently a node)
    Ensure: A tuple that contains the height and the diameter of the tree
    """
    # Leaf node has height 0 and diameter 0
    if (node.isLeaf()):
        return 0, 0

    childHeights = []
    largestChildDiameter = 0

    # For each child node, recursively invoke the algorithm
    for child in node.children:
        height, diameter = find_diam(child)
        if (largestChildDiameter < diameter):
            largestChildDiameter = diameter
            
        childHeights.append(height)

    height = max(childHeights)+1
    childHeights.remove(height-1)

    if (len(childHeights) is not 0):
        secondHeight = max(childHeights)+1 
        longestPathThruThis = height+secondHeight
    else:
        longestPathThruThis = height

    diameter = largestChildDiameter \
    if largestChildDiameter>longestPathThruThis else longestPathThruThis

    return height, diameter

def main():
    tree1 = Tree('*', [Tree('*'),
                       Tree('*'),
                       Tree('*',
                            [Tree('*'),
                             Tree('*')])])
    
    print tree1 
    print "tree1 has a diameter of %d" % find_diam(tree1)[1]

    tree2 = Tree('*', [Tree('*',
                            [Tree('*',
                                  [Tree('*'),
                                   Tree('*')]),
                             Tree('*',
                                  [Tree('*'),
                                   Tree('*')])])])

    print tree2
    print "tree2 has a diameter of %d" % find_diam(tree2)[1]
    
if __name__ == '__main__':
    main()
