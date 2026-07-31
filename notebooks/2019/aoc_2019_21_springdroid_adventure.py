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
# %aimport aoc_utils, Utilities, iter_utils, seq_extensions, func_utils, aoc_2019_intcode
from utils.aoc_utils import * # this includes adding c:\ut to sys.path
from utils.utilities import *
from utils.iter_utils import *
import utils.seq_extensions as seq_extensions # when running standalone, apparently need this import explicitly in main module
from aoc_2019_intcode import process_intcodes, parse_intcodes


# %% [markdown]
# # Parse

# %%
def parse_data(inp):
    return parse_intcodes(inp)


# %% [markdown]
# # Process

# %%
def send_string(s, generator):
    outputs = []

    for c in s:
        outputs.append(generator.send(ord(c)))
    return outputs

def send_and_receive(parsed, s):
    #ics(parsed)
    generator = process_intcodes(parsed)
    outputs = [generator.send(None)]
    outputs.extend(send_string(s, generator))
    outputs.extend(generator)
    outputs = [c for c in outputs if c is not None]
    return outputs

def get_result(outputs):
    try:
        print(sjoin(map(chr, outputs)))
    except ValueError as e:
        return outputs[-1]

inst = \
"""
NOT A J
NOT B T
OR T J
NOT C T
OR T J
AND D J # (!A or !B or !C) and D
WALK
""".strip() + "\n"
#ic(inst)
def process(parsed):
    outputs = send_and_receive(parsed, inst)
    return get_result(outputs)


# %%
def part1(inp):
    parsed = parse_data(inp)
    result = process(parsed)
    print_result(result)


# %% [markdown]
# # Process2

# %%
# still jumps 4 at a time when running
# D must be true
# however need to jump earlier if E is false and H is false (means can't immediately jump again and can't move forward one)
# so added condition is and (E or H)
inst2 = \
"""
NOT A J
NOT B T
OR T J # !A or !B
NOT C T
OR T J # !A or !B or !C
AND D J # (!A or !B or !C) and D
NOT J T
AND J T # T = 0
OR E T # T = E
OR H T # T = E or H
AND T J # (!A or !B or !C) and D and (E or H)
RUN
""".strip() + "\n"
inst2 = sjoin(s.split("#")[0].strip()+"\n" for s in inst2.split("\n"))
#print(inst2)
def process2(parsed):
    outputs = send_and_receive(parsed, inst2)
    return get_result(outputs)


# %%
def part2(inp):
    parsed = parse_data(inp)
    result = process2(parsed)
    print_result(result)


# %% [markdown]
# # Actual data

# %% editable=true slideshow={"slide_type": ""}
real_inp = get_aocd_data()
insert_sample_functions(True, globals())
part1(real_inp)
part2(real_inp)
