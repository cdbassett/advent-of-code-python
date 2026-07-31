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
# %aimport aoc_utils, Utilities, iter_utils, seq_extensions
from utils.aoc_utils import * # this includes adding c:\ut to sys.path
from utils.utilities import *
from iter_utils import *
import utils.seq_extensions as seq_extensions # when running standalone, apparently need this import explicitly in main module

# %% [markdown]
# # Sample Data

# %%
if "example" not in dir() or not example:
    example = get_aocd_example()

# %%
sample_data1 = """
0
3
0
1
-3"""
sample_data1s = [sample_data1]
sample_data2 = sample_data1

# %%
print(sample_data1)


# %% [markdown]
# # Parse

# %%
def parse(inp):
    return seq(inp.strip().split("\n")).map(int).list()


# %% [markdown]
# # Process

# %%
def new_ip1(ip, instructions):
    new_ip = ip + instructions[ip]
    instructions[ip] += 1
    return new_ip

def process(parsed, new_ip_func=new_ip1):
    ics(parsed)
    instructions = parsed[:]
    ip = 0

    try:
        for n in count(0):
            ip = new_ip_func(ip, instructions)
            ics(n, instructions)
    except IndexError as e:
        #ics(instructions)
        return n


# %%
def part1(inp):
    parsed = parse(inp)
    result = process(parsed)
    print_result(result)


# %%
def new_ip2(ip, instructions):
    ofs = instructions[ip]
    ics(ofs)
    new_ip = ip + ofs
    instructions[ip] += (-1 if ofs >= 3 else 1)
    return new_ip

def part2(inp):
    parsed = parse(inp)
    result = process(parsed, new_ip2)
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
# 1079899 is too high
