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
from utilities import *
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
Inst = namedtuple("Inst","register,operation,op_val,cond_reg,compare,comp_val")

def parse_line(line):
    parts = line.split()
    return Inst(parts[0], parts[1], int(parts[2]), parts[4], parts[5], int(parts[6]))

def parse(inp):
    return seq(inp.strip().split("\n")).map(parse_line).list()


# %% [markdown]
# # Process

# %%
comparisons = {
    ">": operator.gt,
    "<": operator.lt,
    "<=": operator.le,
    ">=": operator.ge,
    "==": operator.eq,
    "!=": operator.ne,
}

def run_instructions(parsed, registers):
    max_val = 0
    for inst in parsed:
        ics(inst, registers[inst.register], registers[inst.cond_reg])
        if comparisons[inst.compare](registers[inst.cond_reg], inst.comp_val):
            old = registers[inst.register]
            new_val = old + (inst.op_val if inst.operation == "inc" else -inst.op_val)
            registers[inst.register] = new_val
            max_val = max(max_val, new_val)
            ics("    changed", registers[inst.register])

    return max_val

def process(parsed):
    ics(parsed)
    registers = defaultdict(int)
    run_instructions(parsed, registers)
    ics(registers)
    return max(registers.values())


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
    registers = defaultdict(int)
    max_val = run_instructions(parsed, registers)
    return max_val


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
