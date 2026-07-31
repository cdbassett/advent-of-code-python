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
import math

from icecream import ic
import portion as P

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
print(sample_data1)


# %% [markdown]
# # Parse

# %%
def parse_rule(rule):
    if ">" in rule:
        gt = True
        rule = rule.replace(">",":")
    else:
        gt = False
        rule = rule.replace("<",":")

    attr, value, dest = rule.split(":")
    return Rule(attr, gt, int(value), dest)

def parse_workflow(line):
    name, rules = line[:-1].split("{")
    rule_parts = rules.split(",")
    return Workflow(name, seq(rule_parts[:-1]).map(parse_rule).list(), rule_parts[-1])

def parse_attr(line):
    name, val = line.split("=")
    #return PartAttr(name, int(val))
    return name, int(val)

def parse_part(line):
    return seq(line[1:-1].split(",")).map(parse_attr).dict()

def parse(inp):
    workflows, parts = seq(inp.strip().split("\n")).split()
    return seq(workflows).map(parse_workflow).list(), seq(parts).map(parse_part).list()

Workflow = namedtuple("Workflow","name,rules,final")
Rule = namedtuple("Rule","attr,gt,value,dest")
#PartAttr = namedtuple("PartAttr","name,value")

# %% [markdown]
# # Process

# %%
def check_gt(a, b):
    return a > b

def check_lt(a, b):
    return a > b

def process(parsed):
    def process_single_workflow(workflow):
        for rule in workflow.rules:
            value = part[rule.attr]
            result = value > rule.value if rule.gt else value < rule.value

            if result:
                return rule.dest

        return workflow.final

    def accepted(part):
        workflow = first_work_flow
        #ics(part)

        while 1:
            new_dest = process_single_workflow(workflow)
            #ics(workflow.name, new_dest)

            if new_dest == "A":
                return True
            elif new_dest == "R":
                return False

            workflow = workflows_by_name[new_dest]

    #ics(parsed)
    workflows, parts = parsed
    workflows_by_name = dict((w.name, w) for w in workflows)
    first_work_flow = workflows_by_name["in"]
    total_rating = 0

    for part in parts:
        if accepted(part):
            total_rating += sum(part.values())

    return total_rating


# %%
def part1(inp):
    parsed = parse(inp)
    result = process(parsed)
    print_result(result)


# %% [markdown]
# # Process2

# %%
def process2(parsed):
    workflows, parts = parsed
    workflows_by_name = dict((w.name, w) for w in workflows)
    first_work_flow = workflows_by_name["in"]

    queue = []
    put, get = get_queue_functions_lifo(queue)
    iterations = 0
    starting_intervals = dict((c, P.closed(1, 4000)) for c in "xmas")
    put((first_work_flow, 0, starting_intervals))
    final_intervals = []
    min_val = 1
    max_val = 4000

    while queue:
        iterations += 1
        workflow, rule_index, intervals = get()
        wn = workflow.name
        not_meet_cond_intervals = intervals.copy()

        for n, rule in enumerate(workflow.rules[rule_index:]):
            meet_cond_intervals = not_meet_cond_intervals.copy() # meet condition starts with not met intervals each time, if condition is met those intervals are put in queue
            meet_cond_interval = meet_cond_intervals[rule.attr] # meet condition refreshes each time, if condition is met processi put in queue
            not_meet_cond_interval = not_meet_cond_intervals[rule.attr] # not meet condition intervals is the same, it is the track where no conditions are met

            if rule.gt:
                meet_cond_intervals[rule.attr] = meet_cond_interval = meet_cond_interval & P.closed(rule.value+1, max_val)
                not_meet_cond_intervals[rule.attr] = not_meet_cond_interval = not_meet_cond_interval & P.closed(min_val, rule.value)
            else:
                meet_cond_intervals[rule.attr] = meet_cond_interval = meet_cond_interval & P.closed(min_val, rule.value-1)
                not_meet_cond_intervals[rule.attr] = not_meet_cond_interval = not_meet_cond_interval & P.closed(rule.value, max_val)

            ics(wn, n, rule, meet_cond_interval, not_meet_cond_interval)

                # this handles condition being met (not met is handled by rules continuing to be processed)
            if rule.dest == "A":
                ics(workflow.name, n, intervals)
                final_intervals.append(meet_cond_intervals)
            elif rule.dest == "R":
                pass
            else:
                put((workflows_by_name[rule.dest], 0, meet_cond_intervals))

            # this handles conditions not being met (final dest of workflow)
        if workflow.final == "A":
            ics(workflow.name, not_meet_cond_intervals)
            final_intervals.append(not_meet_cond_intervals)
        elif workflow.final == "R":
            pass
        else:
            put((workflows_by_name[workflow.final], 0, not_meet_cond_intervals))

    ics(final_intervals)
    ics(final_intervals[0]["a"])
    ind = seq(final_intervals).map(intervals_count).list()
    ics(ind)
    return sum(intervals_count(intervals) for intervals in final_intervals)

def interval_count(interval):
    return sum(p[2] - p[1] + 1 for p in P.to_data(interval))

def intervals_count(intervals):
    return math.prod(interval_count(interval) for interval in intervals.values())

def part2(inp):
    parsed = parse(inp)
    result = process2(parsed)
    print_result(result)


# %% [markdown]
# # Sample data

# %%
insert_sample_functions(False, globals())
part1(sample_data1)
part2(sample_data2)

# %% [markdown]
# # Actual data

# %% editable=true slideshow={"slide_type": ""}
real_inp = get_aocd_data()
insert_sample_functions(True, globals())
part1(real_inp)
part2(real_inp)

