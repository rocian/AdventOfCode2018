#!/usr/bin/env python3
# https://adventofcode.com/2018
# --- Day 6: Chronal Coordinates ---

# The device on your wrist beeps several times, and once again you feel like
# you're falling.

# "Situation critical," the device announces. "Destination
# indeterminate. Chronal interference detected. Please specify new target
# coordinates."

# The device then produces a list of coordinates (your puzzle input). Are they
# places it thinks are safe or dangerous? It recommends you check manual page
# 729. The Elves did not give you a manual.

# If they're dangerous, maybe you can minimize the danger by finding the
# coordinate that gives the largest distance from the other points.

# Using only the Manhattan distance, determine the area around each coordinate
# by counting the number of integer X,Y locations that are closest to that
# coordinate (and aren't tied in distance to any other coordinate).

# Your goal is to find the size of the largest area that isn't infinite. For
# example, consider the following list of coordinates:

# 1, 1
# 1, 6
# 8, 3
# 3, 4
# 5, 5
# 8, 9

# If we name these coordinates A through F, we can draw them on a grid, putting
# 0,0 at the top left:

# ..........
# .A........
# ..........
# ........C.
# ...D......
# .....E....
# .B........
# ..........
# ..........
# ........F.

# This view is partial - the actual grid extends infinitely in all
# directions. Using the Manhattan distance, each location's closest coordinate
# can be determined, shown here in lowercase:

# aaaaa.cccc
# aAaaa.cccc
# aaaddecccc
# aadddeccCc
# ..dDdeeccc
# bb.deEeecc
# bBb.eeee..
# bbb.eeefff
# bbb.eeffff
# bbb.ffffFf

# Locations shown as . are equally far from two or more coordinates, and so they
# don't count as being closest to any.

# In this example, the areas of coordinates A, B, C, and F are infinite - while
# not shown here, their areas extend forever outside the visible grid. However,
# the areas of coordinates D and E are finite: D is closest to 9 locations, and
# E is closest to 17 (both including the coordinate's location
# itself). Therefore, in this example, the size of the largest area is 17.

# What is the size of the largest area that isn't infinite?

# --- Part Two ---

# On the other hand, if the coordinates are safe, maybe the best you can do is
# try to find a region near as many coordinates as possible.

# For example, suppose you want the sum of the Manhattan distance to all of the
# coordinates to be less than 32. For each location, add up the distances to all
# of the given coordinates; if the total of those distances is less than 32,
# that location is within the desired region. Using the same coordinates as
# above, the resulting region looks like this:

# ..........
# .A........
# ..........
# ...###..C.
# ..#D###...
# ..###E#...
# .B.###....
# ..........
# ..........
# ........F.

# In particular, consider the highlighted location 4,3 located at the top middle
# of the region. Its calculation is as follows, where abs() is the absolute
# value function:

#     Distance to coordinate A: abs(4-1) + abs(3-1) =  5
#     Distance to coordinate B: abs(4-1) + abs(3-6) =  6
#     Distance to coordinate C: abs(4-8) + abs(3-3) =  4
#     Distance to coordinate D: abs(4-3) + abs(3-4) =  2
#     Distance to coordinate E: abs(4-5) + abs(3-5) =  3
#     Distance to coordinate F: abs(4-8) + abs(3-9) = 10
#     Total distance: 5 + 6 + 4 + 2 + 3 + 10 = 30

# Because the total distance to all coordinates (30) is less than 32, the
# location is within the region.

# This region, which also includes coordinates D and E, has a total size of 16.

# Your actual region will need to be much larger than this example, though,
# instead including all locations with a total distance of less than 10000.

# What is the size of the region containing all locations which have a total
# distance to all given coordinates of less than 10000?


from sys import stdin
import numpy as np


def read_input():
    # read and return stripped couple of coords
    couples = stdin.read().strip().split('\n')
    # create a list of coords
    return [(int(q.split(', ')[0]), int(q.split(', ')[1])) for q in couples]


def part_one(cords):
    # initialize high and low values
    minX = np.inf
    maxX = -np.inf
    minY = np.inf
    maxY = -np.inf

    # find max and min coords
    for i, j in cords:
        if minX > i:
            minX = i

        if maxX < i:
            maxX = i

        if minY > j:
            minY = j

        if maxY < j:
            maxY = j

    # shape aour area
    area = np.chararray((maxX - minX + 1, maxY - minY + 1))

    # copy coords
    cords2 = [u for u in cords]
    # recreate cords by shift
    cords = []
    for i, j in cords2:
        cords.append((i - minX, j - minY))

    # create all possible labels
    pp = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ,!|£$%&/()=?^'
    for x in range(maxX - minX + 1):
        for y in range(maxY - minY + 1):
            D = np.inf
            point = 1
            v = '.'
            for i, j in cords:
                d = np.abs(i - x) + np.abs(j - y)
                if d == D:
                    # exclude this point
                    v = '.'
                if d < D:
                    D = d
                    # this is the shortest cords (at the end)
                    v = pp[point]
                point += 1

            area[x][y] = v

    # create allpoints, exclude and remaining sets
    excluded = set('.')
    allpoints = set('.')
    for x in range(maxX - minX + 1):
        for y in range(maxY - minY + 1):
            val = area[x][y]
            if x == 0 or x == maxX - minX or y == 0 or y == maxY - minY:
                excluded.add(val)
            else:
                allpoints.add(val)

    remaining = allpoints - excluded

    # count how many points fo each char in remaining
    # and take the maximum
    D = 0
    for val in remaining:
        d = sum(sum(area.count(val)))
        if d > D:
            D = d

    # count the total point in the region at a maximun distance of 10000
    # from each point
    total = 0
    for x in range(maxX - minX + 1):
        for y in range(maxY - minY + 1):
            sumc = 0
            for i, j in cords:
                sumc += np.abs(i - x) + np.abs(j - y)

            if sumc < 10000:
                total += 1

    return D, total


corstr = read_input()
how_many_p, total_near = part_one(corstr)

print("\n--- Day 05 ---")
print("part 1: answer to part one = {}".format(how_many_p))
print("part 2: answer to part two = {}".format(total_near))
print("--------------\n")

# --- Day 06 ---
# part 1: answer to part one = 4398
# part 2: answer to part two = 39560
# --------------
#
# 0 02:43  Sat Dec  8 02:43 CET 2018
# 1 04:20  Sat Dec  8 04:20 CET 2018
# position 11619    613
# 2 04:28  Sat Dec  8 04:28 CET 2018
# position 11625    614
