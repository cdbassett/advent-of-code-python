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
for sample in sample_data1s:
    print(sample)
    print("=======================")


# %% [markdown]
# # Parse

# %%
def parse(inp):
    return string_to_integers_list(inp)


# %% [markdown]
# # Process

# %%
def process(lengths, lst, cur_pos = 0, skip_size = 0):
    list_size = len(lst)

    for skip_size, length in enumerate(lengths, skip_size):
        if length > 1:
            use_pos = cur_pos % list_size
            pos_end = (cur_pos + length) % list_size
            #ic(skip_size, length, cur_pos, use_pos, pos_end)

            if pos_end <= use_pos:
                extracted = lst[use_pos:] + lst[:pos_end]
                cutoff = length - pos_end
                rev = list(reversed(extracted))
                #ics("         ", cutoff, extracted, rev)
                lst = rev[cutoff:] + lst[pos_end:use_pos] + rev[:cutoff]
            else:
                lst = lst[:use_pos] + list(reversed(lst[use_pos:pos_end])) + lst[pos_end:]

            #ics("         ", lst)

        cur_pos += length + skip_size

    return lst, cur_pos, skip_size+1


# %%
def part1(inp, list_size = 256):
    parsed = parse(inp)
    lst = list(range(list_size))
    lengths = parsed
    ics(lengths)
    ic(list_size)
    result, _, _ = process(lengths, lst)
    print_result(result[0] * result[1])


# %% [markdown]
# # Process2

# %%
def to_hex(n):
    return  f'{n:02x}'

def process2(parsed, list_size = 256):
    ics(parsed)
    lst = list(range(list_size))
    lengths = parsed + [17, 31, 73, 47, 23]
    ics(lengths)
    ic(list_size)
    cur_pos, skip_size = 0, 0

    for n in range(64):
        lst, cur_pos, skip_size = process(lengths, lst, cur_pos, skip_size)

    #ics(seq([65, 27, 9, 1, 4, 3, 40, 50, 91, 7, 6, 0, 2, 5, 68, 22]).grouped(16).map(partial(reduce, operator.xor)))

    sparse_hash = seq(lst).grouped(16).map(partial(reduce, operator.xor))
    ics(sparse_hash)
    return sjoin(seq(lst).grouped(16).map(partial(reduce, operator.xor)).map(to_hex))


# %%
def part2(inp, list_size = 256):
    ics(inp)
    parsed = map_list(ord, inp.strip())
    result = process2(parsed, list_size)
    print_result(result)


# %% [markdown]
# # Sample data processing

# %%
insert_sample_functions(False, globals())

for sample_data1 in sample_data1s:
    if sample_data1:
        part1(sample_data1, 5)

part2(sjoin(map(chr, [3, 4, 1, 5])))
part2("")
part2("AoC 2017")
part2("1,2,3")
part2("1,2,4")
part2(sample_data2)

# %% [markdown]
# # Actual data

# %% editable=true slideshow={"slide_type": ""}
real_inp = get_aocd_data()
insert_sample_functions(True, globals())
part1(real_inp)
part2(real_inp)
# 5544 is too low
