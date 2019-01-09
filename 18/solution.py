#!/usr/bin/env python3
# https://adventofcode.com/2018
# --- Day 18: Settlers of The North Pole ---

# On the outskirts of the North Pole base construction project, many Elves are
# collecting lumber.

# The lumber collection area is 50 acres by 50 acres; each acre can be either
# open ground (.), trees (|), or a lumberyard (#). You take a scan of the area
# (your puzzle input).

# Strange magic is at work here: each minute, the landscape looks entirely
# different. In exactly one minute, an open acre can fill with trees, a wooded
# acre can be converted to a lumberyard, or a lumberyard can be cleared to open
# ground (the lumber having been sent to other projects).

# The change to each acre is based entirely on the contents of that acre as well
# as the number of open, wooded, or lumberyard acres adjacent to it at the start
# of each minute. Here, "adjacent" means any of the eight acres surrounding that
# acre. (Acres on the edges of the lumber collection area might have fewer than
# eight adjacent acres; the missing acres aren't counted.)

# In particular:

#     An open acre will become filled with trees if three or more adjacent acres
#     contained trees. Otherwise, nothing happens.

#     An acre filled with trees will become a lumberyard if three or more
#     adjacent acres were lumberyards. Otherwise, nothing happens.

#     An acre containing a lumberyard will remain a lumberyard if it was
#     adjacent to at least one other lumberyard and at least one acre containing
#     trees. Otherwise, it becomes open.

# These changes happen across all acres simultaneously, each of them using the
# state of all acres at the beginning of the minute and changing to their new
# form by the end of that same minute. Changes that happen during the minute
# don't affect each other.

# For example, suppose the lumber collection area is instead only 10 by 10 acres
# with this initial configuration:

# Initial state:
# .#.#...|#.
# .....#|##|
# .|..|...#.
# ..|#.....#
# #.#|||#|#|
# ...#.||...
# .|....|...
# ||...#|.#|
# |.||||..|.
# ...#.|..|.

# After 1 minute:
# .......##.
# ......|###
# .|..|...#.
# ..|#||...#
# ..##||.|#|
# ...#||||..
# ||...|||..
# |||||.||.|
# ||||||||||
# ....||..|.

# After 2 minutes:
# .......#..
# ......|#..
# .|.|||....
# ..##|||..#
# ..###|||#|
# ...#|||||.
# |||||||||.
# ||||||||||
# ||||||||||
# .|||||||||

# After 3 minutes:
# .......#..
# ....|||#..
# .|.||||...
# ..###|||.#
# ...##|||#|
# .||##|||||
# ||||||||||
# ||||||||||
# ||||||||||
# ||||||||||

# After 4 minutes:
# .....|.#..
# ...||||#..
# .|.#||||..
# ..###||||#
# ...###||#|
# |||##|||||
# ||||||||||
# ||||||||||
# ||||||||||
# ||||||||||

# After 5 minutes:
# ....|||#..
# ...||||#..
# .|.##||||.
# ..####|||#
# .|.###||#|
# |||###||||
# ||||||||||
# ||||||||||
# ||||||||||
# ||||||||||

# After 6 minutes:
# ...||||#..
# ...||||#..
# .|.###|||.
# ..#.##|||#
# |||#.##|#|
# |||###||||
# ||||#|||||
# ||||||||||
# ||||||||||
# ||||||||||

# After 7 minutes:
# ...||||#..
# ..||#|##..
# .|.####||.
# ||#..##||#
# ||##.##|#|
# |||####|||
# |||###||||
# ||||||||||
# ||||||||||
# ||||||||||

# After 8 minutes:
# ..||||##..
# ..|#####..
# |||#####|.
# ||#...##|#
# ||##..###|
# ||##.###||
# |||####|||
# ||||#|||||
# ||||||||||
# ||||||||||

# After 9 minutes:
# ..||###...
# .||#####..
# ||##...##.
# ||#....###
# |##....##|
# ||##..###|
# ||######||
# |||###||||
# ||||||||||
# ||||||||||

# After 10 minutes:
# .||##.....
# ||###.....
# ||##......
# |##.....##
# |##.....##
# |##....##|
# ||##.####|
# ||#####|||
# ||||#|||||
# ||||||||||

# After 10 minutes, there are 37 wooded acres and 31 lumberyards. Multiplying
# the number of wooded acres by the number of lumberyards gives the total
# resource value after ten minutes: 37 * 31 = 1147.

# What will the total resource value of the lumber collection area be after 10
# minutes?

# --- Part Two ---

# This important natural resource will need to last for at least thousands of
# years. Are the Elves collecting this lumber sustainably?

# What will the total resource value of the lumber collection area be after
# 1000000000 minutes?


from sys import stdin
import numpy as np


def read_input():
    lines = stdin.read().strip().split('\n')
    nx = 0
    for i in range(len(lines)):
        if nx < len(lines[i]):
            nx = len(lines[i])
    ny = len(lines)
    lumber = np.chararray((ny, nx))
    for i, l in enumerate(lines):
        for j, q in enumerate(l):
            lumber[i][j] = q
    return lumber


def represent(s):
    print('\n'.join([''.join(row) for row in s.astype(str)]))
    print('\n')


def evolve(lumber):
    ny, nx = lumber.shape
    newlumber = np.chararray((ny, nx))
    for y in range(ny):
        for x in range(nx):
            acre = lumber[y, x]
            content = lumber[max(y - 1, 0):min(y + 2, ny), max(x - 1, 0):min(x + 2, nx)]
            numtree = content.count(b'|').sum()
            numyard = content.count(b'#').sum()

            # print(numtree)

            result = acre

            if acre == b'.' and numtree > 2:
                result = b'|'
            if acre == b'|' and numyard > 2:
                result = b'#'
            if acre == b'#':
                if numyard > 1 and numtree > 0:
                    result = b'#'
                else:
                    result = b'.'

            newlumber[y, x] = result

    return newlumber


lumber = read_input()

xsolutions = dict()
lumstatus = dict()
start = 0
stop = 0
minutes = 1000000000
for i in range(1, minutes):
    lumber = evolve(lumber)
    numtree = lumber.count(b'|').sum()
    numyard = lumber.count(b'#').sum()
    rvalue = numtree * numyard

    xsolutions[i] = rvalue
    lumstr = ''.join([''.join(row) for row in lumber.astype(str)])

    if i == 10:
        part1 = rvalue
        # break

    if lumstr in lumstatus:
        start = lumstatus[lumstr]
        stop = i
        break

    lumstatus[lumstr] = i

period = stop - start

part2 = xsolutions[(minutes - start) % period + start]


print("\n--- Day 18 ---")
print("part 1: answer to part one = {}".format(part1))
print("part 2: answer to part two = {}".format(part2))
print("--------------\n")

# --- Day 18 ---
# part 1: answer to part one = 539682
# part 2: answer to part two = 226450
# --------------
#
# 0 Mon Jan  7 21:03 CET 2019
#          5931    378
# 1 Tue Jan  8 00:21 CET 2019
# position 5933    379
# 2 Wed Jan  9 23:13 CET 2019
# position 5966    377
