#!/usr/bin/env python3
# https://adventofcode.com/2018
# --- Day 12: Subterranean Sustainability ---

# The year 518 is significantly more underground than your history books
# implied. Either that, or you've arrived in a vast cavern network under the
# North Pole.

# After exploring a little, you discover a long tunnel that contains a row of
# small pots as far as you can see to your left and right. A few of them contain
# plants - someone is trying to grow things in these geothermally-heated caves.

# The pots are numbered, with 0 in front of you. To the left, the pots are
# numbered -1, -2, -3, and so on; to the right, 1, 2, 3.... Your puzzle input
# contains a list of pots from 0 to the right and whether they do (#) or do not
# (.) currently contain a plant, the initial state. (No other pots currently
# contain plants.) For example, an initial state of #..##.... indicates that
# pots 0, 3, and 4 currently contain plants.

# Your puzzle input also contains some notes you find on a nearby table: someone
# has been trying to figure out how these plants spread to nearby pots. Based on
# the notes, for each generation of plants, a given pot has or does not have a
# plant based on whether that pot (and the two pots on either side of it) had a
# plant in the last generation. These are written as LLCRR => N, where L are
# pots to the left, C is the current pot being considered, R are the pots to the
# right, and N is whether the current pot will have a plant in the next
# generation. For example:

#     A note like ..#.. => . means that a pot that contains a plant but with no
#     plants within two pots of it will not have a plant in it during the next
#     generation.

#     A note like ##.## => . means that an empty pot with two plants on each
#     side of it will remain empty in the next generation.

#     A note like .##.# => # means that a pot has a plant in a given generation
#     if, in the previous generation, there were plants in that pot, the one
#     immediately to the left, and the one two pots to the right, but not in the
#     ones immediately to the right and two to the left.

# It's not clear what these plants are for, but you're sure it's important, so
# you'd like to make sure the current configuration of plants is sustainable by
# determining what will happen after 20 generations.

# For example, given the following input:

# initial state: #..#.#..##......###...###

# ...## => #
# ..#.. => #
# .#... => #
# .#.#. => #
# .#.## => #
# .##.. => #
# .#### => #
# #.#.# => #
# #.### => #
# ##.#. => #
# ##.## => #
# ###.. => #
# ###.# => #
# ####. => #

# For brevity, in this example, only the combinations which do produce a plant
# are listed. (Your input includes all possible combinations.) Then, the next 20
# generations will look like this:

#                  1         2         3
#        0         0         0         0
#  0: ...#..#.#..##......###...###...........
#  1: ...#...#....#.....#..#..#..#...........
#  2: ...##..##...##....#..#..#..##..........
#  3: ..#.#...#..#.#....#..#..#...#..........
#  4: ...#.#..#...#.#...#..#..##..##.........
#  5: ....#...##...#.#..#..#...#...#.........
#  6: ....##.#.#....#...#..##..##..##........
#  7: ...#..###.#...##..#...#...#...#........
#  8: ...#....##.#.#.#..##..##..##..##.......
#  9: ...##..#..#####....#...#...#...#.......
# 10: ..#.#..#...#.##....##..##..##..##......
# 11: ...#...##...#.#...#.#...#...#...#......
# 12: ...##.#.#....#.#...#.#..##..##..##.....
# 13: ..#..###.#....#.#...#....#...#...#.....
# 14: ..#....##.#....#.#..##...##..##..##....
# 15: ..##..#..#.#....#....#..#.#...#...#....
# 16: .#.#..#...#.#...##...#...#.#..##..##...
# 17: ..#...##...#.#.#.#...##...#....#...#...
# 18: ..##.#.#....#####.#.#.#...##...##..##..
# 19: .#..###.#..#.#.#######.#.#.#..#.#...#..
# 20: .#....##....#####...#######....#.#..##.

# The generation is shown along the left, where 0 is the initial state. The pot
# numbers are shown along the top, where 0 labels the center pot,
# negative-numbered pots extend to the left, and positive pots extend toward the
# right. Remember, the initial state begins at pot 0, which is not the leftmost
# pot used in this example.

# After one generation, only seven plants remain. The one in pot 0 matched the
# rule looking for ..#.., the one in pot 4 matched the rule looking for .#.#.,
# pot 9 matched .##.., and so on.

# In this example, after 20 generations, the pots shown as # contain plants, the
# furthest left of which is pot -2, and the furthest right of which is pot
# 34. Adding up all the numbers of plant-containing pots after the 20th
# generation produces 325.

# After 20 generations, what is the sum of the numbers of all pots which contain
# a plant?

# --- Part Two ---

# You realize that 20 generations aren't enough. After all, these plants will
# need to last another 1500 years to even reach your timeline, not to mention
# your future.

# After fifty billion (50000000000) generations, what is the sum of the numbers
# of all pots which contain a plant?


from sys import stdin
import re

extract = re.compile(r'Step (.) must be finished before step (.) can begin.')
extract = re.compile(r'Step (.) must be finished before step (.) can begin.')


def read_input():
    # create instruction and notes
    # as list of 0, 1 and as dict {i,r} of
    # input (pattern) and result
    lines = stdin.read().strip().split('\n')
    values = ['.', '#']
    notes = []
    for l in lines:
        if len(l) == 0:
            continue
        if l[0] == 'i':
            ist = l[15:].strip()
            initial_state = []
            for i in ist:
                initial_state.append(values.index(i))

        elif l[0] == '#' or l[0] == '.':
            instl = []
            instruction = l[0:5]
            result = l[9]
            for i in instruction:
                instl.append(values.index(i))

            resul = values.index(result)

            notes.append({'i': instl, 'r': resul})

    return initial_state, notes


def transform(status):
    values = ['.', '#']
    letters = [values[i] for i in status]
    return ''.join(letters)


def part_one(ist, inst, n):

    nist = [i for i in ist]
    # append 30 more palce to left and right of
    # places for pots
    padd = 30
    for i in range(padd):
        nist.insert(0, 0)
    for i in range(padd):
        nist.append(0)

    # uncomment this to print pots stages
    # print(0, '\t', transform(nist))

    for i in range(1, n + 1):
        mist = [0] * len(nist)
        for q in inst:
            for h in range(2, len(nist) - 3):
                if q['i'] == nist[h - 2:h + 3]:
                    mist[h] = q['r']

        nist = [w for w in mist]
        # uncomment this to print pots stages
        # print(i, '\t', transform(nist))

    n = 0
    for i in range(len(nist)):
        n += (i - padd) * nist[i]

    return n


def part_two(ist, inst, n):
    nist = [i for i in ist]
    # append 280 more palce to left and right of
    # places for pots
    padd = 280
    for i in range(padd):
        nist.insert(0, 0)
    for i in range(padd):
        nist.append(0)

    # uncomment this to print pots stages
    # print(0, '\t', transform(nist))

    for i in range(1, n + 1):
        mist = [0] * len(nist)
        for q in inst:
            for h in range(2, len(nist) - 3):
                if q['i'] == nist[h - 2:h + 3]:
                    mist[h] = q['r']

        nist = [w for w in mist]
        # uncomment this to print pots stages
        # print(i, '\t', transform(nist))

    n = 0
    for i in range(len(nist)):
        n += (i - padd) * nist[i]

    return n


first, notes = read_input()
part1 = part_one(first, notes, 20)
# by visual inspection of a prolonged
# part 1 the pattern became constant after 100 generations
#        so we take de difference between 101th and 100th generation
#        and multiply it for the opportune number
part2 = ((part_two(first, notes, 101) - part_two(first, notes, 100)) *
         (50000000000 - 100) + part_two(first, notes, 100))

print("\n--- Day 12 ---")
print("part 1: answer to part one = {}".format(part1))
print("part 2: answer to part two = {}".format(part2))
print("--------------\n")

# --- Day 12 ---
# part 1: answer to part one = 2571
# part 2: answer to part two = 3100000000655
# --------------
#
# 0 22:45  Thu Dec 13 22:45 CET 2018
# 1 00:09  Fri Dec 14 00:09 CET 2018
# position 7046    965
# 2 00:19  Fri Dec 14 00:19 CET 2018
# position 7053    966
