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

# %% pycharm={"is_executing": true}
# %load_ext autoreload

# %%
from collections import *

from icecream import ic, colorize as ic_colorize
#ic.configureOutput(outputFunction=print)
ic.configureOutput(outputFunction=lambda s: print(ic_colorize(s)))
import pyperclip

# %autoreload explicit
# import and reload these automatically
# %aimport aoc_utils, Utilities, iter_utils, seq_extensions
from aoc_utils import * # this includes adding c:\ut to sys.path
from Utilities import *
from iter_utils import *
import seq_extensions # when running standalone, apparently need this import explicitly in main module


# %%
def parse_line(line):
    return line.split()


# %%
def parse(inp):
    return seq(inp.strip().split("\n")).map(parse_line).list()


# %%
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
            case _:
                raise Exception(f"Unhandled instruction {inst}")

        ip += 1

    ic(ip)
    return registers


# %%
def part1(inp):
    parsed = parse(inp)
    registers = process(parsed, { "a": 0, "b": 0, "c": 0, "d": 0 })
    result = registers["a"]
    ics(result)
    print_result(result)


# %%
def part2(inp):
    parsed = parse(inp)
    registers = process(parsed, { "a": 0, "b": 0, "c": 1, "d": 0 })
    result = registers["a"]
    ics(result)
    print_result(result)


# %% [markdown]
# # Sample data

# %%
insert_sample_functions(False, globals())
samp_inp1 = """
cpy 41 a
inc a
inc a
dec a
jnz a 2
dec a
"""
#for line in samp_inp1.strip().split("\n"):
#    part1(line)
part1(samp_inp1)
part2(samp_inp1)

# %% [markdown]
# # Actual data

# %% editable=true slideshow={"slide_type": ""}
real_inp = get_aocd_data()
insert_sample_functions(True, globals())
part1(real_inp)
part2(real_inp)

# %%
