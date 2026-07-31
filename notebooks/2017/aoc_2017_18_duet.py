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

# %% editable=false jupyter={"source_hidden": true}
from aoc_utils import *
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
from aoc_utils import * # this includes adding c:\ut to sys.path
from utilities import *
from iter_utils import *
import seq_extensions # when running standalone, apparently need this import explicitly in main module
import queue

# %% [markdown]
# # Sample Data

# %%
if "example" not in dir() or not example:
    example = get_aocd_example()

# %%
sample_data1s = split_example(example)
sample_data1 = sample_data1s[0]
sample_data2 = """snd 1
snd 2
snd p
rcv a
rcv b
rcv c
rcv d"""

# %%
for sample in sample_data1s:
    print(sample)
    print("=======================")


# %% [markdown]
# # Parse

# %%
def parse_line(line):
    return line.split()

def parse(inp):
    return seq(inp.strip().split("\n")).map(parse_line).list()


# %% [markdown]
# # Process

# %%
def make_get_val(registers):
    def get_val(val):
        try:
            return int(val)
        except:
            return registers.get(val, 0)
    return get_val

def run(instructions, registers):
    get_val = make_get_val(registers)
    #ics(instructions, len(instructions))
    inst_len = len(instructions)
    ip = 0
    freq = None

    while ip < inst_len:
        inst = instructions[ip]
        #ics(ip, inst, registers)

        match inst:
            case "add", reg, val:
                registers[reg] += get_val(val)
            case "mul", reg, val:
                registers[reg] *= get_val(val)
            case "mod", reg, val:
                registers[reg] %= get_val(val)
            case "jgz", chk, val:
                if get_val(chk) > 0:
                    ip += get_val(val)
                    continue
            case "set", reg, val:
                registers[reg] = get_val(val)
            case "snd", val:
                freq = get_val(val)
            case "rcv", val:
                if get_val(val):
                    return freq
            case _:
                raise Exception(f"Unhandled instruction {inst}")

        ip += 1

def process(parsed):
    #ics(parsed)
    return run(parsed, {"p": 0})


# %%
def part1(inp):
    parsed = parse(inp)
    result = process(parsed)
    print_result(result)


# %% [markdown]
# # Process2

# %%
def run2(instructions, registers):
    get_val = make_get_val(registers)

    #ics(instructions, len(instructions))
    inst_len = len(instructions)
    ip = 0
    freq = None
    q = queue.Queue()
    id = registers["p"]

    while ip < inst_len:
        inst = instructions[ip]
        #ics(ip, inst, registers)

        match inst:
            case "add", reg, val:
                registers[reg] += get_val(val)
            case "mul", reg, val:
                registers[reg] *= get_val(val)
            case "mod", reg, val:
                registers[reg] %= get_val(val)
            case "jgz", chk, val:
                if get_val(chk) > 0:
                    ip += get_val(val)
                    continue
            case "set", reg, val:
                registers[reg] = get_val(val)
            case "rcv", reg:
                if not q.empty():
                    rcv = q.get()
                    ics(id, "INPUT from queue", rcv, reg)
                else:
                    ics(id, "INPUT before yield", registers)
                    rcv = (yield) # yields None

                    #if input is None:
                    #    break
                    ics(id, "    INPUT after yield", rcv, reg)

                if rcv is not None:
                    registers[reg] = rcv
            case "snd", val:
                snd = get_val(val)
                ics(id, "OUTPUT", snd)
                rcv = (yield snd)

                if rcv is not None:
                    q.put(rcv)

                ics(id, "    OUTPUT after yield", snd, rcv)
            case _:
                raise Exception(f"Unhandled instruction {inst}")

        ip += 1
    ics(id, registers)

def process2(parsed):
    #ics(parsed)
    prog0 = run2(parsed, {"p": 0})
    prog1 = run2(parsed, {"p": 1})
    #prog0.send(None) # start them
    #prog1.send(None)
    ics("first send")
    a, b = prog0.send(None), prog1.send(None)
    cnt = 0
    i = 0
    ics("begin loop")

        # repeat until both are looking for input
    while (a, b) != (None, None):
        ics(i, a, b)

        if b != None:
            cnt += 1
            # getting None indicates generator was requesting input rather than sending output
        a, b = prog0.send(b), prog1.send(a)
        i += 1

    return cnt


# %%
def part2(inp):
    parsed = parse(inp)
    result = process2(parsed)
    print_result(result)


# %% [markdown]
# # Sample data processing

# %%
insert_sample_functions(False, globals())

for sample_data1 in sample_data1s:
    part1(sample_data1)

part2(sample_data2)

# %% [markdown]
# # Actual data

# %% editable=true slideshow={"slide_type": ""}
real_inp = get_aocd_data()
insert_sample_functions(True, globals())
part1(real_inp)
part2(real_inp)
#ic(real_inp)
# 7366 is too high
