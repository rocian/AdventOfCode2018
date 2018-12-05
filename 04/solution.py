#!/usr/bin/env python3
# https://adventofcode.com/2018
# --- Day 4: Repose Record ---

# You've sneaked into another supply closet - this time, it's across from the
# prototype suit manufacturing lab. You need to sneak inside and fix the issues
# with the suit, but there's a guard stationed outside the lab, so this is as
# close as you can safely get.

# As you search the closet for anything that might help, you discover that
# you're not the first person to want to sneak in. Covering the walls, someone
# has spent an hour starting every midnight for the past few months secretly
# observing this guard post! They've been writing down the ID of the one guard
# on duty that night - the Elves seem to have decided that one guard was enough
# for the overnight shift - as well as when they fall asleep or wake up while at
# their post (your puzzle input).

# For example, consider the following records, which have already been organized
# into chronological order:

# [1518-11-01 00:00] Guard #10 begins shift
# [1518-11-01 00:05] falls asleep
# [1518-11-01 00:25] wakes up
# [1518-11-01 00:30] falls asleep
# [1518-11-01 00:55] wakes up
# [1518-11-01 23:58] Guard #99 begins shift
# [1518-11-02 00:40] falls asleep
# [1518-11-02 00:50] wakes up
# [1518-11-03 00:05] Guard #10 begins shift
# [1518-11-03 00:24] falls asleep
# [1518-11-03 00:29] wakes up
# [1518-11-04 00:02] Guard #99 begins shift
# [1518-11-04 00:36] falls asleep
# [1518-11-04 00:46] wakes up
# [1518-11-05 00:03] Guard #99 begins shift
# [1518-11-05 00:45] falls asleep
# [1518-11-05 00:55] wakes up

# Timestamps are written using year-month-day hour:minute format. The guard
# falling asleep or waking up is always the one whose shift most recently
# started. Because all asleep/awake times are during the midnight hour (00:00 -
# 00:59), only the minute portion (00 - 59) is relevant for those events.

# Visually, these records show that the guards are asleep at these times:

# Date   ID   Minute
#             000000000011111111112222222222333333333344444444445555555555
#             012345678901234567890123456789012345678901234567890123456789
# 11-01  #10  .....####################.....#########################.....
# 11-02  #99  ........................................##########..........
# 11-03  #10  ........................#####...............................
# 11-04  #99  ....................................##########..............
# 11-05  #99  .............................................##########.....

# The columns are Date, which shows the month-day portion of the relevant day;
# ID, which shows the guard on duty that day; and Minute, which shows the
# minutes during which the guard was asleep within the midnight hour. (The
# Minute column's header shows the minute's ten's digit in the first row and the
# one's digit in the second row.) Awake is shown as ., and asleep is shown as #.

# Note that guards count as asleep on the minute they fall asleep, and they
# count as awake on the minute they wake up. For example, because Guard #10
# wakes up at 00:25 on 1518-11-01, minute 25 is marked as awake.

# If you can figure out the guard most likely to be asleep at a specific time,
# you might be able to trick that guard into working tonight so you can have the
# best chance of sneaking in. You have two strategies for choosing the best
# guard/minute combination.

# Strategy 1: Find the guard that has the most minutes asleep. What minute does
# that guard spend asleep the most?

# In the example above, Guard #10 spent the most minutes asleep, a total of 50
# minutes (20+25+5), while Guard #99 only slept for a total of 30 minutes
# (10+10+10). Guard #10 was asleep most during minute 24 (on two days, whereas
# any other minute the guard was asleep was only seen on one day).

# While this example listed the entries in chronological order, your entries are
# in the order you found them. You'll need to organize them before they can be
# analyzed.

# What is the ID of the guard you chose multiplied by the minute you chose? (In
# the above example, the answer would be 10 * 24 = 240.)
# --- Part Two ---

# Strategy 2: Of all guards, which guard is most frequently asleep on the same
# minute?

# In the example above, Guard #99 spent minute 45 asleep more than any other
# guard or minute - three times in total. (In all other cases, any guard spent
# any minute asleep at most twice.)

# What is the ID of the guard you chose multiplied by the minute you chose? (In
# the above example, the answer would be 99 * 45 = 4455.)


from sys import stdin
import re


begins = re.compile(r'\[\d{4}-(\d+)-(\d+) (\d+):(\d+)\] Guard #(\d+) begins.*')
asleep = re.compile(r'\[\d{4}-(\d+)-(\d+) (\d+):(\d+)\].*asleep')
awake = re.compile(r'\[\d{4}-(\d+)-(\d+) (\d+):(\d+)\].*wakes up')


def read_input():
    # the input is a list of string separated by LF
    slist = [i for i in stdin.read().split('\n') if i]
    # the input is not garantited to be ordered, so we order
    # it. The timestamp is a key for ordering
    # not only by number, but by char too
    slist.sort()
    return slist


def part_one_two(slist):
    guards = dict()
    # parse list and get minutes and ids of each state:
    #       shift    --  create data structure
    #       asleep   --  store minute
    #       wake up  --  calculate and incremente each minute
    #                    between this minute (excluse) and the preceding
    #                    asleep (incluse).
    for i in slist:
        if begins.match(i):  # shift
            shift_log = begins.search(i).groups()
            minute = int(shift_log[3])
            guard_id = int(shift_log[4])
            if guard_id not in guards.keys():
                guards[guard_id] = {'asleep': 0, 'awake': 0, 'total': {}}
                for k in range(60):
                    guards[guard_id]['total'][k] = 0
            continue
        if asleep.match(i):  # asleep
            asleep_log = asleep.search(i).groups()
            minute = int(asleep_log[3])
            guards[guard_id]['asleep'] = minute
            continue
        if awake.match(i):  # wake up
            awake_log = awake.search(i).groups()
            minute = int(awake_log[3])
            guards[guard_id]['awake'] = minute

            for k in range(guards[guard_id]['asleep'], guards[guard_id]['awake']):
                guards[guard_id]['total'][k] += 1

            continue

    # Find the guard that has the most minutes asleep. What minute does that
    # guard spend asleep the most?
    sleepest_id = None
    max_minutes = -1
    for i in guards.keys():
        total = 0
        for k in range(60):
            total += guards[i]['total'][k]
        if total > max_minutes:
            max_minutes = total
            sleepest_id = i

    # for the sleepest_id find the minute that the guard spend asleep the most
    sleepest_minute = -1
    max_times_asleep = -1
    for k in range(60):
        if guards[sleepest_id]['total'][k] > max_times_asleep:
            max_times_asleep = guards[sleepest_id]['total'][k]
            sleepest_minute = k

    # find the most frequently asleep guard on the same minute
    max_frequency = -1
    max_freq_id = None
    max_minute_asleep = -1
    for i in guards.keys():
        for k in range(60):
            freq = guards[i]['total'][k]
            if max_frequency < freq:
                max_frequency = freq
                max_freq_id = i
                max_minute_asleep = k

    return sleepest_minute * sleepest_id, max_minute_asleep * max_freq_id


stringlist = read_input()
bestasleep, best2asleep = part_one_two(stringlist)

print("\n--- Day 04 ---")
print("part 1: answer to part one = {}".format(bestasleep))
print("part 2: answer to part two = {}".format(best2asleep))
print("--------------\n")

# --- Day 04 ---
# part 1: answer to part one = 73646
# part 2: answer to part two = 4727
# --------------
#
# 0 00:37  Wed Dec  5 00:37 CET 2018
# 1 01:08  Wed Dec  5 01:08 CET 2018
# position  11709    634
# 2 01:15  Wed Dec  5 01:15 CET 2018
# position  11747    637
