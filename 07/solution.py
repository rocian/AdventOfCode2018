#!/usr/bin/env python3
# https://adventofcode.com/2018
# --- Day 7: The Sum of Its Parts ---

# You find yourself standing on a snow-covered coastline; apparently, you landed
# a little off course. The region is too hilly to see the North Pole from here,
# but you do spot some Elves that seem to be trying to unpack something that
# washed ashore. It's quite cold out, so you decide to risk creating a paradox
# by asking them for directions.

# "Oh, are you the search party?" Somehow, you can understand whatever Elves
# from the year 1018 speak; you assume it's Ancient Nordic Elvish. Could the
# device on your wrist also be a translator? "Those clothes don't look very
# warm; take this." They hand you a heavy coat.

# "We do need to find our way back to the North Pole, but we have higher
# priorities at the moment. You see, believe it or not, this box contains
# something that will solve all of Santa's transportation problems - at least,
# that's what it looks like from the pictures in the instructions." It doesn't
# seem like they can read whatever language it's in, but you can: "Sleigh
# kit. Some assembly required."

# "'Sleigh'? What a wonderful name! You must help us assemble this 'sleigh' at
# once!" They start excitedly pulling more parts out of the box.

# The instructions specify a series of steps and requirements about which steps
# must be finished before others can begin (your puzzle input). Each step is
# designated by a single letter. For example, suppose you have the following
# instructions:

# Step C must be finished before step A can begin.
# Step C must be finished before step F can begin.
# Step A must be finished before step B can begin.
# Step A must be finished before step D can begin.
# Step B must be finished before step E can begin.
# Step D must be finished before step E can begin.
# Step F must be finished before step E can begin.

# Visually, these requirements look like this:


#   -->A--->B--
#  /    \      \
# C      -->D----->E
#  \           /
#   ---->F-----

# Your first goal is to determine the order in which the steps should be
# completed. If more than one step is ready, choose the step which is first
# alphabetically. In this example, the steps would be completed as follows:

#     Only C is available, and so it is done first.
#
#     Next, both A and F are available. A is first alphabetically, so it is done
#     next.
#
#     Then, even though F was available earlier, steps B and D are now also
#     available, and B is the first alphabetically of the three.
#
#     After that, only D and F are available. E is not available because only
#     some of its prerequisites are complete. Therefore, D is completed next.
#
#     F is the only choice, so it is done next.
#
#     Finally, E is completed.
#
# So, in this example, the correct order is CABDFE.
# In what order should the steps in your instructions be completed?

# --- Part Two ---

# As you're about to begin construction, four of the Elves offer to help. "The
# sun will set soon; it'll go faster if we work together." Now, you need to
# account for multiple people started on steps simultaneously. If multiple steps
# are available, workers should still begin them in alphabetical order.

# Each step takes 60 seconds plus an amount corresponding to its letter: A=1,
# B=2, C=3, and so on. So, step A takes 60+1=61 seconds, while step Z takes
# 60+26=86 seconds. No time is required between steps.

# To simplify things for the example, however, suppose you only have help from
# one Elf (a total of two workers) and that each step takes 60 fewer seconds (so
# that step A takes 1 second and step Z takes 26 seconds). Then, using the same
# instructions as above, this is how each second would be spent:

# Second   Worker 1   Worker 2   Done
#    0        C          .
#    1        C          .
#    2        C          .
#    3        A          F       C
#    4        B          F       CA
#    5        B          F       CA
#    6        D          F       CAB
#    7        D          F       CAB
#    8        D          F       CAB
#    9        D          .       CABF
#   10        E          .       CABFD
#   11        E          .       CABFD
#   12        E          .       CABFD
#   13        E          .       CABFD
#   14        E          .       CABFD
#   15        .          .       CABFDE

# Each row represents one second of time. The Second column identifies how many
# seconds have passed as of the beginning of that second. Each worker column
# shows the step that worker is currently doing (or . if they are idle). The
# Done column shows completed steps.

# Note that the order of the steps has changed; this is because steps now take
# time to finish and multiple workers can begin multiple steps simultaneously.

# In this example, it would take 15 seconds for two workers to complete these
# steps.

# With 5 workers and the 60+ second step durations described above, how long
# will it take to complete all of the steps?


from sys import stdin
import re
import numpy as np

extract = re.compile(r'Step (.) must be finished before step (.) can begin.')


def read_input():
    lines = stdin.read().strip().split('\n')
    couples = [extract.search(l).groups() for l in lines]
    return couples


def c2mat(couples):
    # create chain matrix
    # and order of execution
    allq = set()
    for a, b in couples:
        allq.add(a)
        allq.add(b)

    order = list(allq)
    order.sort()

    mat = np.zeros((len(order), len(order)))

    for a, b in couples:
        mat[order.index(a), order.index(b)] = 1

    return mat, order


def part_one(mat, order):
    done = set()       # done items
    solution = []      # chain solution
    while len(done) < len(order):
        # execute job:
        #               - job can be executed if
        #                 - mat column sum to 0
        #                 - job is not already done
        #               - append job index to done set
        #               - append job letter to solution
        #               - nullify matrix rows
        for i in range(len(order)):
            if (mat[:, i].sum() == 0) and (i not in done):
                done.add(i)
                mat[i, :] = 0
                solution.append(order[i])
                break

    return ''.join(solution)


def part_two(mat, order, nw, bigst):
    # configure workers list
    workers = []
    for i in range(nw):
        z = {'t': 0, 'w': -1}
        workers.append(z)

    done = set()             # done items
    started = set()          # items started
    solution = []            # chain solution

    # set time
    seconds = 0

    while len(done) < len(order):

        # free workers: if time (w[t]) is equal seconds,
        #               and time is greater than 0
        #               worker has terminated its job
        #               and can be freed
        #               - append job letter to solution
        #               - append job index to done set
        #               - nullify matrix rows
        #               - set worker as free w[t] = -1
        for w in workers:
            if w['t'] == seconds and w['t'] > 0:
                solution.append(order[w['w']])
                done.add(w['w'])
                mat[w['w'], :] = 0
                w['w'] = -1

        # give job to free workers (w[t]=-1)
        #               - job can be executed if
        #                 - mat column sum to 0
        #                 - job is not already done
        #                 - job is not already started
        #               - associate job to worker
        #               - calculate time of job
        #               - add to list of started job
        for w in workers:
            if w['w'] == -1:
                for i in range(len(order)):
                    if (mat[:, i].sum() == 0) and (i not in done) and (i not in started):
                        w['w'] = i
                        w['t'] = seconds + bigst + 1 + i
                        started.add(i)
                        break

        # print list of workers and relative jobs
        row = []
        for w in workers:
            if w['w'] == -1:
                row.append('.')
            else:
                row.append(order[w['w']])

        print(seconds, '\t'.join(row))

        # increase time
        seconds += 1

    print('solution:' + ''.join(solution))
    return seconds - 1


chain = read_input()
mat, order = c2mat(chain)
part1 = part_one(mat, order)
# mat is changed, so
# recreate mat and order
mat, order = c2mat(chain)
part2 = part_two(mat, order, 5, 60)

print("\n--- Day 07 ---")
print("part 1: answer to part one = {}".format(part1))
print("part 2: answer to part two = {}".format(part2))
print("--------------\n")

# --- Day 07 ---
# part 1: answer to part one = EBICGKQOVMYZJAWRDPXFSUTNLH
# part 2: answer to part two = 906
# --------------
#
# 0 14:45  Sat Dec  8 14:45 CET 2018
# 1 15:12  Sat Dec  8 15:12 CET 2018
# position 8115   2520
# 2 04:31  Sun Dec  9 04:31 CET 2018
# position 9331   2461
