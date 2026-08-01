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

import sympy as sp
from icecream import ic

# %autoreload explicit
# import and reload these automatically
# %aimport aoc_utils, Utilities, iter_utils, seq_extensions, func_utils, aoc_2018_computer
from utils.aoc_utils import * # this includes adding c:\ut to sys.path
from utils.utilities import *
from utils.iter_utils import *
import utils.seq_extensions as seq_extensions # when running standalone, apparently need this import explicitly in main module
from aoc_2018_computer import *
import aoc_2018_computer

# %% [markdown]
# # Sample Data

# %%
if "example" not in dir() or not example:
    example = get_aocd_example()

# %%
sample_data1s = split_example(example)
sample_data1 = sample_data1s[0]
sample_data2 = sample_data1


# %% [markdown]
# # Parse

# %%
def parse(inp):
    return parse_instructions(inp)


# %% [markdown]
# # Process

# %%
def get_f(instructions, ip_idx, registers):
    for registers in aoc_2018_computer.run_instructions_with_ip_gen(instructions, ip_idx, registers):
        if registers[ip_idx] == 1:
            ic(registers[F])
            return registers[F]

def process(parsed):
    ic(len(parsed))
    ic(len(all_instructions))
    ics(parsed)
    ip_idx, instructions = parsed
    ics(instructions)
    registers = [0] * 6
    aoc_2018_computer.run_instructions_with_ip(instructions, ip_idx, registers)
    ic(registers)
    return registers[0]


# %%
def part1(inp):
    parsed = parse(inp)
    result = process(parsed)
    print_result(result)


# %% [markdown]
# # Process2

# %%
"""
A = 0
for (E = 1; E <= F; E++):
    for (B = 1; B <= F; B++):
        if F == E * B:
            A += E
"""

# %%
A, B, C, D, E, F = range(6)

def all_factors(factor_f):
    factors = sp.factorint(factor_f)
    ic(factor_f, factors)
    #return list(combinations((f for f, cnt in factors.items() for n in range(cnt)), 2))
    af = list(f for f, cnt in factors.items() for n in range(cnt))+[1, factor_f]
    ic(af)
    combos = list(combinations(af, len(af)-1))
    ic(combos)
    return sum(af)

def process2(parsed):
    ip_idx, instructions = parsed

    factor_f = ic(get_f(instructions, ip_idx, [0] * 6))
    ic(all_factors(factor_f))

    registers = [0] * 6
    registers[0] = 1
    factor_f = get_f(instructions, ip_idx, registers)
    return ic(all_factors(factor_f))


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

# %% [markdown]
# # Actual data

# %% editable=true slideshow={"slide_type": ""}
real_inp = get_aocd_data()
insert_sample_functions(True, globals())

part1(real_inp) # 1482
part2(real_inp) # 14068560, sum of factors

# %% [markdown]
# # Analysis

# %%
import aoc_2018_computer
parsed = parse(real_inp)
ip_idx, instructions = parsed
ic(ip_idx)
aoc_2018_computer.analyze_instructions(instructions, ip_idx)

