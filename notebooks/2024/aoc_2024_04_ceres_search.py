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
example

# %%
sample_data1 = """
MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX""".strip()
sample_data2 = sample_data1
sample_data1s = [sample_data1]

# %%
for sample in sample_data1s:
    print(sample)
    print("=======================")


# %% [markdown]
# # Parse

# %%
#Disk = namedtuple("Disk","pos_count,t0pos")

def parse_line(line):
    return line

def parse_data(inp):
    return seq(inp.strip().split("\n")).map(parse_line).list()


# %% [markdown]
# # Process

# %%
def setup(parsed):
    W, H = width_height(parsed)
    ic(W, H)
    letters = dict((pos,parsed[pos[1]][pos[0]] ) for pos in product(range(W), range(H)))
    return W, H, letters

def process(parsed):
    def find_word(word, pos, dir):
        #ics(pos, dir)
        
        for c in word:
            if letters.get(pos) != c:
                return False
                
            pos = add_tuple(pos, dir)                
        return True                
            
    ics(parsed)
    W, H, letters = setup(parsed)
    cnt = 0

    for pos in product(range(W), range(H)):
        #ics(pos)
        for dir in diag_neighbors:
            if find_word("XMAS", pos, dir):
                #ics(pos, dir, cnt)
                cnt += 1
                
    return cnt


# %%
def part1(inp):
    parsed = parse_data(inp)
    result = process(parsed)
    print_result(result)


# %%
def process2(parsed):
    def find_x(combo, pos):
        return all(letters.get(add_tuple(pos, (x, y))) == c for x, y, c in combo)
        
    ics(parsed)
    W, H, letters = setup(parsed)

    combos = []
    mass = ["MAS","SAM"]
    
    for words in product(mass, mass):
        ics(words)
        p1 = [(x, x, c1) for c1, c2, x, y in zip(words[0], words[1], range(3), range(2, -1, -1))]
        p2 = [(x, y, c2) for c1, c2, x, y in zip(words[0], words[1], range(3), range(2, -1, -1))]
        combos.append(p1 + p2)
    
    ics(combos)
    cnt = 0

    for pos in product(range(W-1), range(H-1)):
        for combo in combos:
            if find_x(combo, pos):
                ics(combo, pos, cnt)
                cnt += 1
    
    return cnt


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
