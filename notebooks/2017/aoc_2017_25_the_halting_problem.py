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

# %%
for sample in sample_data1s:
    print(sample)
    print("=======================")

# %% [markdown]
# # Parse

# %%
Action = namedtuple("Action","write,move,state")
State = namedtuple("State","name,actions")

def last(s):
    return s[-1]

def parse_chunk(lines):
    glob = njoin(lines).replace("right","1").replace("left", "-1")
    lines = glob.split("\n")
    nums = string_to_integers(glob)
    stripped = seq(lines).map(rpartial(str.strip, ".:")).list()
    name = stripped[0][-1]

    for n, chunk in seq(nums).grouped(3).enumerate():
        assert chunk[0] == n

    return State(name, tuple(Action(numbers[1], numbers[2], state) for numbers, state in seq(nums).grouped(3).zip(seq(stripped).drop(1).grouped(4).map(sjoin).map(last))))

def parse(inp):
    lines = inp.strip().split("\n")
    steps = string_to_integers(lines[1])
    return steps, seq(lines).split().drop(1).map(parse_chunk).list()


# %% [markdown]
# # Process

# %%
def process(parsed):
    states = dict((state.name, state) for state in parsed[1])
    steps = parsed[0]
    ic(steps)
    ics(states)
    state_letter = "A"
    state = states[state_letter]
    pos = 0
    values = defaultdict(int)

    for step in range(steps):
        cur_val = values[pos]
        action = state.actions[cur_val]
        values[pos] = action.write
        pos += action.move
        state = states[action.state]

    return sum(values.values())


# %%
def part1(inp):
    parsed = parse(inp)
    result = process(parsed)
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
part1(real_inp)
