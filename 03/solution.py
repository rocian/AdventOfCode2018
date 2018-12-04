#!/usr/bin/env python3
# https://adventofcode.com/2018
# --- Day 3: No Matter How You Slice It ---

# The Elves managed to locate the chimney-squeeze prototype fabric for Santa's
# suit (thanks to someone who helpfully wrote its box IDs on the wall of the
# warehouse in the middle of the night). Unfortunately, anomalies are still
# affecting them - nobody can even agree on how to cut the fabric.

# The whole piece of fabric they're working on is a very large square - at least
# 1000 inches on each side.

# Each Elf has made a claim about which area of fabric would be ideal for
# Santa's suit. All claims have an ID and consist of a single rectangle with
# edges parallel to the edges of the fabric. Each claim's rectangle is defined
# as follows:

#     The number of inches between the left edge of the fabric and the left edge of the rectangle.
#     The number of inches between the top edge of the fabric and the top edge of the rectangle.
#     The width of the rectangle in inches.
#     The height of the rectangle in inches.

# A claim like #123 @ 3,2: 5x4 means that claim ID 123 specifies a rectangle 3
# inches from the left edge, 2 inches from the top edge, 5 inches wide, and 4
# inches tall. Visually, it claims the square inches of fabric represented by #
# (and ignores the square inches of fabric represented by .) in the diagram
# below:

# ...........
# ...........
# ...#####...
# ...#####...
# ...#####...
# ...#####...
# ...........
# ...........
# ...........

# The problem is that many of the claims overlap, causing two or more claims to
# cover part of the same areas. For example, consider the following claims:

# #1 @ 1,3: 4x4
# #2 @ 3,1: 4x4
# #3 @ 5,5: 2x2

# Visually, these claim the following areas:

# ........
# ...2222.
# ...2222.
# .11XX22.
# .11XX22.
# .111133.
# .111133.
# ........

# The four square inches marked with X are claimed by both 1 and 2. (Claim 3,
# while adjacent to the others, does not overlap either of them.)

# If the Elves all proceed with their own plans, none of them will have enough
# fabric. How many square inches of fabric are within two or more claims?

# To begin, get your puzzle input.

# --- Part Two ---

# Amidst the chaos, you notice that exactly one claim doesn't overlap by even a
# single square inch of fabric with any other claim. If you can somehow draw
# attention to it, maybe the Elves will be able to make Santa's suit after all!

# For example, in the claims above, only claim 3 is intact after all claims are
# made.

# What is the ID of the only claim that doesn't overlap?

from sys import stdin
import re
import numpy as np
# from collections import defaultdict

claim = re.compile(r'#(?P<ID>\d+) @ (?P<left>\d+),(?P<top>\d+): (?P<width>\d+)x(?P<height>\d+)')

def read_input():
    # the input is a list of string separated by LF
    slist = [claim.search(i).groups() for i in stdin.read().split('\n') if i]
    return slist
        

def part_one(slist):
    # the fabric has zeros overlapping at start
    fabric = np.zeros((1000,1000))
    
    for i in range(len(slist)):
        x0 = int(slist[i][1])
        y0 = int(slist[i][2])
        x1 = int(slist[i][3]) + x0
        y1 = int(slist[i][4]) + y0
        # add 1 to the slice of the fabric covered by the claim 
        fabric[x0:x1,y0:y1] += 1

    # return the number of square that were covered more than one
    # times and the fabric itself for future use
    return  np.sum(fabric > 1), fabric

def part_two(slist, fabric):
    # they claim that only one claim soes not overlap
    # we wil check that!
    what = []
    for i in range(len(slist)):
        x0 = int(slist[i][1])
        y0 = int(slist[i][2])
        x1 = int(slist[i][3]) + x0
        y1 = int(slist[i][4]) + y0

        # if the slice sum is equal to its area then there hasn't been no overlap
        if np.sum(fabric[x0:x1,y0:y1] == 1) == ( int(slist[i][3]) *  int(slist[i][4])):
            what.append(slist[i][0])

    return what

stringlist = read_input()
overlapped, fabric = part_one(stringlist)
idlist = part_two(stringlist, fabric)

print("\n--- Day 03 ---")
print("part 1: overlapped square inches = {}".format(overlapped))
if len(idlist) == 1:
    print("part 2: non overlapping ID = {}".format(idlist[0]))
else:
    print("part 2: Non unique non overlapping ID. something goes wrong.")
print("--------------\n")

# --- Day 03 ---
# part 1: overlapped square inches = 104712
# part 2: non overlapping ID = 840
# --------------
# 0 2:54  Tue Dec  4 02:54 CET 2018
# 1 4:21  Tue Dec  4 04:21 CET 2018
# position  16437  1300
# 2 4:31  Tue Dec  4 04:31 CET 2018
# position  16507  1287
