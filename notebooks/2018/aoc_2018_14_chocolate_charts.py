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
def parse(inp):
    return inp.strip()


# %% [markdown]
# # Process

# %%
def new_recipes(a, b):
    s = a + b

    if s >= 10:
        return [s // 10, s % 10]

    return [s]

def sect(r, sp):
    return f"{sp[0]}{r}{sp[1]}"

def repr(pos_a, pos_b, recipes):
    sep = { pos_a: "()", pos_b: "[]" }
    #sjoin(f"{sp[0]}{r}{sp[1]}" for n, r in recipes if (sp := sep.get(n, "  ")))
    return sjoin(sect(r, sep.get(n, "  ")) for n, r in enumerate(recipes))

def generate():
    recipes = [3, 7]
    a, b = recipes
    pos_a, pos_b = 0, 1

    while True:
        recipes += new_recipes(a, b)
        pos_a = (pos_a + 1 + a) % len(recipes)
        pos_b = (pos_b + 1 + b) % len(recipes)
        a, b = recipes[pos_a], recipes[pos_b]
        #ics(pos_a, a, pos_b, b, recipes)
        #ics(repr(pos_a, pos_b, recipes))
        yield recipes

def process(parsed):
    ics(parsed)
    parsed = int(parsed)
    needed = 2 + parsed + 10

    for recipes in generate():
        if len(recipes) >= needed:
            return sjoin(map(str, recipes[parsed:parsed + 10]))


# %%
def part1(inp):
    parsed = parse(inp)
    result = process(parsed)
    print_result(result)


# %% [markdown]
# # Process2

# %%
def process2(parsed):
    #ics(parsed)
    needed = maplist(int, parsed)
    ics(needed)
    checked = 0
    nl = len(needed)

    for step, recipes in enumerate(generate()):
        until = len(recipes) - nl
        #ics(step, until, recipes[checked:])

        #while checked < until:
        for checked in range(checked, until):
            #ics("    ", checked, recipes[checked:checked+nl])
            if recipes[checked:checked+nl] == needed:
                return checked

    return None


# %%
def part2(inp):
    parsed = parse(inp)
    result = process2(parsed)
    print_result(result)


# %% [markdown]
# # Sample data processing

# %%
insert_sample_functions(False, globals())

for sample_data1 in sample_data1s[:4]:
    part1(sample_data1)

for sample_data1 in sample_data1s[4:]:
    part2(sample_data1[:5])

# %% [markdown]
# # Actual data

# %% editable=true slideshow={"slide_type": ""}
real_inp = get_aocd_data()
insert_sample_functions(True, globals())
part1(real_inp) # 8610321414
part2(real_inp)
