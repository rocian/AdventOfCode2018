#!/usr/bin/env python3
# https://adventofcode.com/2018
# --- Day 17: Reservoir Research ---

# You arrive in the year 18. If it weren't for the coat you got in 1018, you
# would be very cold: the North Pole base hasn't even been constructed.

# Rather, it hasn't been constructed yet. The Elves are making a little
# progress, but there's not a lot of liquid water in this climate, so they're
# getting very dehydrated. Maybe there's more underground?

# You scan a two-dimensional vertical slice of the ground nearby and discover
# that it is mostly sand with veins of clay. The scan only provides data with a
# granularity of square meters, but it should be good enough to determine how
# much water is trapped there. In the scan, x represents the distance to the
# right, and y represents the distance down. There is also a spring of water
# near the surface at x=500, y=0. The scan identifies which square meters are
# clay (your puzzle input).

# For example, suppose your scan shows the following veins of clay:

# x=495, y=2..7
# y=7, x=495..501
# x=501, y=3..7
# x=498, y=2..4
# x=506, y=1..2
# x=498, y=10..13
# x=504, y=10..13
# y=13, x=498..504

# Rendering clay as #, sand as ., and the water spring as +, and with x
# increasing to the right and y increasing downward, this becomes:

#    44444455555555
#    99999900000000
#    45678901234567
#  0 ......+.......
#  1 ............#.
#  2 .#..#.......#.
#  3 .#..#..#......
#  4 .#..#..#......
#  5 .#.....#......
#  6 .#.....#......
#  7 .#######......
#  8 ..............
#  9 ..............
# 10 ....#.....#...
# 11 ....#.....#...
# 12 ....#.....#...
# 13 ....#######...

# The spring of water will produce water forever. Water can move through sand,
# but is blocked by clay. Water always moves down when possible, and spreads to
# the left and right otherwise, filling space that has clay on both sides and
# falling out otherwise.

# For example, if five squares of water are created, they will flow downward
# until they reach the clay and settle there. Water that has come to rest is
# shown here as ~, while sand through which water has passed (but which is now
# dry again) is shown as |:

# ......+.......
# ......|.....#.
# .#..#.|.....#.
# .#..#.|#......
# .#..#.|#......
# .#....|#......
# .#~~~~~#......
# .#######......
# ..............
# ..............
# ....#.....#...
# ....#.....#...
# ....#.....#...
# ....#######...

# Two squares of water can't occupy the same location. If another five squares
# of water are created, they will settle on the first five, filling the clay
# reservoir a little more:

# ......+.......
# ......|.....#.
# .#..#.|.....#.
# .#..#.|#......
# .#..#.|#......
# .#~~~~~#......
# .#~~~~~#......
# .#######......
# ..............
# ..............
# ....#.....#...
# ....#.....#...
# ....#.....#...
# ....#######...

# Water pressure does not apply in this scenario. If another four squares of
# water are created, they will stay on the right side of the barrier, and no
# water will reach the left side:

# ......+.......
# ......|.....#.
# .#..#.|.....#.
# .#..#~~#......
# .#..#~~#......
# .#~~~~~#......
# .#~~~~~#......
# .#######......
# ..............
# ..............
# ....#.....#...
# ....#.....#...
# ....#.....#...
# ....#######...

# At this point, the top reservoir overflows. While water can reach the tiles
# above the surface of the water, it cannot settle there, and so the next five
# squares of water settle like this:

# ......+.......
# ......|.....#.
# .#..#||||...#.
# .#..#~~#|.....
# .#..#~~#|.....
# .#~~~~~#|.....
# .#~~~~~#|.....
# .#######|.....
# ........|.....
# ........|.....
# ....#...|.#...
# ....#...|.#...
# ....#~~~~~#...
# ....#######...

# Note especially the leftmost |: the new squares of water can reach this tile,
# but cannot stop there. Instead, eventually, they all fall to the right and
# settle in the reservoir below.

# After 10 more squares of water, the bottom reservoir is also full:

# ......+.......
# ......|.....#.
# .#..#||||...#.
# .#..#~~#|.....
# .#..#~~#|.....
# .#~~~~~#|.....
# .#~~~~~#|.....
# .#######|.....
# ........|.....
# ........|.....
# ....#~~~~~#...
# ....#~~~~~#...
# ....#~~~~~#...
# ....#######...

# Finally, while there is nowhere left for the water to settle, it can reach a
# few more tiles before overflowing beyond the bottom of the scanned data:

# ......+.......    (line not counted: above minimum y value)
# ......|.....#.
# .#..#||||...#.
# .#..#~~#|.....
# .#..#~~#|.....
# .#~~~~~#|.....
# .#~~~~~#|.....
# .#######|.....
# ........|.....
# ...|||||||||..
# ...|#~~~~~#|..
# ...|#~~~~~#|..
# ...|#~~~~~#|..
# ...|#######|..
# ...|.......|..    (line not counted: below maximum y value)
# ...|.......|..    (line not counted: below maximum y value)
# ...|.......|..    (line not counted: below maximum y value)

# How many tiles can be reached by the water? To prevent counting forever,
# ignore tiles with a y coordinate smaller than the smallest y coordinate in
# your scan data or larger than the largest one. Any x coordinate is valid. In
# this example, the lowest y coordinate given is 1, and the highest is 13,
# causing the water spring (in row 0) and the water falling off the bottom of
# the render (in rows 14 through infinity) to be ignored.

# So, in the example above, counting both water at rest (~) and other sand tiles
# the water can hypothetically reach (|), the total number of tiles the water
# can reach is 57.

# How many tiles can the water reach within the range of y values in your scan?

# --- Part Two ---

# After a very long time, the water spring will run dry. How much water will be
# retained?

# In the example above, water that won't eventually drain out is shown as ~, a
# total of 29 tiles.

# How many water tiles are left after the water spring stops producing water and
# all remaining water not at rest has drained?

from sys import stdin
import re
import numpy as np
import collections

clayx = re.compile(r'x=(?P<x>\d+), y=(?P<sy>\d+)\.\.(?P<ey>\d+)$')
clayy = re.compile(r'y=(?P<y>\d+), x=(?P<sx>\d+)\.\.(?P<ex>\d+)$')


def read_input():
    # the input is a list of string separated by LF
    slist = []
    for i in stdin.read().strip().split('\n'):
        if i.startswith('x'):
            a = [int(x) for x in clayx.search(i).groups()]
            slist.append((range(a[0], a[0] + 1), range(a[1], a[2] + 1)))
        else:
            a = [int(x) for x in clayy.search(i).groups()]
            slist.append((range(a[1], a[2] + 1),range(a[0], a[0] + 1)))

    minx, miny = np.inf, np.inf
    maxx, maxy = -np.inf, -np.inf
    for x, y in slist:
        if np.max(x) > maxx:
            maxx = np.max(x)
        if np.min(x) < minx:
            minx = np.min(x)
        if np.max(y) > maxy:
            maxy = np.max(y)
        if np.min(y) < miny:
            miny = np.min(y)

    return slist, minx, maxx, miny, maxy


def represent(s):
    print('\n'.join([''.join(row) for row in s.astype(str)]))
    print('\n')


def findlimits(s, x, y):
    ymax, xmax = s.shape
    if (y + 1) > ymax:
        return False, False, [x, x + 1], b'|'

    ltypel, ltyper = True, True
    sx = 1
    while  True:
        X = x - sx
        if X < 0:
            ltypel = False
            break
        if s[y][X] == b'.' and s[y+1][X] in b'#~':
            X = x - sx
            
        if s[y][X] == b'.' and s[y+1][X] in b'.':
            sx += 1
            ltypel = False
            break
        if s[y][X] == b'#':
            ltypel = True
            break
        sx += 1

    dx = 1
    while  True:
        X = x + dx
        if X >= xmax:
            ltyper = False
            dx = dx - 1
            break
        if s[y][X] == b'.' and s[y+1][X] in b'#~':
            X = x + dx
        if s[y][X] == b'.' and s[y+1][X] in b'.':
            dx += 1
            ltyper = False
            break
        if s[y][X] == b'#':
            ltyper = True
            break
        dx += 1

    mark = b'|'
    if ltypel and ltyper:
        mark = b'~'

    return ltypel, ltyper, [x - sx + 1, x + dx + 1 - 1], mark
        
    
s, minx, maxx, miny, maxy = read_input()

# fence for borders
minx -= 3

scan = np.chararray((maxy - miny + 1,maxx - minx + 1))
scan[:] = '.'
for rx, ry in s:
    for y in ry:
        for x in rx:
            scan[y-miny][x-minx] = b'#'

scan[0][500 - minx] = '|'
# uncomment if want a representation
# represent(scan)
q = collections.deque([(500 - minx,0)])
polo = 0
while True:
    x, y = q.pop()
    if scan[y][x] == b'|':
        if  0 <= (y + 1) <= (maxy - miny):
            if scan[y + 1][x] == b'.':
                scan[y + 1][x] = b'|'
                q.append((x, y))
                q.append((x, y + 1))
            elif scan[y + 1][x] in b'#~':
                ltypel, ltyper, rx, mark = findlimits(scan, x, y)
                scan[y][rx[0]:rx[1]] = mark
                if not ltypel:
                    q.append((rx[0], y))
                if not ltyper:
                    q.append((rx[1]-1, y))
                    

    if len(q) == 0:
        # represent(scan)
        break

# still water
part2 = scan.count(b'~').sum()
# flowing water
part1 = scan.count(b'|').sum() + part2
print("\n--- Day 17 ---")
print("part 1: answer to part one = {}".format(part1))
print("part 2: answer to part two = {}".format(part2))
print("--------------\n")

# --- Day 17 ---
# part 1: answer to part one = 29802
# part 2: answer to part two = 24660
# --------------
#
# 0 Sun Jan  6 11:03 CET 2019
#          4631     31
# 1 Sat Jan  6 17:45 CET 2019
# position 4639     30
# 2 Sat Jan  6 17:48 CET 2019
# position 4640     29
