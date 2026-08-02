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
# [Advent of Code 2021 - Day 8](https://adventofcode.com/2021/day/8)

# %% editable=false
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
from z3 import *

# %autoreload explicit
# import and reload these automatically
# %aimport aoc_utils, Utilities, iter_utils, seq_extensions, func_utils
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
    def seg_index(c):
        return (ord(c) - ord("a") + 1)

    def segments_sum(number_segment):
        return sum(seg_index(c) for c in number_segment)
        
    #ics(parsed)
    patterns, outputs = parsed
    segments = "abcdefg"
    seg_count = len(segments)
    seg_range = range(seg_count)
    
    lcd_number_segments = [
        "abcefg", # 0
        "cf", # 1
        "acdeg", # 2
        "acdfg", # 3
        "bcdf", # 4
        "abdfg", # 5
        "abdefg", # 6
        "acf", # 7
        "abcdefg", # 8
        "abcdfg", # 9
        ]

    number_segments_by_length = seq(lcd_number_segments).group_by(len)
    ics(number_segments_by_length)
    digit_by_pattern = dict(zip(lcd_number_segments, range(10)))
    ics(digit_by_pattern)
    number_segment_sums_by_length = number_segments_by_length.map(itemgetter(0)).zip(number_segments_by_length.map(itemgetter(1)).level2_map_tuple(segments_sum)).list()
    #number_segment_sums_by_length = seq(lcd_number_segments).map(len).zip(seq(lcd_number_segments).map(segments_sum))).group_by(itemgetter(0))
    ics(number_segment_sums_by_length)
    res = 0
    
    for line_patterns, line_outputs in zip(patterns, outputs):
        length_mapping = seq(line_patterns).group_by(len).dict() # length of scrambled pattern -> list of sets of scrambled patterns with that length
        X = [ Int(c) for c in segments ]
        X_by_char = dict(zip(segments, X))
        s = Solver()
        s.add(Distinct(X))
        s.add([And(X[i] > 0, X[i] <= seg_count) for i in seg_range]) # use 1-based bc we're setting conditions with sums, and we want "a" to count
        
        for l, number_segment_sums in number_segment_sums_by_length:
            scrambled_segments = length_mapping[l]
            #ics(l, length_mapping[l], number_segment_sums)
            
            for scrambled_segment in scrambled_segments:
                summand = sum(X_by_char[c] for c in scrambled_segment)
                s.add(Or([summand == number_segment_sum for number_segment_sum in number_segment_sums]))
                
            #s.add(Or([sum(X_by_char[c] for c in scrambled_segment) == sum(seg_index(c) for c in number_segment) for scrambled_segment, number_segment in product(scrambled_segments, number_segments)]))
            
        #ics(s)
        
        if s.check() == sat:
            m = s.model()
            #print(m)
        else:
            print("failed to solve")
            return

        #lookup = dict((segments[m[X[i]].as_long() - 1], c) for i, c in zip(seg_range, segments))
        lookup = dict((c, segments[m[X[i]].as_long() - 1]) for i, c in zip(seg_range, segments))
        ics(lookup)
        ics(line_outputs)
        #for line_output in line_outputs:
        #    ics(line_output, sjoin(sorted(lookup[c] for c in line_output)))
        output = sjoin(str(digit_by_pattern[sjoin(sorted(lookup[c] for c in line_output))]) for line_output in line_outputs)
        ics(output)
        res += int(output)
    
    return res


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
