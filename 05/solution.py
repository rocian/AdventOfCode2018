#!/usr/bin/env python3
# https://adventofcode.com/2018
# --- Day 5: Alchemical Reduction ---

# You've managed to sneak in to the prototype suit manufacturing lab. The Elves
# are making decent progress, but are still struggling with the suit's size
# reduction capabilities.

# While the very latest in 1518 alchemical technology might have solved their
# problem eventually, you can do better. You scan the chemical composition of
# the suit's material and discover that it is formed by extremely long polymers
# (one of which is available as your puzzle input).

# The polymer is formed by smaller units which, when triggered, react with each
# other such that two adjacent units of the same type and opposite polarity are
# destroyed. Units' types are represented by letters; units' polarity is
# represented by capitalization. For instance, r and R are units with the same
# type but opposite polarity, whereas r and s are entirely different types and
# do not react.

# For example:

#     In aA, a and A react, leaving nothing behind.

#     In abBA, bB destroys itself, leaving aA. As above, this then destroys
#     itself, leaving nothing.

#     In abAB, no two adjacent units are of the same type, and so nothing
#     happens.

#     In aabAAB, even though aa and AA are of the same type, their polarities
#     match, and so nothing happens.

# Now, consider a larger example, dabAcCaCBAcCcaDA:

# dabAcCaCBAcCcaDA  The first 'cC' is removed.
# dabAaCBAcCcaDA    This creates 'Aa', which is removed.
# dabCBAcCcaDA      Either 'cC' or 'Cc' are removed (the result is the same).
# dabCBAcaDA        No further actions can be taken.

# After all possible reactions, the resulting polymer contains 10 units.

# How many units remain after fully reacting the polymer you scanned? (Note: in
# this puzzle and others, the input is large; if you copy/paste your input, make
# sure you get the whole thing.)

# --- Part Two ---

# Time to improve the polymer.

# One of the unit types is causing problems; it's preventing the polymer from
# collapsing as much as it should. Your goal is to figure out which unit type is
# causing the most problems, remove all instances of it (regardless of
# polarity), fully react the remaining polymer, and measure its length.

# For example, again using the polymer dabAcCaCBAcCcaDA from above:

#     Removing all A/a units produces dbcCCBcCcD. Fully reacting this polymer
#     produces dbCBcD, which has length 6.

#     Removing all B/b units produces daAcCaCAcCcaDA. Fully reacting this
#     polymer produces daCAcaDA, which has length 8.

#     Removing all C/c units produces dabAaBAaDA. Fully reacting this polymer
#     produces daDA, which has length 4.

#     Removing all D/d units produces abAcCaCBAcCcaA. Fully reacting this
#     polymer produces abCBAc, which has length 6.

# In this example, removing all C/c units was best, producing the answer 4.

# What is the length of the shortest polymer you can produce by removing all
# units of exactly one type and fully reacting the result?


from sys import stdin


def read_input():
    # read and return stripped string of polymer
    return stdin.read().strip()


def part_one(polymer):
    # create a list for all uppercase letters present in string
    letters = list(set([s.upper() for s in polymer]))
    # sort them and create a new string
    letters.sort()
    letters = ''.join(letters)

    newstring = polymer

    changed = True
    while changed:
        # length before applying changes
        before = len(newstring)
        for l in letters:
            one = l.lower() + l
            two = l + l.lower()

            newstring = newstring.replace(one, "")
            newstring = newstring.replace(two, "")

        # length after changes
        after = len(newstring)

        # if there were changes continue loop
        changed = False
        if before != after:
            changed = True

    return len(newstring)


def part_two(polymer):
    # create a list for all uppercase letters present in string
    letters = list(set([s.upper() for s in polymer]))
    # sort them and create a new string
    letters.sort()
    letters = ''.join(letters)

    minimum = len(polymer)
    string = polymer

    for l in letters:
        one = l.lower()
        two = l
        # print(string)
        newstring = string.replace(one, "")
        # print(newstring)
        newstring = newstring.replace(two, "")
        # print(newstring)
        result_len = part_one(newstring)  # list(newstring))
        if result_len < minimum:
            minimum = result_len

        print(one, two, result_len, minimum)

    return minimum


polymer = read_input()
polymer_len = part_one(polymer)
polymer_shorted_len = part_two(polymer)

print("\n--- Day 05 ---")
print("part 1: answer to part one = {}".format(polymer_len))
print("part 2: answer to part two = {}".format(polymer_shorted_len))
print("--------------\n")

# --- Day 05 ---
# part 1: answer to part one = 9562
# part 2: answer to part two = 4934
# --------------
#
# 0 02:53  Thu Dec  6 02:53 CET 2018
# 1 03:27  Thu Dec  6 03:27 CET 2018
# position 14217    825
# 2 03:56  Thu Dec  6 03:56 CET 2018
# position 14313    812
