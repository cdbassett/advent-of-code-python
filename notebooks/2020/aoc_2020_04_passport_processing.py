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
# [Advent of Code 2020 - Day 4](https://adventofcode.com/2020/day/4)

# %% editable=false jupyter={"source_hidden": true}
from utils.aoc_utils import *
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

# %autoreload explicit
# import and reload these automatically
# %aimport aoc_utils, Utilities, iter_utils, seq_extensions, func_utils
from utils.aoc_utils import * # this includes adding c:\ut to sys.path
from utils.utilities import *
from utils.iter_utils import *
import utils.seq_extensions # when running standalone, apparently need this import explicitly in main module

# %% [markdown]
# # Sample Data

# %%
if "example" not in dir() or not example:
    example = get_aocd_example()

# %%
example

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
def parse_line(lines):
    return seq(" ".join(lines).split()).map(colon_splitter).dict()

def parse_data(inp):
    return seq(inp.strip().split("\n")).split().map(parse_line).list()


# %% [markdown]
# # Process

# %%
req_fields = \
"""byr (Birth Year)
iyr (Issue Year)
eyr (Expiration Year)
hgt (Height)
hcl (Hair Color)
ecl (Eye Color)
pid (Passport ID)
cid (Country ID)"""
req_fields = seq(req_fields.strip().split("\n")).map(functools.partial(str.split, maxsplit=1)).dict()
del req_fields["cid"]
req_fields_set = set(req_fields.keys())

def passport_contains_fields(pp):
    return len(req_fields_set - set(pp.keys())) == 0

def process(parsed):
    #ics(parsed)
    return seq(parsed).count(passport_contains_fields)


# %%
def part1(inp):
    parsed = parse_data(inp)
    result = process(parsed)
    print_result(result)


# %% [markdown]
# # Process2

# %%
validations = {
    "byr": lambda v: 1920 <= int(v) <= 2002
    ,"iyr": lambda v: 2010 <= int(v) <= 2020
    ,"eyr": lambda v: 2020 <= int(v) <= 2030
    ,"hgt": lambda v: (m := re.match(r"(\d+)cm$", v)) and 150 <= int(m.group(1)) <= 193 or (m := re.match(r"(\d+)in$", v)) and 59 <= int(m.group(1)) <= 76
    ,"hcl": lambda v: re.match(r"#[0-9a-f]{6}$", v)
    ,"ecl": lambda v: re.match(r"(amb|blu|brn|gry|grn|hzl|oth)$", v)
    ,"pid": lambda v: re.match(r"[0-9]{9}$", v)
}

def passport_is_valid(pp):
    if not passport_contains_fields(pp):
        return False

    return all(validations[key](pp[key]) for key in req_fields)

def process2(parsed):
    #ics(parsed)
    return seq(parsed).count(passport_is_valid)


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
part1(real_inp)
part2(real_inp)
