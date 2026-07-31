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
import os
import sys
from collections import *
import re
import math

from icecream import ic
import iteration_utilities as it_ut
from z3 import *

# %autoreload explicit
# import and reload these automatically
# %aimport aoc_utils, Utilities, iter_utils, seq_extensions, func_utils
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
    def char_bit(c):
        return 1 << (ord(c) - ord("a"))
        
    def pattern_bits(pattern):
        return seq(list(pattern)).map(char_bit).reduce(operator.or_)

    def is_power_of_two(x):
        return And(x != 0, 0 == (x & (x - 1)))
        
    def z3_bitwise_or(v):
        first, *rest = v
        expr = first

        for r in rest:
            expr = expr | r
            
        return expr            

    def z3_bitwise_and(v):
        first, *rest = v
        expr = first

        for r in rest:
            expr = expr & r
            
        return expr            

    
    ics(parsed)
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

    #number_segments_by_length = seq(lcd_number_segments).map(len).zip(lcd_number_segments)
    number_segments_by_length = seq(lcd_number_segments).enumerate().group_by(lambda p: len(p[1]))
    ics(number_segments_by_length)
    number_segment_bit_patterns_by_length = number_segments_by_length.smap(lambda l, patterns_for_length: (l, seq(patterns_for_length).map(itemgetter(1)).map(pattern_bits).reduce(operator.or_))).dict()
    ics(number_segment_bit_patterns_by_length)
    numbers_segment_is_in = 0
    
    for line_patterns, line_outputs in zip(patterns, outputs):
        #for p in lcd_number_segments:
            #ics(p, bin(pattern_bits(p)))
        length_mapping = defaultdict(list) # length of scrambled pattern -> list of sets of scrambled patterns with that length
        scrambled_letter_mapping = defaultdict(list) # scrambled letter -> list of indices to scrambled patterns with that letter
    
        for n, pattern in enumerate(line_patterns):
            length_mapping[len(pattern)].append(set(pattern))
    
            for letter in pattern:
                scrambled_letter_mapping[letter].append(n)
    
        # each var is index into segments for actual letter
        X = [ BitVec("X"+c, seg_count) for c in segments ]
        # and the patterns we are given
        P = [ BitVec("P"+str(p), seg_count) for p, pattern in enumerate(line_patterns) ]
        #X = [ Int(c) for c in segments ]
    
        s = Solver()
        
        #s.add([And(X[i] >= 0, X[i] < seg_count) for i in seg_range])
        # each segment should be one bit
        s.add([is_power_of_two(X[i]) for i in seg_range])
        #ics(line_patterns)
        s.add([P[p] == pattern_bits(pattern) for p, pattern in enumerate(line_patterns)])

        patterns_by_length = seq(lcd_number_segments).group_by(len)
        bit_patterns_by_length = patterns_by_length.smap(lambda l, patterns_for_length: (l, seq(patterns_for_length).map(pattern_bits).reduce(operator.or_))).dict()
        ics(bit_patterns_by_length)
        
        for l, number_segments_and_indices in number_segments_by_length:
            combined_bits = seq(number_segments_and_indices).map(itemgetter(1)).map(pattern_bits).reduce(operator.or_)
            ics(l, combined_bits, number_segments_and_indices)
            s.add([X[n] & combined_bits) == X[n] for n in ])
            
        
        # for each segment character there should be one bit that is in the correct characters and not in the others
        for n, seg in enumerate(segments):
            in_digits, out_digits = seq(lcd_number_segments).enumerate().partition(lambda segs: seg in segs[1])

            if in_digits:
                expr = z3_bitwise_and(in_digits.map(lambda d: P[d[0]]))
                s.add((X[n] & (expr)) == X[n])
                
            if out_digits:
                expr = z3_bitwise_or(out_digits.map(lambda d: P[d[0]]))
                s.add((X[n] & (expr)) == 0)
        ics(s)
        
        if s.check() == sat:
            m = s.model()
            print(m)
        else:
            print("failed to solve")
    
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
