#!/usr/bin/env python3
# https://adventofcode.com/2018
# --- Day 13: Mine Cart Madness ---

# A crop of this size requires significant logistics to transport produce, soil,
# fertilizer, and so on. The Elves are very busy pushing things around in carts
# on some kind of rudimentary system of strack they've come up with.

# Seeing as how cart-and-track systems don't appear in recorded history for
# another 1000 years, the Elves seem to be making this up as they go along. They
# haven't even figured out how to avoid collisions yet.

# You map out the strack (your puzzle input) and see where you can help.

# Tracks consist of straight paths (| and -), curves (/ and \), and
# intersections (+). Curves connect exactly two perpendicular pieces of track;
# for example, this is a closed loop:

# /----\
# |    |
# |    |
# \----/

# Intersections occur when two perpendicular paths cross. At an intersection, a
# cart is capable of turning left, turning right, or continuing straight. Here
# are two loops connected by two intersections:

# /-----\
# |     |
# |  /--+--\
# |  |  |  |
# \--+--/  |
#    |     |
#    \-----/

# Several carts are also on the strack. Carts always face either up (^), down
# (v), left (<), or right (>). (On your initial map, the track under each cart
# is a straight path matching the direction the cart is facing.)

# Each time a cart has the option to turn (by arriving at any intersection), it
# turns left the first time, goes straight the second time, turns right the
# third time, and then repeats those directions starting again with left the
# fourth time, straight the fifth time, and so on. This process is independent
# of the particular intersection at which the cart has arrived - that is, the
# cart has no per-intersection memory.

# Carts all move at the same speed; they take turns moving a single step at a
# time. They do this based on their current location: carts on the top row move
# first (acting from left to right), then carts on the second row move (again
# from left to right), then carts on the third row, and so on. Once each cart
# has moved one step, the process repeats; each of these loops is called a tick.

# For example, suppose there are two carts on a straight track:

# |  |  |  |  |
# v  |  |  |  |
# |  v  v  |  |
# |  |  |  v  X
# |  |  ^  ^  |
# ^  ^  |  |  |
# |  |  |  |  |

# First, the top cart moves. It is facing down (v), so it moves down one
# square. Second, the bottom cart moves. It is facing up (^), so it moves up one
# square. Because all carts have moved, the first tick ends. Then, the process
# repeats, starting with the first cart. The first cart moves down, then the
# second cart moves up - right into the first cart, colliding with it! (The
# location of the crash is marked with an X.) This ends the second and last
# tick.

# Here is a longer example:

# /->-\
# |   |  /----\
# | /-+--+-\  |
# | | |  | v  |
# \-+-/  \-+--/
#   \------/

# /-->\
# |   |  /----\
# | /-+--+-\  |
# | | |  | |  |
# \-+-/  \->--/
#   \------/

# /---v
# |   |  /----\
# | /-+--+-\  |
# | | |  | |  |
# \-+-/  \-+>-/
#   \------/

# /---\
# |   v  /----\
# | /-+--+-\  |
# | | |  | |  |
# \-+-/  \-+->/
#   \------/

# /---\
# |   |  /----\
# | /->--+-\  |
# | | |  | |  |
# \-+-/  \-+--^
#   \------/

# /---\
# |   |  /----\
# | /-+>-+-\  |
# | | |  | |  ^
# \-+-/  \-+--/
#   \------/

# /---\
# |   |  /----\
# | /-+->+-\  ^
# | | |  | |  |
# \-+-/  \-+--/
#   \------/

# /---\
# |   |  /----<
# | /-+-->-\  |
# | | |  | |  |
# \-+-/  \-+--/
#   \------/

# /---\
# |   |  /---<\
# | /-+--+>\  |
# | | |  | |  |
# \-+-/  \-+--/
#   \------/

# /---\
# |   |  /--<-\
# | /-+--+-v  |
# | | |  | |  |
# \-+-/  \-+--/
#   \------/

# /---\
# |   |  /-<--\
# | /-+--+-\  |
# | | |  | v  |
# \-+-/  \-+--/
#   \------/

# /---\
# |   |  /<---\
# | /-+--+-\  |
# | | |  | |  |
# \-+-/  \-<--/
#   \------/

# /---\
# |   |  v----\
# | /-+--+-\  |
# | | |  | |  |
# \-+-/  \<+--/
#   \------/

# /---\
# |   |  /----\
# | /-+--v-\  |
# | | |  | |  |
# \-+-/  ^-+--/
#   \------/

# /---\
# |   |  /----\
# | /-+--+-\  |
# | | |  X |  |
# \-+-/  \-+--/
#   \------/

# After following their respective paths for a while, the carts eventually
# crash. To help prevent crashes, you'd like to know the location of the first
# crash. Locations are given in X,Y coordinates, where the furthest left column
# is X=0 and the furthest top row is Y=0:

#            111
#  0123456789012
# 0/---\
# 1|   |  /----\
# 2| /-+--+-\  |
# 3| | |  X |  |
# 4\-+-/  \-+--/
# 5  \------/

# In this example, the location of the first crash is 7,3.
# --- Part Two ---

# There isn't much you can do to prevent crashes in this ridiculous
# system. However, by predicting the crashes, the Elves know where to be in
# advance and instantly remove the two crashing carts the moment any crash
# occurs.

# They can proceed like this for a while, but eventually, they're going to run
# out of carts. It could be useful to figure out where the last cart that hasn't
# crashed will end up.

# For example:

# />-<\
# |   |
# | /<+-\
# | | | v
# \>+</ |
#   |   ^
#   \<->/

# /---\
# |   |
# | v-+-\
# | | | |
# \-+-/ |
#   |   |
#   ^---^

# /---\
# |   |
# | /-+-\
# | v | |
# \-+-/ |
#   ^   ^
#   \---/

# /---\
# |   |
# | /-+-\
# | | | |
# \-+-/ ^
#   |   |
#   \---/

# After four very expensive crashes, a tick ends with only one cart remaining;
# its final location is 6,4.

# What is the location of the last cart at the end of the first tick where it is
# the only cart left?


from sys import stdin
import numpy as np

strack = {' ': 2, '|': 1j, '/': 1, '\\': -1, '-': -1j, '+': 0}
scars = {'^': 1, '>': 1j, 'v': -1, '<': -1j}


class carlist(object):
    def __init__(self):
        self.cars = []

    def append(self, tup):
        if tup in self.cars:
            return False
        self.cars.append(tup)
        return True

    def remove(self, tup):
        if tup not in self.cars:
            return False
        self.cars.remove(tup)
        return True


class car(object):

    option = [-1j, 1, 1j]

    def __init__(self, x, y, d):
        self.x = x
        self.y = y
        self.d = scars[d]
        self.index = 0

    def step(self, track):
        x = self.x
        y = self.y

        if track[self.x, self.y] != 0:
            snew = track[self.x, self.y] * self.d
            self.y -= int(snew.imag)
            self.x += int(snew.real)
            self.d = int(snew.imag) + 1j * int(snew.real)
        else:
            self.curve()
            snew = -1j * self.d
            self.y += int(snew.imag)
            self.x += int(snew.real)

        return (x, y), (self.x, self.y)

    def curve(self):
        self.d = self.option[self.index] * self.d
        self.index = (self.index + 1) % 3


def read_input():
    lines = stdin.read().split('\n')
    clist = []
    nx = 0
    for i in range(len(lines)):
        if nx < len(lines[i]):
            nx = len(lines[i])

    ny = len(lines)
    track = np.zeros((nx, ny), dtype=complex)
    for x in range(nx):
        for y in range(ny):
            track[x, y] = 2

    for y, l in enumerate(lines):
        li = list(l)
        for x, c in enumerate(li):

            if c in scars.keys():
                p = car(x, y, c)
                clist.append(p)
                if c in ['^', 'v']:
                    c = '|'
                else:
                    c = '-'

            track[x, y] = strack[c]

    return track, clist


def represent(track, carlist, crash=None, carlist2=None):
    nx, ny = track.shape
    stinv = dict()
    scinv = dict()
    for k in strack.keys():
        stinv[strack[k]] = k

    for k in scars.keys():
        scinv[scars[k]] = k

    visual = np.empty((ny, nx), dtype=str)
    visual[:, :] = ' '
    for y in range(ny):
        for x in range(nx):
            visual[y, x] = stinv[track[x, y]]

    for c in carlist:
        visual[c.y, c.x] = scinv[c.d]

    if crash is not None:
        visual[crash[1], crash[0]] = 'X'

    print('\n'.join([''.join(row) for row in visual]))


def part_one(track, cars):
    tick = 0
    position = carlist()

    for i, c in enumerate(cars):
        position.append((c.x, c.y))

    crashed = set()
    firstcrash = True

    while True:
        # represent(track, cars)
        cars.sort(key=lambda c: (c.y, c.x))
        for i, c in enumerate(cars):
            if c in crashed:
                continue

            old, new = c.step(track)
            position.remove(old)

            if not position.append(new):
                # represent(track, cars, new)
                if firstcrash:
                    ftick, fnew = tick, new
                    firstcrash = False

                crashed.add(c)
                for s in cars:
                    if s not in crashed:
                        if (s.x, s.y) == new:
                            crashed.add(s)

                position.remove(new)

                if len(crashed) == (len(cars) - 1):
                    for s in cars:
                        if s not in crashed:
                            utpost = (s.x, s.y)
                    return ftick, fnew, utpost

        tick += 1


track, cars = read_input()
tick, first_crash, last_car_pos = part_one(track, cars)

print("\n--- Day 13 ---")
print("part 1: answer to part one = tick {}, pos {}".format(tick, first_crash))
print("part 2: answer to part two = {}".format(last_car_pos))
print("--------------\n")

# --- Day 13 ---
# part 1: answer to part one = tick 125, pos (76, 108)
# part 2: answer to part two = (2, 84)
# --------------
#
# 0 03:46  Fri Dec 14 03:46 CET 2018
# 1 15:30  Sat Dec 15 15:30 CET 2018
# position 6025    599
# 2 15:53  Sat Dec 15 15:53 CET 2018
# position 6032    600
