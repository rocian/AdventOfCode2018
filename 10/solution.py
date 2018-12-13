#!/usr/bin/env python3
# https://adventofcode.com/2018

# --- Day 10: The Stars Align ---

# It's no use; your navigation system simply isn't capable of providing walking
# directions in the arctic circle, and certainly not in 1018.

# The Elves suggest an alternative. In times like these, North Pole rescue
# operations will arrange points of light in the sky to guide missing Elves back
# to base. Unfortunately, the message is easy to miss: the points move slowly
# enough that it takes hours to align them, but have so much momentum that they
# only stay aligned for a second. If you blink at the wrong time, it might be
# hours before another message appears.

# You can see these points of light floating in the distance, and record their
# position in the sky and their velocity, the relative change in position per
# second (your puzzle input). The coordinates are all given from your
# perspective; given enough time, those positions and velocities will move the
# points into a cohesive message!

# Rather than wait, you decide to fast-forward the process and calculate what
# the points will eventually spell.

# For example, suppose you note the following points:

# position=< 9,  1> velocity=< 0,  2>
# position=< 7,  0> velocity=<-1,  0>
# position=< 3, -2> velocity=<-1,  1>
# position=< 6, 10> velocity=<-2, -1>
# position=< 2, -4> velocity=< 2,  2>
# position=<-6, 10> velocity=< 2, -2>
# position=< 1,  8> velocity=< 1, -1>
# position=< 1,  7> velocity=< 1,  0>
# position=<-3, 11> velocity=< 1, -2>
# position=< 7,  6> velocity=<-1, -1>
# position=<-2,  3> velocity=< 1,  0>
# position=<-4,  3> velocity=< 2,  0>
# position=<10, -3> velocity=<-1,  1>
# position=< 5, 11> velocity=< 1, -2>
# position=< 4,  7> velocity=< 0, -1>
# position=< 8, -2> velocity=< 0,  1>
# position=<15,  0> velocity=<-2,  0>
# position=< 1,  6> velocity=< 1,  0>
# position=< 8,  9> velocity=< 0, -1>
# position=< 3,  3> velocity=<-1,  1>
# position=< 0,  5> velocity=< 0, -1>
# position=<-2,  2> velocity=< 2,  0>
# position=< 5, -2> velocity=< 1,  2>
# position=< 1,  4> velocity=< 2,  1>
# position=<-2,  7> velocity=< 2, -2>
# position=< 3,  6> velocity=<-1, -1>
# position=< 5,  0> velocity=< 1,  0>
# position=<-6,  0> velocity=< 2,  0>
# position=< 5,  9> velocity=< 1, -2>
# position=<14,  7> velocity=<-2,  0>
# position=<-3,  6> velocity=< 2, -1>

# Each line represents one point. Positions are given as <X, Y> pairs: X
# represents how far left (negative) or right (positive) the point appears,
# while Y represents how far up (negative) or down (positive) the point appears.

# At 0 seconds, each point has the position given. Each second, each point's
# velocity is added to its position. So, a point with velocity <1, -2> is moving
# to the right, but is moving upward twice as quickly. If this point's initial
# position were <3, 9>, after 3 seconds, its position would become <6, 3>.

# Over time, the points listed above would move like this:

# Initially:
# ........#.............
# ................#.....
# .........#.#..#.......
# ......................
# #..........#.#.......#
# ...............#......
# ....#.................
# ..#.#....#............
# .......#..............
# ......#...............
# ...#...#.#...#........
# ....#..#..#.........#.
# .......#..............
# ...........#..#.......
# #...........#.........
# ...#.......#..........

# After 1 second:
# ......................
# ......................
# ..........#....#......
# ........#.....#.......
# ..#.........#......#..
# ......................
# ......#...............
# ....##.........#......
# ......#.#.............
# .....##.##..#.........
# ........#.#...........
# ........#...#.....#...
# ..#...........#.......
# ....#.....#.#.........
# ......................
# ......................

# After 2 seconds:
# ......................
# ......................
# ......................
# ..............#.......
# ....#..#...####..#....
# ......................
# ........#....#........
# ......#.#.............
# .......#...#..........
# .......#..#..#.#......
# ....#....#.#..........
# .....#...#...##.#.....
# ........#.............
# ......................
# ......................
# ......................

# After 3 seconds:
# ......................
# ......................
# ......................
# ......................
# ......#...#..###......
# ......#...#...#.......
# ......#...#...#.......
# ......#####...#.......
# ......#...#...#.......
# ......#...#...#.......
# ......#...#...#.......
# ......#...#..###......
# ......................
# ......................
# ......................
# ......................

# After 4 seconds:
# ......................
# ......................
# ......................
# ............#.........
# ........##...#.#......
# ......#.....#..#......
# .....#..##.##.#.......
# .......##.#....#......
# ...........#....#.....
# ..............#.......
# ....#......#...#......
# .....#.....##.........
# ...............#......
# ...............#......
# ......................
# ......................

# After 3 seconds, the message appeared briefly: HI. Of course, your message
# will be much longer and will take many more seconds to appear.

# What message will eventually appear in the sky?

# --- Part Two ---

# Good thing you didn't have to wait, because that would have taken a long time
# - much longer than the 3 seconds in the example above.

# Impressed by your sub-hour communication capabilities, the Elves are curious:
# exactly how many seconds would they have needed to wait for that message to
# appear?



from sys import stdin
import numpy as np
import re
from scipy.special import entr
from pylab import *
import matplotlib.pyplot as plt
from PIL import Image

candv = re.compile(r".*<(.*),(.*)>.*<(.*),(.*)>")

def read_input():
    coords = [candv.search(x).groups() for x in stdin.read().strip().split('\n')]
    return [(int(x[0]), int(x[1]), int(x[2]), int(x[3])) for x in coords]

def part_one(coords):
    # get min max of image
    xmin = np.Inf
    xmax = -np.Inf

    ymin = np.Inf
    ymax = -np.Inf

    xvmin = np.Inf
    xvmax = -np.Inf

    yvmin = np.Inf
    yvmax = -np.Inf
    
    for x, y, vx, vy in coords:
        if xmin > x:
            xmin = x
        if ymin > y:
            ymin = y
        if xmax < x:
            xmax = x
        if ymax < y:
            ymax = y
        if xvmin > vx:
            xvmin = vx
        if yvmin > vy:
            yvmin = vy
        if xvmax < vx:
            xvmax = vx
        if yvmax < vy:
            yvmax = vy

    # calculate image size
    X = xmax - xmin
    Y = ymax - ymin

    pmin = np.Inf                     # minimum entropy
    the_t0 = -1                       # estimated final time
    t = 0                             # time
    citeration = True                 # if False stop iteration
    siz = 250                         # image size reduction factor
    # instead of iterating through to all t we could use
    # a fast gradient methods, but by reducing the image size
    # semmes that there is non need of such optimization
    while citeration:
        S = np.zeros((X//siz,Y//siz))                        # image
        n = 0                                                # number of point
        for x, y, vx, vy in coords:
            nx = (x + vx * t - xmin ) // siz
            ny = (y + vy * t - ymin) // siz
            if  (0 <= nx < X//siz) and (0 <= ny < Y//siz):
                S[nx, ny] += 1

            n += 1
        # we calculate entropy of reduced image
        p = (entr(S).sum(axis=0) / np.log(2))
        if pmin > sum(p) :
            pmin = sum(p)
            the_t0 = t
        
        t += 1

        # stop when half of the points ore out of sight
        # or when t is greater than 10^5
        if t > 100000:
            citeration = False

        if sum(sum(S)) < (n//2):
            citeration = False


    # calculate mean and deviation of image at time the_t (minimum entropy)
    nx = 0
    ny = 0
    N = 0
    for x, y, vx, vy in coords:
        nx += (x + vx * the_t0 - xmin)
        ny += (y + vy * the_t0 - ymin)
        N += 1

    xx = nx / N
    yy = ny / N

    for x, y, vx, vy in coords:
        nx += (x + vx * the_t0 - xmin - xx)**2
        ny += (y + vy * the_t0 - ymin - yy)**2

    sx = (nx/(N-1))**(1/2)
    sy = (ny/(N-1))**(1/2)

    # Use mean and stdev to calculate bounding box of image to represent
    # plot the 20 image around the approssimate minimum 
    # for successive visual inspect
    for t in range(20):
        the_t = the_t0 + t - 9
        S = np.zeros((2*int(sy)+1,2*int(sx)+1))
        for x, y, vx, vy in coords:
            nx = (x + vx * the_t - xmin)
            ny = (y + vy * the_t - ymin)
            if  (xx - sx <= nx < xx + sx) and (yy -sy<= ny < yy +sy):
                S[int(ny - yy + sy), int(nx - xx + sx)] = 255
                
        im = Image.fromarray(S.astype(np.uint8))
        im.save("{}.jpg".format(the_t))  # show()
        
coords = read_input()
part_one(coords)
#
# Solution by visual inspectio of result image files
#
# 0 12:30  Tue Dec 11 12:30 CET 2018
# 1 01:15  Thu Dec 13 01:15 CET 2018
# position 9826    41
# 2 01:16  Thu Dec 13 01:16 CET 2018
# position 9851    39
