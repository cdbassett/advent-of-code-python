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
# [Advent of Code 2016 - Day 23](https://adventofcode.com/2016/day/23)

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
# # Sample Data

# %%
if "example" not in dir() or not example:
    example = get_aocd_example()

# %%
sample_data1s = split_example(example)
sample_data1 = sample_data1s[0]
sample_data2 = sample_data1

# %%
print(sample_data1)


# %% [markdown]
# # Parse

# %%
def parse_line(line):
    return line.split()


# %%
def parse(inp):
    return seq(inp.strip().split("\n")).map(parse_line).list()


# %% [markdown]
# # Process

# %%
def toggle(entry):
    if len(entry) == 2:
        entry[0] = "dec" if entry[0] == "inc" else "inc"
    elif len(entry) == 3:
        entry[0] = "cpy" if entry[0] == "jnz" else "jnz"

def process(parsed, registers):
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
        ics(ip, inst, registers)

        match inst:
            case "tgl", val:
                index = ip + get_val(val)

                if 0 <= index < len(parsed):
                    toggle(parsed[index])

            case "jnz", chk, val:
                if get_val(chk):
                    ip += get_val(val)
                    continue
            case "cpy", val, reg:
                if reg in registers:
                    registers[reg] = get_val(val)
            case "inc", reg:
                if reg in registers:
                    registers[reg] += 1
            case "dec", reg:
                if reg in registers:
                    registers[reg] -= 1
            case _:
                raise Exception(f"Unhandled instruction {inst}")

        ip += 1

    ic(ip)
    return registers


# %%
def part1(inp):
    parsed = parse(inp)
    registers = process(parsed, { "a": 7, "b": 0, "c": 0, "d": 0 })
    result = registers["a"]
    print_result(result)


# %%
def part2(inp):
    parsed = parse(inp)
    registers = process(parsed, { "a": 12, "b": 0, "c": 0, "d": 0 })
    result = registers["a"]
    print_result(result)


# %% [markdown]
# # Sample data

# %%
insert_sample_functions(False, globals())
part1(sample_data1) # 3
part2(sample_data2) # 3

# %% [markdown]
# # Actual data

# %% editable=true slideshow={"slide_type": ""}
real_inp = get_aocd_data()
insert_sample_functions(True, globals())
part1(real_inp)
part2(real_inp)
