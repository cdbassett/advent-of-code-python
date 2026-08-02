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

# %% [markdown]
# [Advent of Code 2018 - Day 16](https://adventofcode.com/2018/day/16)

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
# %aimport aoc_utils, Utilities, iter_utils, seq_extensions, func_utils, aoc_2018_computer
from utils.aoc_utils import * # this includes adding c:\ut to sys.path
from utils.utilities import *
from utils.iter_utils import *
import utils.seq_extensions as seq_extensions # when running standalone, apparently need this import explicitly in main module
from aoc_2018_computer import *
import aoc_2018_computer

# %% [markdown]
# # Sample Data

# %%
sample_data1s = \
["""Before: [3, 2, 1, 1]
9 2 1 2
After:  [3, 2, 2, 1]

[0,0,0,0]
"""]
sample_data1 = sample_data1s[0]


# %% [markdown]
# # Parse

# %%
def parse(inp):
    return seq(inp.strip().split("\n")).split().map(njoin).map(string_to_integers).list()


# %% [markdown]
# # Process

# %%
def test_instruction(sample, test_inst):
   #ics(params, test_inst)
    before, inst, after = sample
    registers = before[:]
    inst = inst[:]
    inst[0] = test_inst
    handle_inst(inst, registers)
    #ics(test_inst, before, registers, after)
    return registers == after

# returns count of instructions out of all that this sample could be
def test_instructions(sample):
    return seq(all_instructions).count(partial(test_instruction, sample))

def process(parsed):
    ic(len(parsed))
    ic(len(all_instructions))
    #ic(parsed)
    # ignore instructions at the end
    samples = parsed[:-1]
    #assert all(seq(samples).map(test_instructions))
    ic(seq(samples).map(test_instructions).count(lambda c: c == 1))
    return seq(samples).map(test_instructions).count(lambda c: c >= 3)


# %%
def part1(inp):
    parsed = parse(inp)
    result = process(parsed)
    print_result(result)


# %% [markdown]
# # Process2

# %%
def determine_matching_instructions(check_instructions, sample):
    return seq(check_instructions).where(partial(test_instruction, sample)).list()

def process2(parsed):
    unknown = set(all_instructions) # strings
    discovered = {} # opcode -> inst
    samples, program = parsed[:-1], parsed[-1]
    #ic(samples)
    ic(len(program))

    for iteration in count():
        ic(iteration, len(unknown))
        use_samples = [sample for sample in samples if sample[1][0] not in discovered]
        # determine samples that only match one instruction
        for matching_insts, sample in seq(samples).map(partial(determine_matching_instructions, unknown)).zip(samples):
            if len(matching_insts) == 1:
                #ic(matching_insts, sample)
                instruction, opcode = matching_insts[0], sample[1][0]
                unknown.remove(instruction)
                discovered[opcode] = instruction

        if not unknown:
            #ic(discovered)
            break

    converted_program = [(discovered[opcode], *rest) for opcode, *rest in program]
    registers = [0] * 4
    aoc_2018_computer.run_instructions(converted_program, registers)
    return registers[0]


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

# %% [markdown]
# # Actual data

# %% editable=true slideshow={"slide_type": ""}
real_inp = get_aocd_data()
insert_sample_functions(True, globals())
part1(real_inp) # 563
part2(real_inp) # 629
