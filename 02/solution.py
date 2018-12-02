#!/usr/bin/env python3
# https://adventofcode.com/2018
# --- Day 2: Inventory Management System ---

# You stop falling through time, catch your breath, and check the screen on the
# device. "Destination reached. Current Year: 1518. Current Location: North Pole
# Utility Closet 83N10." You made it! Now, to find those anomalies.

# Outside the utility closet, you hear footsteps and a voice. "...I'm not sure
# either. But now that so many people have chimneys, maybe he could sneak in
# that way?" Another voice responds, "Actually, we've been working on a new kind
# of suit that would let him fit through tight spaces like that. But, I heard
# that a few days ago, they lost the prototype fabric, the design plans,
# everything! Nobody on the team can even seem to remember important details of
# the project!"

# "Wouldn't they have had enough fabric to fill several boxes in the warehouse?
# They'd be stored together, so the box IDs should be similar. Too bad it would
# take forever to search the warehouse for two similar box IDs..." They walk too
# far away to hear any more.

# Late at night, you sneak to the warehouse - who knows what kinds of paradoxes
# you could cause if you were discovered - and use your fancy wrist device to
# quickly scan every box and produce a list of the likely candidates (your
# puzzle input).

# To make sure you didn't miss any, you scan the likely candidate boxes again,
# counting the number that have an ID containing exactly two of any letter and
# then separately counting those with exactly three of any letter. You can
# multiply those two counts together to get a rudimentary checksum and compare
# it to what your device predicts.

# For example, if you see the following box IDs:

#     abcdef contains no letters that appear exactly two or three times.
#     bababc contains two a and three b, so it counts for both.
#     abbcde contains two b, but no letter appears exactly three times.
#     abcccd contains three c, but no letter appears exactly two times.
#     aabcdd contains two a and two d, but it only counts once.
#     abcdee contains two e.
#     ababab contains three a and three b, but it only counts once.

# Of these box IDs, four of them contain a letter which appears exactly twice,
# and three of them contain a letter which appears exactly three
# times. Multiplying these together produces a checksum of 4 * 3 = 12.

# What is the checksum for your list of box IDs?

# --- Part Two ---

# Confident that your list of box IDs is complete, you're ready to find the
# boxes full of prototype fabric.

# The boxes will have IDs which differ by exactly one character at the same
# position in both strings. For example, given the following box IDs:

# abcde
# fghij
# klmno
# pqrst
# fguij
# axcye
# wvxyz

# The IDs abcde and axcye are close, but they differ by two characters (the
# second and fourth). However, the IDs fghij and fguij differ by exactly one
# character, the third (h and u). Those must be the correct boxes.

# What letters are common between the two correct box IDs? (In the example
# above, this is found by removing the differing character from either ID,
# producing fgij.)


from sys import stdin


def read_input():
    # the input is a list of string separated by LF
    slist = [i for i in stdin.read().split()]
    return slist


def part_one(slist):
    # count if the strings in list contains at least
    # a letter repeated two or three times
    ndouble = 0
    ntriple = 0
    for i in slist:
        letters = list(i)
        frequency = dict()
        for l in letters:
            if l in frequency.keys():
                frequency[l] += 1
            else:
                frequency[l] = 1

        # we should count frequency 2 and three only one time ignoring repetitions
        count2 = True
        count3 = True
        for l in letters:
            if frequency[l] == 2 and count2:
                ndouble += 1
                count2 = False

            if frequency[l] == 3 and count3:
                ntriple += 1
                count3 = False

    # and return a checksum that is the product of the 2,3-repetitions
    return ndouble * ntriple


def part_two(slist):
    # Bonus count howmany loop do we need tho have a repetition
    # of a frequency
    for i in slist:
        letters = list(i)
        # cA = set(i)
        for j in slist:
            diff = 0
            didx = -1
            lettersb = list(j)
            if i == j:
                continue
            for idx, l1 in enumerate(letters):
                if l1 != lettersb[idx]:
                    diff += 1
                    didx = idx
            if diff == 1:
                del letters[didx]
                newstring = ''.join(letters)
                return newstring

    # If we are there then there are not solutions
    return None


stringlist = read_input()
checksum = part_one(stringlist)
commonletters = part_two(stringlist)

print("\n--- Day 02 ---")
print("part 1: checksum = {}".format(checksum))
print("part 2: common letters ID = {}".format(commonletters))
print("--------------\n")

# --- Day 02 ---
# part 1: checksum 8118
# part 2: common letters ID jbbenqtlaxhivmwyscjukztdp
# --------------
# 0 6:00  Sun Dec  2 06:00 CET 2018
# 1 6:15  Sun Dec  2 06:15 CET 2018
# position    485   852
# 2 6:27  Sun Dec  2 06:27 CET 2018
# position   1154   940
