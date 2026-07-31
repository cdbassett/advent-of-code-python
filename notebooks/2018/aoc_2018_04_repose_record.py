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
# %aimport aoc_utils, Utilities, iter_utils, seq_extensions
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
sample_data1 = sample_data1s[0]
sample_data2 = sample_data1

# %%
for sample in sample_data1s:
    print(sample)
    print("=======================")


# %% [markdown]
# # Parse

# %%
def parse_line(line):
    return string_to_integers_list(line) + line.split()[-1:]

def parse(inp):
    return seq(inp.strip().replace("-", " ").split("\n")).map(parse_line).list()


# %% [markdown]
# # Process

# %%
year, month, day, hour, minute = range(5)
midnight_minutes = 24*60

def minutes(time):
    return time[hour] * 60 + time[minute]

def build_analysis(parsed):
    def add_minutes(start_minutes, end_minutes, id):
        ics("    ", id, start_minutes, end_minutes, end_minutes - start_minutes)
        guard_times[id].update(range(start_minutes, end_minutes))
        guard_sleep_time[cur_guard] += end_minutes - start_minutes

    def add_time(start_time, end_time, id):
        if start_time is not None:
            ics(id, start_time, end_time)

            if end_time[day] > start_time[day]:
                ics(id, start_time, end_time)
                #ics(start_time[day], end_time[day])
                #assert end_time[day] == start_time[day]+1, f"{icf(end_time[day])} != {icf(start_time[day]+1)}"
                #assert end_time[day] == start_time[day]+1, f"{end_time[day]} != {start_time[day]+1)}"
                add_minutes(minutes(start_time), midnight_minutes, id)

                for d in range(start_time[day]+1, end_time[day]):
                    add_minutes(0, midnight_minutes, id)

                add_minutes(0, minutes(end_time), id)
            else:
                add_minutes(minutes(start_time), minutes(end_time), id)

    ic(len(parsed))
    #ics(parsed)

    schedule = sorted(parsed)
    guard_times = defaultdict(Counter) # id -> count of minutes
    guard_sleep_time = defaultdict(int)
    cur_guard = None
    cur_guard_start = None
    ic(schedule[:10])

    for line in schedule:
        time = line[:5]
        work = line[5:]
        #ics(time, work)

        match work:
            case id, "shift":
                add_time(cur_guard_start, time, cur_guard)
                cur_guard = id
                cur_guard_start = None

            case ["asleep"]:
                cur_guard_start = time

            case ["up"]:
                add_time(cur_guard_start, time, cur_guard)
                cur_guard_start = None

    return guard_times, guard_sleep_time

def process(parsed):
    guard_times, guard_sleep_time = build_analysis(parsed)
    ic(len(guard_sleep_time.items()))
    guard = sorted(guard_sleep_time.items(), key=itemgetter(1), reverse=True)[0][0]
    guard_minute = guard_times[guard].most_common(1)[0][0] # most common, minute
    ics(guard, guard_minute)
    #ics(sorted(guard_sleep_time.items(), key=itemgetter(1), reverse=True))
    #ics(guard_times)
    return guard * guard_minute


# %%
def part1(inp):
    parsed = parse(inp)
    result = process(parsed)
    print_result(result)


# %% [markdown]
# # Process2

# %%
def process2(parsed):
    guard_times, guard_sleep_time = build_analysis(parsed)
    sorted_guards = sorted(((cntr.most_common(1)[0], guard_id) for guard_id, cntr in guard_times.items()), reverse = True, key=lambda el: el[0][1])
    ic(sorted_guards[:5])
    guard = sorted_guards[0][1]
    guard_minute = sorted_guards[0][0][0]
    ics(guard, guard_minute)
    return guard * guard_minute


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
