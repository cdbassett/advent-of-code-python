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


# %% [markdown]
# # Parse

# %%
def parse(inp):
    return inp.strip().split(",")


# %% [markdown]
# # Process

# %%
def hash(s):
    total = 0

    for c in s:
        total += ord(c)
        total *= 17
        total %= 256

    return total

def process(parsed):
    #ics(parsed)
    return seq(parsed).map(hash).sum()


# %%
def part1(inp):
    parsed = parse(inp)
    result = process(parsed)
    print_result(result)


# %% [markdown]
# # Process2

# %%
def box_focus(n, box):
    result = sum(n * nf * v for nf, v in enumerate(box.values(), 1))
    ics(n, result)
    return result

def process2(parsed, box_cnt):
    #ics(parsed)
    boxes = [OrderedDict() for _ in range(box_cnt)]

    for inst in parsed:
        match inst.split("="):
            case label, cnt:
                #ics(label, hash(label), cnt)
                boxes[hash(label)][label] = int(cnt)
            case _:
                label = inst[:-1]
                #ic(label, hash(label))
                boxes[hash(label)].pop(label, None)
        #ics(boxes)

    ics(boxes)
    return sum(starmap(box_focus, enumerate(boxes, 1)))


# %%
def part2(inp, box_cnt):
    parsed = parse(inp)
    result = process2(parsed, box_cnt)
    print_result(result)


# %% [markdown]
# # Sample data

# %%
insert_sample_functions(False, globals())
part1(sample_data1)
part2(sample_data2, 4)

# %% [markdown]
# # Actual data

# %% editable=true slideshow={"slide_type": ""}
real_inp = get_aocd_data()
insert_sample_functions(True, globals())
part1(real_inp)
part2(real_inp, 256)
