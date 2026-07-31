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

# %%
# %load_ext autoreload

# %%
from collections import *
import re

from icecream import ic

# %autoreload explicit
# import and reload these automatically
# %aimport aoc_utils, Utilities, iter_utils, seq_extensions
from utils.aoc_utils import * # this includes adding c:\ut to sys.path
from utils.utilities import *
from iter_utils import *


# %%
def parse_line(line):
    pieces = line.replace("goes to ", "").replace("gives low to ", "").replace("and high to ", "").split()
    parsed = seq(pieces).grouped(2).multimap(str,int).list()
    return parsed


# %%
line = "value 5 goes to bot 2"
line = "bot 1 gives low to output 1 and high to bot 0"
parse_line(line)


# %%
def parse(inp):
    return seq(inp.strip().split("\n")).map(parse_line).list()


# %%
reSearch = re.compile(r"\((\d+)x(\d+)\)")


# %%
def process(inp):
    def get_out(to_str):
        if to_str == "output":
            return outputs
        return bot_vals

    def distribute(bot_num, vals, level = 0):
        ics(bot_num, vals, level)
        #ics(bot_vals)
        def handle_entry(entry, val):
            lo_dict, lo_ndx = entry
            lo_vals = lo_dict[lo_ndx]
            lo_vals.append(val)

            if len(lo_vals) == 2:
                if 0:
                    pass_vals = lo_vals[:]
                    lo_vals[:] = []
                    ics(lo_dict, lo_vals)
                    assert lo_vals is lo_dict[lo_ndx]
                    distribute(lo_ndx, pass_vals, level+1)
                else:
                    distribute(lo_ndx, lo_vals, level+1)

        lo, hi = vals

        if lo > hi:
            hi, lo = lo, hi

        comparisons[lo, hi] = bot_num
        bot_entry = bot_dist.get(bot_num)
        assert(bot_entry)
        lo_entry, hi_entry = bot_entry
        handle_entry(lo_entry, lo)
        handle_entry(hi_entry, hi)
        vals[:] = []


    parsed = parse(inp)
    rcvrs = {}
    outputs = defaultdict(list)
    bot_dist = {} # bot_num -> (dict, lo_ndx), (dict, hi_ndx)
    bot_vals = defaultdict(list) # current values bots are holding
    val_to_bot = {} # which bot a value goes to
    comparisons = {} # (lo, hi) -> bot num

    for inst in parsed:
        match inst:
            case [("value", val), ("bot", bot_num)]:
                ics(val, bot_num)
                bot_vals[bot_num].append(val)
                val_to_bot[val] = bot_num
            case [("bot", bot_num), (to_lo, lo_ndx), (to_hi, hi_ndx)]:
                ics(bot_num, to_lo, lo_ndx, to_hi, hi_ndx)
                bot_dist[bot_num] = (get_out(to_lo), lo_ndx),(get_out(to_hi), hi_ndx)

    ics(val_to_bot)
    #ics(bot_dist)

    step = 1
    while full_bot := first_true(bot_vals.items(), key=lambda item: len(item[1]) == 2):
        bot_num, vals = full_bot
        ics(step, bot_num, vals)
        distribute(bot_num, vals)
        step += 1

    ics(bot_vals)
    ics(outputs)
    return comparisons, outputs


# %%
def part1(inp, val1, val2):
    comparisons, outputs = process(inp)
    result = comparisons[val1, val2]
    print_result(result)


# %%
def part2(inp):
    comparisons, outputs = process(inp)
    result = outputs[0][0] * outputs[1][0] * outputs[2][0]
    print_result(result)


# %% [markdown]
# # Sample data

# %%
insert_sample_functions(False, globals())
samp_inp1 = """
value 5 goes to bot 2
bot 2 gives low to bot 1 and high to bot 0
value 3 goes to bot 1
bot 1 gives low to output 1 and high to bot 0
bot 0 gives low to output 2 and high to output 0
value 2 goes to bot 2
"""
#for line in samp_inp1.strip().split("\n"):
#    part1(line)
part1(samp_inp1, 2, 5)
part2(samp_inp1)

# %% [markdown]
# # Actual data

# %%
real_inp = get_aocd_data()
insert_sample_functions(True, globals())
part1(real_inp, 17, 61)
part2(real_inp)

# %%
