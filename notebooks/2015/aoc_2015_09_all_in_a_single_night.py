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
sample_data1 = sample_data1s[0]
sample_data2 = sample_data1

# %%
for sample in sample_data1s:
    print(sample)
    print("=======================")

# %% [markdown]
# # Parse

# %%
Route = namedtuple("Route","frm,to,dist")

def parse_line(line):
    parts = line.split()
    return Route(parts[0], parts[2], int(parts[4]))

def parse_data(inp):
    return seq(inp.strip().split("\n")).map(parse_line).list()


# %% [markdown]
# # Process

# %%
def setup(parsed, func):
    def best_city_dist(city, remaining_cities):
        if len(remaining_cities) == 1:
            return distances[city, remaining_cities[0]]
            
        return func(distances[city, test_city] + best_city_dist(test_city, other_cities) for test_city, other_cities in tuples_without(remaining_cities))
        
    distances = defaultdict(int) # to allow first iteration where starting city is not provided
    cities = set()
    
    for city_a, city_b, dist in parsed:
        distances[city_a, city_b] = dist
        distances[city_b, city_a] = dist
        cities.add(city_a)
        cities.add(city_b)
        
    return tuple(cities), best_city_dist

def process(parsed):
    cities, best_city_dist = setup(parsed, min)
    return best_city_dist(None, cities)


# %%
def part1(inp):
    parsed = parse_data(inp)
    result = process(parsed)
    print_result(result)


# %%
def process2(parsed):
    cities, best_city_dist = setup(parsed, max)
    return best_city_dist(None, cities)


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
part1(real_inp)
part2(real_inp)

# %% [markdown]
# # Others' solutions
