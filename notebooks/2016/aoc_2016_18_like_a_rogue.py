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
import iteration_utilities as it_ut
import pyperclip

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
sample_data1 = """
.^^.^.^^^^
"""
sample_data2 = sample_data1


# %% [markdown]
# # Parse

# %%
#Disk = namedtuple("Disk","pos_count,t0pos")

def parse_line(line):
    return line

def parse(inp):
    #return seq(inp.strip().split("\n")).map(parse_line).list()
    return inp.strip()


# %% [markdown]
# # Process

# %%
trap_strings = set("^^.,.^^,^..,..^".split(","))

def calc_char(s):
    return "^" if sjoin(s) in trap_strings else "."

def calc_row(in_row):
    #return in_row
    return seq(list("."+in_row+".")).sliding(3).map(calc_char).make_string("")

def process(parsed, rows):
    ics(parsed)
    #t = seq(list("."+parsed+".")).sliding(3).map(sjoin)
    #ics(t.len(), t.make_string("|"))
    ics(calc_row(parsed))
    map_lines = seq(it_ut.applyfunc(calc_row, parsed)).pad_front(parsed).take(rows).list()
    ics(len(map_lines), map_lines)
    return seq(list("".join(map_lines))).count(lambda c: c == ".")


# %%
def part1(inp, rows):
    parsed = parse(inp)
    result = process(parsed, rows)
    print_result(result)


# %% [markdown]
# # Process2

# %%
def process2(parsed, rows):
    ics(parsed)
    cnt = seq(it_ut.applyfunc(calc_row, parsed)).pad_front(parsed).take(rows).map(lambda s: s.count(".")).sum()
    return cnt

def part2(inp, rows):
    parsed = parse(inp)
    result = process2(parsed, rows)
    print_result(result)


# %% [markdown]
# # Sample data

# %%
insert_sample_functions(False, globals())
part1("..^^.", 3)
part1(".^^.^.^^^^", 10)
part2(sample_data2, 10)

# %% [markdown]
# # Actual data

# %% editable=true slideshow={"slide_type": ""}
real_inp = get_aocd_data()
insert_sample_functions(True, globals())
part1(real_inp, 40)
part2(real_inp, 400000)
