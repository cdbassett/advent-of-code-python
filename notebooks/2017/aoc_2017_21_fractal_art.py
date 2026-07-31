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
def parse_line(line):
    return line.split(" => ")

def parse(inp):
    return seq(inp.strip().split("\n")).map(parse_line).list()


# %% [markdown]
# # Process

# %%
def hash_count(s):
    return sum(1 for c in s if c == "#")

def flip(a):
    return list(reversed(a))

def restring(a):
    return list(map(sjoin, a))

def transpose(a):
    return restring(zip(*a))

    # from / separated string to array of strings
def expand(s):
    return s.split("/")

    # from array of strings to / separated string
def compress(a):
    return "/".join(a)

def chunk_slice(n, chunk_size):
    return slice(n * chunk_size, (n+1) * chunk_size)

def get_chunk(state, x, y, chunk_size):
    #return [line[x*chunk_size:(x+1)*chunk_size] for line in state[y*chunk_size:(y+1)*chunk_size]]
    return [line[chunk_slice(x, chunk_size)] for line in state[chunk_slice(y, chunk_size)]]

# assumes state has col elements as indivial chars. not all in one string
def set_chunk(state, x, y, chunk):
    chunk_size = len(chunk)

    for n, line in enumerate(state[chunk_slice(y, chunk_size)]):
        #ic(n, line)
        line[chunk_slice(x, chunk_size)] = list(chunk[n])


def process(parsed, iterations = 5):
    ics(parsed)
    counts = defaultdict(int)
    transforms = dict() # string -> string (compressed form)

    for f, t in parsed:
        a = expand(f)
        c = f
        #ics(f, a, "========")

        for n in range(4):
            transforms[c] = t
            a = transpose(a)
            #ics(n, a)
            c = compress(a)
            transforms[c] = t
            a = flip(a)
            #ics(n, a)
            c = compress(a)
    #ics(transforms)

    state = expand(".#./..#/###")    # starting state

    for iteration in range(iterations):
        chunk_size = 2 if len(state) % 2 == 0 else 3
        chunk_cnt = len(state) // chunk_size
        ics(iteration, chunk_size, chunk_cnt)
        new_chunk_size = 3 if len(state) % 2 == 0 else 4
        new_state = [[" "] * new_chunk_size * chunk_cnt for _ in range(new_chunk_size * chunk_cnt)]
        #ics(restring(new_state))

        for x, y in product(range(chunk_cnt), range(chunk_cnt)):
            chunk = get_chunk(state, x, y, chunk_size)
            ics(x, y, chunk)
            new_chunk = expand(transforms[compress(chunk)])
            ics(x, y, new_chunk)
            set_chunk(new_state, x, y, new_chunk)

        state = restring(new_state)
        ics(state)

    return sjoin(state).count("#")

        #counts[(hash_count(f), hash_count(t))] += 1
    #ic(counts)


# %%
def part1(inp, iterations):
    parsed = parse(inp)
    result = process(parsed, iterations)
    print_result(result)


# %% [markdown]
# # Sample data processing

# %%
insert_sample_functions(False, globals())

for sample_data1 in sample_data1s:
    part1(sample_data1, 2)

# %% [markdown]
# # Actual data

# %% editable=true slideshow={"slide_type": ""}
real_inp = get_aocd_data()
insert_sample_functions(True, globals())
part1(real_inp, 5)
part1(real_inp, 18)
