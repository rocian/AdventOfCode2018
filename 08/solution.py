#!/usr/bin/env python3
# https://adventofcode.com/2018

# --- Day 8: Memory Maneuver ---

# The sleigh is much easier to pull than you'd expect for something its
# weight. Unfortunately, neither you nor the Elves know which way the North Pole
# is from here.

# You check your wrist device for anything that might help. It seems to have
# some kind of navigation system! Activating the navigation system produces more
# bad news: "Failed to start navigation system. Could not read software license
# file."

# The navigation system's license file consists of a list of numbers (your
# puzzle input). The numbers define a data structure which, when processed,
# produces some kind of tree that can be used to calculate the license number.

# The tree is made up of nodes; a single, outermost node forms the tree's root,
# and it contains all other nodes in the tree (or contains nodes that contain
# nodes, and so on).

# Specifically, a node consists of:

#     A header, which is always exactly two numbers:
#         The quantity of child nodes.
#         The quantity of metadata entries.
#     Zero or more child nodes (as specified in the header).
#     One or more metadata entries (as specified in the header).

# Each child node is itself a node that has its own header, child nodes, and
# metadata. For example:

# 2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2
# A----------------------------------
#     B----------- C-----------
#                      D-----

# In this example, each node of the tree is also marked with an underline
# starting with a letter for easier identification. In it, there are four nodes:

#     A, which has 2 child nodes (B, C) and 3 metadata entries (1, 1, 2).
#     B, which has 0 child nodes and 3 metadata entries (10, 11, 12).
#     C, which has 1 child node (D) and 1 metadata entry (2).
#     D, which has 0 child nodes and 1 metadata entry (99).

# The first check done on the license file is to simply add up all of the
# metadata entries. In this example, that sum is 1+1+2+10+11+12+2+99=138.

# What is the sum of all metadata entries?

# --- Part Two ---

# The second check is slightly more complicated: you need to find the value of
# the root node (A in the example above).

# The value of a node depends on whether it has child nodes.

# If a node has no child nodes, its value is the sum of its metadata
# entries. So, the value of node B is 10+11+12=33, and the value of node D is
# 99.

# However, if a node does have child nodes, the metadata entries become indexes
# which refer to those child nodes. A metadata entry of 1 refers to the first
# child node, 2 to the second, 3 to the third, and so on. The value of this node
# is the sum of the values of the child nodes referenced by the metadata
# entries. If a referenced child node does not exist, that reference is
# skipped. A child node can be referenced multiple time and counts each time it
# is referenced. A metadata entry of 0 does not refer to any child node.

# For example, again using the above nodes:
#
#     Node C has one metadata entry, 2. Because node C has only one child node,
#     2 references a child node which does not exist, and so the value of node C
#     is 0.
#
#     Node A has three metadata entries: 1, 1, and 2. The 1 references node A's
#     first child node, B, and the 2 references node A's second child node,
#     C. Because node B has a value of 33 and node C has a value of 0, the value
#     of node A is 33+33+0=66.
#
# So, in this example, the value of the root node is 66.
# What is the value of the root node?


from sys import stdin


def read_input():
    # read and return stripped list of int for tree contruction
    return [int(i) for i in stdin.read().strip().split()]


class node(object):
    def __init__(self):
        self.child = []
        self.meta = []

    def getwm(self):
        # get whole metadata sum for this node and its childrens
        cm = 0
        for c in self.child:
            cm += c.getwm()
        return sum(self.meta) + cm

    def getvn(self):
        # get value of this node based on chlds values
        # if it has not childs its value is the sum of its meta
        if len(self.child) == 0:
            return sum(self.meta)

        # if it has childs its value is the sum of childs values
        # indexed by metavalue
        # meta=1 refer to child 1 ecc.
        # invalid index are skipped
        cm = 0
        for i in self.meta:
            if 0 < i <= len(self.child):
                cm += self.child[i - 1].getvn()

        return cm

    def add_child(self, node):
        self.child.append(node)

    def __str__(self):
        return "[{}],{}".format(self.child, self.meta)


def get_node(root, index, values):
    # recursive method to construct tree

    # the first value on values is the number of childs
    noc = values[index]
    index += 1

    # the second values is the number of metadata
    nmeta = values[index]
    index += 1

    # create a new node and add it as child of root node
    newnode = node()
    root.add_child(newnode)

    # if there are childs recursively add them to the tree
    for i in range(noc):
        index = get_node(newnode, index, values)

    # add metadata
    newnode.meta = values[index:index + nmeta]

    # return new index
    return index + nmeta


def part_one(values):
    # create tree
    node0 = node()
    index = 0
    get_node(node0, index, values)

    # manually add a metadata to the root node, as
    # it is needed to calculate the values of tree
    node0.meta = [1]
    return node0.getwm(), node0.getvn()


treevalues = read_input()
part1, part2 = part_one(treevalues)

print("\n--- Day 08 ---")
print("part 1: answer to part one = {}".format(part1))
print("part 2: answer to part two = {}".format(part2))
print("--------------\n")

# --- Day 08 ---
# part 1: answer to part one = 46097
# part 2: answer to part two = 24820
# --------------
#
# 0 08:01  Sun Dec  9 08:01 CET 2018
# 1 10:44  Sun Dec  9 10:44 CET 2018
# position 8078    514
# 2 10:58  Sun Dec  9 10:58 CET 2018
# position 8095    519
