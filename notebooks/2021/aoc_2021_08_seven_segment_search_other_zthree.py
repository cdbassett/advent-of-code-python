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

# %% editable=false
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
from z3 import *

# %autoreload explicit
# import and reload these automatically
# %aimport aoc_utils, Utilities, iter_utils, seq_extensions, func_utils
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
sample_data1 = sample_data1s[1]
sample_data2 = sample_data1


# %% [markdown]
# # Parse

# %%
def parse_line(line):
    return line.split("|")

def parse_data(inp):
    #ics(inp)
    if is_sample:
        parsed = seq(inp.strip().split("\n")).grouped(2).map(sjoin).map(parse_line).list()
    else:
        parsed = seq(inp.strip().split("\n")).map(parse_line).list()

    patterns, outputs = zip(*parsed)
    outputs = seq(outputs).map(str.split).list()
    patterns = seq(patterns).map(str.split).list()
    return patterns, outputs


# %% [markdown]
# # Process

# %%
def process(parsed):
    #ics(parsed)
    patterns, outputs = parsed
    output_lengths = Counter(seq(outputs).flatten().map(len))
    checked_counts = [output_lengths.get(n) for n in (2, 3, 4, 7)] # 1, 7, 4, 8
    checked_counts = filter(None, checked_counts)
    result = sum(checked_counts)
    return result


# %%
def part1(inp):
    parsed = parse_data(inp)
    result = process(parsed)
    print_result(result)


# %%
def process2(parsed):
    vals = dict(zip('abcdefg', range(1, 8)))
    inv_vals = dict((v, k) for k, v in vals.items())
    digits = ["abcefg", "cf", "acdeg", "acdfg", "bcdf",
            "abdfg", "abdefg", "acf", "abcdefg", "abcdfg"]
    of_length = seq(digits).group_by(len).dict()
    
    def add_clause(line_pattern, vars_lookup):
        summand = seq([vars_lookup[c] for c in line_pattern]).reduce(operator.add)
        ors = [summand == sum(vals[c] for c in k_) for k_ in of_length[len(line_pattern)]]
        return Or(ors)
        
    def parse(m, vars_lookup, line_output):
        segs = sorted([inv_vals[m[vars_lookup[c]].as_long()] for c in line_output])
        return digits.index(''.join(segs))
        
    def solve_line(line_patterns, line_outputs):
        s = Solver()
        a, b, c, d, e, f, g = vars = Ints('a b c d e f g')
        vars_lookup = dict(zip('abcdefg', vars))
        s.add(Distinct(vars))
            
        for line_pattern in line_patterns:
            s.add(add_clause(line_pattern, vars_lookup))

        ics(s)
        s.check()
        m = s.model()
        ics(m)
        return [parse(m, vars_lookup, line_output) for line_output in line_outputs]

    #ics(parsed)
    patterns, outputs = parsed

    for line_patterns, line_outputs in zip(patterns, outputs):
        res = solve_line(line_patterns, line_outputs)
        print(res)
    
    return None


# %% [markdown]
# # Process2

# %%
def part2(inp):
    parsed = parse_data(inp)
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
#ic(real_inp)
part1(real_inp)
part2(real_inp)

# %% [markdown]
# # Others' solutions
