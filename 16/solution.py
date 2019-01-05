#!/usr/bin/env python3
# https://adventofcode.com/2018

# --- Day 16: Chronal Classification ---

# As you see the Elves defend their hot chocolate successfully, you go back to
# falling through time. This is going to become a problem.

# If you're ever going to return to your own time, you need to understand how
# this device on your wrist works. You have a little while before you reach your
# next destination, and with a bit of trial and error, you manage to pull up a
# programming manual on the device's tiny screen.

# According to the manual, the device has four registers (numbered 0 through 3)
# that can be manipulated by instructions containing one of 16 opcodes. The
# registers start with the value 0.

# Every instruction consists of four values: an opcode, two inputs (named A and
# B), and an output (named C), in that order. The opcode specifies the behavior
# of the instruction and how the inputs are interpreted. The output, C, is
# always treated as a register.

# In the opcode descriptions below, if something says "value A", it means to
# take the number given as A literally. (This is also called an "immediate"
# value.) If something says "register A", it means to use the number given as A
# to read from (or write to) the register with that number. So, if the opcode
# addi adds register A and value B, storing the result in register C, and the
# instruction addi 0 7 3 is encountered, it would add 7 to the value contained
# by register 0 and store the sum in register 3, never modifying registers 0, 1,
# or 2 in the process.

# Many opcodes are similar except for how they interpret their arguments. The
# opcodes fall into seven general categories:

# Addition:
#     addr (add register) stores into register C the result of adding register A
#          and register B.
#     addi (add immediate) stores into register C the result of adding register
#          A and value B.
# Multiplication:
#     mulr (multiply register) stores into register C the result of multiplying
#          register A and register B.
#     muli (multiply immediate) stores into register C the result of multiplying
#          register A and value B.
# Bitwise AND:
#     banr (bitwise AND register) stores into register C the result of the
#          bitwise AND of register A and register B.
#     bani (bitwise AND immediate) stores into register C the result of the
#          bitwise AND of register A and value B.
# Bitwise OR:
#     borr (bitwise OR register) stores into register C the result of the
#          bitwise OR of register A and register B.
#     bori (bitwise OR immediate) stores into register C the result of the
#          bitwise OR of register A and value B.
# Assignment:
#     setr (set register) copies the contents of register A into register
#          C. (Input B is ignored.)
#     seti (set immediate) stores value A into register C. (Input B is ignored.)
# Greater-than testing:
#     gtir (greater-than immediate/register) sets register C to 1 if value A is
#          greater than register B. Otherwise, register C is set to 0.
#     gtri (greater-than register/immediate) sets register C to 1 if register A
#          is greater than value B. Otherwise, register C is set to 0.
#     gtrr (greater-than register/register) sets register C to 1 if register A
#          is greater than register B. Otherwise, register C is set to 0.
# Equality testing:
#     eqir (equal immediate/register) sets register C to 1 if value A is equal
#          to register B. Otherwise, register C is set to 0.
#     eqri (equal register/immediate) sets register C to 1 if register A is
#          equal to value B. Otherwise, register C is set to 0.
#     eqrr (equal register/register) sets register C to 1 if register A is equal
#          to register B. Otherwise, register C is set to 0.

# Unfortunately, while the manual gives the name of each opcode, it doesn't seem
# to indicate the number. However, you can monitor the CPU to see the contents
# of the registers before and after instructions are executed to try to work
# them out. Each opcode has a number from 0 through 15, but the manual doesn't
# say which is which. For example, suppose you capture the following sample:

# Before: [3, 2, 1, 1]
# 9 2 1 2
# After:  [3, 2, 2, 1]

# This sample shows the effect of the instruction 9 2 1 2 on the
# registers. Before the instruction is executed, register 0 has value 3,
# register 1 has value 2, and registers 2 and 3 have value 1. After the
# instruction is executed, register 2's value becomes 2.

# The instruction itself, 9 2 1 2, means that opcode 9 was executed with A=2,
# B=1, and C=2. Opcode 9 could be any of the 16 opcodes listed above, but only
# three of them behave in a way that would cause the result shown in the sample:

#     Opcode 9 could be mulr: register 2 (which has a value of 1) times register
#     1 (which has a value of 2) produces 2, which matches the value stored in
#     the output register, register 2.

#     Opcode 9 could be addi: register 2 (which has a value of 1) plus value 1
#     produces 2, which matches the value stored in the output register,
#     register 2.

#     Opcode 9 could be seti: value 2 matches the value stored in the output
#     register, register 2; the number given for B is irrelevant.

# None of the other opcodes produce the result captured in the sample. Because
# of this, the sample above behaves like three opcodes.

# You collect many of these samples (the first section of your puzzle
# input). The manual also includes a small test program (the second section of
# your puzzle input) - you can ignore it for now.

# Ignoring the opcode numbers, how many samples in your puzzle input behave like
# three or more opcodes?

# --- Part Two ---

# Using the samples you collected, work out the number of each opcode and
# execute the test program (the second section of your puzzle input).

# What value is contained in register 0 after executing the test program?


from sys import stdin


def addr(r, i):
    # (add register) stores into register C the result of adding register A and
    # register B.
    _, A, B, C = i
    r[C] = r[A] + r[B]
    return r


def addi(r, i):
    # (add immediate) stores into register C the result of adding register A and
    # value B.
    _, A, B, C = i
    r[C] = r[A] + B
    return r


def mulr(r, i):
    # (multiply register) stores into register C the result of multiplying
    # register A and register B.
    _, A, B, C = i
    r[C] = r[A] * r[B]
    return r


def muli(r, i):
    _, A, B, C = i
    r[C] = r[A] * B
    return r


def banr(r, i):
    _, A, B, C = i
    r[C] = r[A] & r[B]
    return r


def bani(r, i):
    _, A, B, C = i
    r[C] = r[A] & B
    return r


def borr(r, i):
    _, A, B, C = i
    r[C] = r[A] | r[B]
    return r


def bori(r, i):
    _, A, B, C = i
    r[C] = r[A] | B
    return r


def setr(r, i):
    _, A, B, C = i
    r[C] = r[A]
    return r


def seti(r, i):
    _, A, B, C = i
    r[C] = A
    return r


def gtir(r, i):
    _, A, B, C = i
    r[C] = int(A > r[B])
    return r


def gtri(r, i):
    _, A, B, C = i
    r[C] = int(r[A] > B)
    return r


def gtrr(r, i):
    _, A, B, C = i
    r[C] = int(r[A] > r[B])
    return r


def eqir(r, i):
    _, A, B, C = i
    r[C] = int(A == r[B])
    return r


def eqri(r, i):
    _, A, B, C = i
    r[C] = int(r[A] == B)
    return r


def eqrr(r, i):
    _, A, B, C = i
    r[C] = int(r[A] == r[B])
    return r


opfunc = [addr, addi, mulr, muli, banr, bani, borr, bori,
          setr, seti, gtir, gtri, gtrr, eqir, eqri, eqrr]


def read_input():
    lines = stdin.read().split('\n')
    cpus = []
    oper = []
    cpue = []
    prg = []
    i = 0
    while i < len(lines):
        l = lines[i]
        if l.startswith('Before'):
            cpus.append([int(x) for x in l[9:-1].split(', ')])
            l = lines[i + 1]
            oper.append([int(x) for x in l.strip().split(' ')])
            l = lines[i + 2]
            cpue.append([int(x) for x in l[9:-1].split(', ')])
            i += 2
        elif l != '':
            prg.append([int(x) for x in l.strip().split(' ')])

        i += 1

    return cpus, oper, cpue, prg


def process(start, operation, stop, identified):
    result = []
    for i, instr in enumerate(operation):
        count = 0
        for o in opfunc:
            if o in identified:
                continue
            ss = [x for x in start[i]]
            if o(ss, instr) == stop[i]:
                count += 1

        result.append(count)

    return result


def process_single(start, operation, stop, identified):
    for j, o in enumerate(opfunc):
        if o in identified:
            continue
        ss = [x for x in start]
        if o(ss, operation) == stop:
            return j


opcode = dict()
identified = []
registers = [0, 0, 0, 0]

start, operation, stop, program = read_input()

result = process(start, operation, stop, identified)

grttwo = [x for x in result if x > 2]
part1 = len(grttwo)

while True:
    # cicle through result, get all ones (index with count == 1)
    result = process(start, operation, stop, identified)
    if sum(result) == 0:
        break
    got = [i for i, x in enumerate(result) if x == 1]
    for i in got:
        # assign the opcode
        icode = process_single(start[i], operation[i], stop[i], identified)
        if icode is not None:
            # add the opcode to identified
            identified.append(opfunc[icode])
            # add the opcode to dict
            opcode[operation[i][0]] = opfunc[icode]

for l in program:
    registers = opcode[l[0]](registers, l)

part2 = registers[0]

print("\n--- Day 16 ---")
print("part 1: answer to part one = {}".format(part1))
print("part 2: answer to part two = {}".format(part2))
print("--------------\n")

# --- Day 16 ---
# part 1: answer to part one = 517
# part 2: answer to part two = 667
# --------------
#
# 0 Sat Jan  5 18:04 CET 2019
#          6726    285
# 1 Sat Jan  5 19:27 CET 2019
# position 6731    283
# 2 Sat Jan  5 20:11 CET 2019
# position 6732    282
