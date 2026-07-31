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
sample_data1 = """
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
"""
sample_data2 = sample_data1


# %% [markdown]
# # Parse

# %%
def parse_line(line):
    h, *n = line.replace(",", " ").split()
    return h, tuple(map(int, n))

def parse(inp):
    return seq(inp.strip().split("\n")).map(parse_line).list()


# %% [markdown]
# # Process

# %%
@cache
def decode(springs, rules):
    if not rules:
        return bool("#" not in springs)

    if not springs:
        return 0

    s = springs[0]
    result = 0

    if s in ".?":
        result += decode(springs[1:], rules) # this covers reults of skipping first char

    if s in "#?": # this coversthe  possibility that the next spring sequence starts at this char
        r = rules[0]

        if (
            r <= len(springs) # sequence will fit in remaining springs
            and "." not in springs[:r] # no .s in first r chars of springs, means all either # or ?
            and (springs[r] != "#") # and char after r is not # (we padded at end with . to avoid extra check
        ):
            result += decode(springs[r + 1:], rules[1:]) # decode springs after r with remaining rules - can skip one bc must be a sapce between sprign groups

    return result

def line_count(line):
    h, counts = line
    return decode(h.strip(".")+".", counts)

def process(parsed):
    ics(parsed)
    return seq(parsed).map(line_count).sum()


# %%
def part1(inp):
    parsed = parse(inp)
    result = process(parsed)
    print_result(result)


# %%
def part2(inp):
    parsed = parse(inp)
    parsed = [("?".join([h]*5), n*5) for h, n in parsed]
    result = process(parsed)
    print_result(result)


# %% [markdown]
# # Sample data

# %%
insert_sample_functions(False, globals())
part1(sample_data1)
part2(sample_data2)

# %% [markdown]
# # Actual data

# %% editable=true slideshow={"slide_type": ""}
real_inp = get_aocd_data()
insert_sample_functions(True, globals())
part1(real_inp)
part2(real_inp)
