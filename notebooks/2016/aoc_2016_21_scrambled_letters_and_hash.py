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
import portion as P

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


# %% [markdown]
# # Parse

# %%
def parse_line(line):
    return seq(line.split("-")).map(int).list()

def parse(inp):
    return inp.strip().split("\n")
    return seq(inp.strip().split("\n")).map(parse_line).list()


# %% [markdown]
# # Process

# %%
def rotate(password, cnt):
    d = deque(password)
    d.rotate(cnt)
    return list(d)

def process(parsed, password):
    ics(parsed, password)
    password = list(password)

    for line in parsed:
        inst = line.split() + string_to_integers_list(line)
        ics(inst)

        match inst:
            case ["swap", "position", *_, pos1, pos2]:
#                ics(pos1, pos2)
                password[pos1], password[pos2] = password[pos2], password[pos1]
            case ["swap", "letter", letter1, *_, letter2]:
                password = seq(password).map(lambda c: letter1 if c == letter2 else letter2 if c == letter1 else c).list()
            case ["rotate", "left", *_, cnt]:
                password = rotate(password, -cnt)
            case ["rotate", "right", *_, cnt]:
                password = rotate(password, cnt)
            case ["rotate", "based", *_, letter]:
                idx = password.index(letter)
                password = rotate(password, idx + 1 + int(idx >= 4))
            case ["reverse", "positions", *_, pos1, pos2]:
                password = password[:pos1] + list(reversed(password[pos1:pos2+1])) + password[pos2+1:]
            case ["move", "position", *_, pos1, pos2]:
                letter = password.pop(pos1)
                password.insert(pos2, letter)
            case _:
                print("Uknown instruction " + line)
        ics(password)

    return sjoin(password)


# %%
def part1(inp, password):
    parsed = parse(inp)
    result = process(parsed, password)
    print_result(result)


# %% [markdown]
# # Process2

# %%
def process2(parsed, password):
    for test in itertools.permutations(password):
        if process(parsed, test) == password:
            return sjoin(test)


# %%
def part2(inp, password):
    parsed = parse(inp)
    result = process2(parsed, password)
    print_result(result)


# %% [markdown]
# # Sample data

# %%
insert_sample_functions(False, globals())
part1(sample_data1, "abcde")

# %% [markdown]
# # Actual data

# %% editable=true slideshow={"slide_type": ""}
real_inp = get_aocd_data()
insert_sample_functions(True, globals())
part1(real_inp, "abcdefgh")
part2(real_inp, "fbgdceah")

