from operator import itemgetter
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
from aoc_utils import *
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
from aoc_utils import * # this includes adding c:\ut to sys.path
from Utilities import *
from iter_utils import *
import seq_extensions # when running standalone, apparently need this import explicitly in main module

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
    return inp.strip().split(",")


# %% [markdown]
# # Process

# %%
def dance(parsed, programs):
    programs = list(programs)

    for inst in parsed:
        c, rest = head_tail(inst)
        #ics(c, rest, rest.split("/"), string_to_integers_list(rest))

        match [c] + rest.split("/") + string_to_integers_list(rest):
            case "s", _, spin:
                #ics(spin)
                programs = programs[-spin:] + programs[:-spin]
            case "x", _, _, p1, p2:
                #ics(p1, p2)
                programs[p1], programs[p2] = programs[p2], programs[p1]
            case "p", a, b:
                #ics(a, b)
                p1 = programs.index(a)
                p2 = programs.index(b)
                programs[p1], programs[p2] = programs[p2], programs[p1]
            case _:
                raise Exception(f"unknown inst {c}: {rest}")
        #ics(sjoin(programs))

    return sjoin(programs)

def process(parsed, program_count):
    programs =sjoin(seq.range(program_count).map(partial(operator.add, ord("a"))).map(chr))
    ics(parsed, programs)
    return dance(parsed, programs)


# %%
def part1(inp, program_count):
    parsed = parse(inp)
    result = process(parsed, program_count)
    print_result(result)


# %% [markdown]
# # Process2

# %%
def process2(parsed, program_count):
    def state_by_index(idx):
        return first_element(k for k, v in seen.items() if v == idx)

    programs =sjoin(seq.range(program_count).map(partial(operator.add, ord("a"))).map(chr))
    ics(parsed, programs)
    seen = { }
    cycles = 1000000000

    for idx in range(cycles):
        programs = dance(parsed, programs)

        if programs in seen:
            break

        seen[programs] = idx

    first_idx_of_cycle = seen[programs]
    cycle_length = idx - first_idx_of_cycle
    final_cycle_idx = (cycles - 1 - first_idx_of_cycle) % (cycle_length) + first_idx_of_cycle
    ic(idx, first_idx_of_cycle, cycle_length, final_cycle_idx)
    final_programs = state_by_index(final_cycle_idx)
    return final_programs


# %%
def part2(inp, program_count):
    parsed = parse(inp)
    result = process2(parsed, program_count)
    print_result(result)


# %% [markdown]
# # Sample data processing

# %%
insert_sample_functions(False, globals())

for sample_data1 in sample_data1s:
    part1(sample_data1, 5)

part2(sample_data2, 5)

# %% [markdown]
# # Actual data

# %% editable=true slideshow={"slide_type": ""}
real_inp = get_aocd_data()
insert_sample_functions(True, globals())
part1(real_inp, 16)
part2(real_inp, 16)
