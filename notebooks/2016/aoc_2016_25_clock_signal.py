# ---

# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.15.2
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% [markdown]
# [Advent of Code 2016 - Day 25](https://adventofcode.com/2016/day/25)

# %% editable=false jupyter={"source_hidden": true}
from utils.aoc_utils import *
if is_notebook():
    print(get_aoc_url())

# %% [markdown]
# # Imports

# %%
# %load_ext autoreload

# %%
from collections import *

from icecream import ic

# %autoreload explicit
# import and reload these automatically
# %aimport aoc_utils, Utilities, iter_utils, seq_extensions
from utils.aoc_utils import * # this includes adding c:\ut to sys.path
from utils.utilities import *
from utils.iter_utils import *
import utils.seq_extensions as seq_extensions # when running standalone, apparently need this import explicitly in main module


# %% [markdown]
# # Parse

# %% [markdown]
# ```
#          cpy a d
#          cpy 15     # a + 170 * 15 (2550) to d, b gets 0, c gets 0c
# label2:  cpy 170     # add 170 * c to d, b gets 0, c gets 0 b
# label3:  in         #  # add b to d, b gets 0c d
#          d         #  #ec b
#          jnz b l  #  #abel3
#                  # dec c
#          jnz c  #
#  label2
# label8:        # a gets original a + (2550)
#  cpy d a
# label9:       # b gets original a + (2550) first time, / 2 after that  cpy a b
#              # loop (b) gets original a + (2550) first time, / 2 after that
#    cpy 0 a
# label         # until b is 0, subtract 1 at a time, inc a every 212: cpy 2 c
# label13:     #   # subtract 2 from b, c gets 2 - b jz b label20
#             #   #        dec b
#            #   #         dec c
#           #   #   jnz c label13           #  * a gets b / 2 ((original a + 170 * 15) /2), b gets 0, c gets remainder of (original a + 2550) / 2
#          inc a
#         #  a = loop/2, c = 2 - loop % 2
#
# b=0 => c=2, a=0
# b=1 => c=1, a=0
# b=2 => c=2, a=1
# b=3 => c=1, a=1
# b=4 => c=2, a=2
#       jmp label12         #
# label20: cpy 2 b
# la    # bel21: jz c lab           #el26
#                     # (b = 2 - (2 - loop % 2) = loop % 2dec b
#          dec c     # b = 2 - c, c = 0
#
#          jmp            # 2 - c = 2 - b % 2 = 2 - b % 2 = 2 - ((original a + 170 * 15) % 2)label21
# label26: out     # loop 0 - (org a + 2550) timesb
#          jnz a lab
# el9
#          jmp label8
#     cpy a d
#     cpy 15 c
# label_A: # add 170 * c to d, b gets 0, c gets 0
#     cpy 170 b
# label_B: # add b to d, b gets 0
#     inc d
#     dec b
#     jnz b label_B
#     dec c
#     jnz c label_A
# label_K:
#     cpy d a
# label_J:
#     nop
#     cpy a b
#     cpy 0 a
# label_F:
#     cpy 2 c
# label_E:
#     //jnz b label_C
#     //jmp label_D
#     jz b label_D
#     nop
# label_C:
#     dec b
#     dec c
#     jnz c label_E
#     inc a
#     jmp label_F
# label_D:
#     cpy 2 b
# label_I:
#     //jnz c label_G
#     //jmp label_H
#     jz c label_H
#     nop
# label_G:
#     dec b
#     dec c
#     jmp label_I
# label_H:
#     nop
#     out b
#     jnz a label_J
#     jmp label_K
# ```

# %%
def parse_line(line):
    return line.split()

def parse(inp):
    return seq(inp.strip().split("\n")).map(parse_line).list()


# %% [markdown]
# # Process

# %%
def run_instructions(parsed, registers):
    def get_val(val):
        try:
            return int(val)
        except:
            return registers[val]

    ics(parsed, len(parsed))
    inst_len = len(parsed)
    ip = 0

    while ip < inst_len:
        inst = parsed[ip]

        #if ip >= 8:
        #    ic(ip, inst, registers)

        match inst:
            case "jnz", chk, val:
                if get_val(chk):
                    ip += get_val(val)
                    continue
            case "cpy", val, reg:
                registers[reg] = get_val(val)
            case "inc", reg:
                registers[reg] += 1
            case "dec", reg:
                registers[reg] -= 1
            case "out", reg:
                ics(get_val(reg))
                yield get_val(reg)
            case _:
                raise Exception(f"Unhandled instruction {inst}")
        ip += 1

    ic(ip)

def pre_label_reduced(lines):
    lines = list(lines)

    for ip, inst in enumerate(lines):
        match inst:
            case "jnz", chk, val:
                if chk == "0":
                    lines[ip] = ["nop"]
                #elif val == "2" and lines[ip+1][0] == "jnz" and lines[ip+1][1] == "1":
                elif chk == "1" and lines[ip-1][0] == "jnz" and lines[ip-1][2] == "2":
                    lines[ip-1] = ["jz", lines[ip-1][1], str(int(val)+1)] # we are the second instruction, have to adjust
                    lines[ip] = ["nop"]

    return lines

def labeled(parsed):
    labeled_lines = [["", inst] for inst in parsed]

    for ip, (label, inst) in enumerate(labeled_lines):
        match inst:
            case jmp, chk, val if jmp in ("jnz", "jmp", "jz"):
                new_ip = ip + int(val)
                new_label = f"label{new_ip}"
                #ic(new_ip, label)
                labeled_lines[ip] = [label, [jmp, chk, new_label]]
                labeled_lines[new_ip][0] = new_label
                #inst[2] = label

    return labeled_lines

def get_repr(labeled_lines):
    return "\n".join(f"[{ip:2}] {label+':' if label else '' :9}{' '.join(inst)}" for ip, (label, inst) in enumerate(labeled_lines))

def get_comp_repr(parsed, labeled_lines):
    return "\n".join(f"{label:9}{' '.join(inst):15}{' '.join(old)}" for old, (label, inst) in zip(parsed, labeled_lines))

def reduced(labeled_lines):
    labeled_lines = list(labeled_lines)

    for ip, (label, inst) in enumerate(labeled_lines):
        match inst:
            case ("jnz", chk, val) | ("jz", chk, val):
                if chk == "1":
                    labeled_lines[ip][1] = ["jmp", val]


    return labeled_lines

def remove_nops(labeled_lines):
    labeled_lines = list(labeled_lines)

    for ip, (label, inst) in enumerate(labeled_lines):
        match inst:
            case ["nop"]:
                if label:
                    assert not labeled_lines[ip+1][0] # make sure not a label in next isnt
                    labeled_lines[ip+1][0] = label

    return [[label, inst] for label, inst in labeled_lines if inst[0] != "nop"]

def process(parsed):
    #ic(parsed)
    ic(len(parsed))

    if 0:
        lines = pre_label_reduced(parsed)
        #print("Reduced 1:")
        #ic(lines)
        #print("\n".join(" ".join(line) for line in lines))
        labeled_lines = labeled(lines)
        #print("Labeled:")
        #print(get_repr(labeled_lines))
        labeled_lines = reduced(labeled_lines)
        #print("Reduced 2:")
        #print(get_repr(labeled_lines))
        #print(get_comp_repr(parsed, labeled_lines))
        labeled_lines = remove_nops(labeled_lines)
        #print("De-nopped:")
        print(get_repr(labeled_lines))


    registers = { "a": -2550+2, "b": 0, "c": 0, "d": 0 }
    #registers = { "a": 2, "b": 0, "c": 0, "d": 0 }
    first = seq(run_instructions(parsed, registers)).take(10).list()
    ic(first)

    length = 10
    compare = seq(cycle([0, 1])).take(length).list()
    ic(compare)

    if 1:
        for n in range(1000):
            registers = { "a": n, "b": 0, "c": 0, "d": 0 }
            #ic(n, registers)
            first = seq(run_instructions(parsed, registers)).take(length).list()
            ic(first)

            if first == compare:
                return n

    return None


# %%
def part1(inp):
    parsed = parse(inp)
    result = process(parsed)
    print_result(result)


# %% [markdown]
# # Actual data

# %% editable=true slideshow={"slide_type": ""}
real_inp = get_aocd_data()
insert_sample_functions(True, globals())
part1(real_inp)
