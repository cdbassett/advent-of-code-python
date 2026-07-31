from operator import itemgetter
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
from utils.pathfinding_redblob import *

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
    parts = line.split()
    return parts[1], parts[7]

def parse(inp):
    return seq(inp.strip().split("\n")).map(parse_line).list()


# %% [markdown]
# # Process

# %%
def process(parsed):
    def letter_priority(c):
        #return 100 - ord(c)
        return ord(c)
    ic(len(parsed))
    ics(parsed)

    dependencies = defaultdict(list)
    requirements = defaultdict(list)

    for a, b in parsed:
        dependencies[a].append(b)
        requirements[b].append(a)

    ics(dependencies, requirements)
    dependents = sets_union(list(dependencies.values()))
    ics(dependents)
    frontier = PriorityQueue()

    for a in dependencies.keys():
        if a not in dependents:
            frontier.put(a, letter_priority(a))

#    ics(frontier.elements)
    sequence = ""

    while not frontier.empty():
        ics(frontier.elements)
        c = frontier.get()
        sequence += c
        ics(c, sequence, dependencies[c])

        for next in list(dependencies[c]):
            ics(next, requirements[next])
            requirements[next].remove(c)

            if not requirements[next]:
                dependencies[c].remove(next)
                frontier.put(next, letter_priority(next))

    return sequence


# %%
def part1(inp):
    parsed = parse(inp)
    result = process(parsed)
    print_result(result)


# %% [markdown]
# # Process2

# %%
QueueJob = namedtuple("QueueJob","name,worker,finished")
"""
Still a priority queue, but include the time completed and worker doing the job,
so that when a job is pulled from the queue it is done and the current time is available
so priority is time, letter
"""
def process2(parsed, worker_count, add_time):
    workers = list(range(worker_count))
    available_workers = set(workers)
    ord_A = ord("A")

    def job_finished_time(time, job):
        return time + ord(job) - ord_A + add_time

    def letter_priority(time, job):
        return job_finished_time(time, job), job

    ic(len(parsed), add_time)
    #ics(parsed)
    dependencies = defaultdict(list)
    requirements = defaultdict(list)

    for a, b in parsed:
        dependencies[a].append(b)
        requirements[b].append(a)

    ics(dependencies, requirements)
    dependents = sets_union(list(dependencies.values()))
    ics(dependents)
    processing_jobs = PriorityQueue()
    waiting_jobs = PriorityQueue()

    for job in set(dependencies.keys()):
        if job not in dependents:
            waiting_jobs.put(job, job)

    ic(len(waiting_jobs.elements))
    sequence = ""
    time = 0

    # fill processing_jobs from waiting_jobs until no more workers or no more waiting jobs
    while not processing_jobs.empty() or not waiting_jobs.empty():
        ics("begin", waiting_jobs.elements)
        # fill processing_jobs from waiting_jobs
        while not waiting_jobs.empty() and available_workers:
            job = waiting_jobs.get()
            use_worker = first_element(available_workers)
            available_workers.remove(use_worker)
            ics("pull waiting", job, time, use_worker, available_workers)
            processing_jobs.put(QueueJob(job, use_worker, job_finished_time(time, job)), letter_priority(time, job))

        ics(processing_jobs.elements)
        # pull next processed job
        if not processing_jobs.empty():
            job, use_worker, time = processing_jobs.get()
            available_workers.add(use_worker)
            sequence += job
            ics("pull processing", job, use_worker, time, sequence, dependencies[job], len(available_workers))

            for next in list(dependencies[job]):
                ics("chk depends", next, requirements[next])
                requirements[next].remove(job)

                if not requirements[next]:
                    dependencies[job].remove(next)
                    ics("put waiting", next)
                    waiting_jobs.put(next, next)
        else:
            raise Exception("huh?")

    return time


# %%
def part2(inp, workers, add_time):
    parsed = parse(inp)
    result = process2(parsed, workers, add_time)
    print_result(result)


# %% [markdown]
# # Sample data processing

# %%
insert_sample_functions(False, globals())

for sample_data1 in sample_data1s:
    part1(sample_data1)

part2(sample_data2, 2, 1)

# %% [markdown]
# # Actual data

# %% editable=true slideshow={"slide_type": ""}
real_inp = get_aocd_data()
insert_sample_functions(True, globals())
part1(real_inp)
part2(real_inp, 5, 61)
