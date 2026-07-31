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
sample_data1s = split_example(example)
sample_data1 = sample_data1s[0]
sample_data2 = sample_data1

# %%
print(sample_data1)


# %% [markdown]
# # Parse

# %%
def parse(inp):
    return seq(inp.strip().split()).map(int).list()


# %% [markdown]
# # Process

# %%
def redist(banks):
    #idx = sorted()
    bank_len = len(banks)
    ics(seq(banks).reverse().zip_with_index().sorted(reverse=True))
    idx = bank_len - 1 - seq(banks).reverse().zip_with_index().sorted(reverse=True).take(1).one()[1] # get first element with highest value, reversed zip index means first isntance of highest will have highest index
    bank_cnt = banks[idx]
    ics(banks, idx, bank_cnt)

    new_banks = new_list(banks, idx, 0)
    #ics(new_banks)
    #indexes = list(range(leng)
    next_idx = (idx + 1) % bank_len
    indexes = seq.range(next_idx, bank_len).concat(range(next_idx))
    ics(indexes.list())
    bank_portion, remainder = divmod(bank_cnt, bank_len)
    ics(bank_portion, remainder)

    for n, d_idx in enumerate(indexes):
        new_banks[d_idx] += bank_portion + (1 if n < remainder else 0)

    ics("        ", new_banks)
    return tuple(new_banks)

def process(parsed):
    ics(parsed)
    banks = tuple(parsed)
    seen = set([banks])

    #while (new_banks := redist(banks)) not in seen:
        #seen.add(new_banks)
    for n in count(1):
        banks = redist(banks)

        if banks in seen:
            break

        seen.add(banks)
        #break

    return n


# %%
def part1(inp):
    parsed = parse(inp)
    result = process(parsed)
    print_result(result)


# %% [markdown]
# # Process2

# %%
def process2(parsed):
    ics(parsed)
    banks = tuple(parsed)
    seen = { banks: 0 }

    for n in count(1):
        banks = redist(banks)
        idx = seen.get(banks)

        if idx is not None:
            return n - idx

        seen[banks] = n

    return n


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
#3155 is too high
