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
# %aimport aoc_utils, Utilities, iter_utils, seq_extensions, func_utils, aoc_2019_intcode
from utils.aoc_utils import * # this includes adding c:\ut to sys.path
from utils.utilities import *
from iter_utils import *
import utils.seq_extensions as seq_extensions # when running standalone, apparently need this import explicitly in main module
from aoc_2019_intcode import process_intcodes, parse_intcodes


# %% [markdown]
# # Parse

# %%
def parse_data(inp):
    return parse_intcodes(inp)


# %% [markdown]
# # Process

# %%
# running with 2-way generator is complicated bc of multiple varying length input and outputs
# running with only collecting output locks up bc nic with no input just keeps polling and since we only get control on output we never get control again
# running with only input might work
def process(parsed):
    #ics(parsed)
    generators = []
    queues = []

    def retrieve(id):
        q = queues[id]
#        ics("retrieve", id, q)
        return q.popleft() if q else -1
        
    def send(id, val):
        #ics("send", id, val)
        q = queues[id]
        q.append(val)

    for id in range(50):
        #generator = process_intcodes(parsed, n, input_func = partial(retrieve, id), output_func = partial(send, id))
        generator = process_intcodes(parsed, id, input_func = partial(retrieve, id)) # we will treat as iterator rather than providing an output function so that we have pause points
        #generator.send(None) # start it
        #generator.send(n) # set 
        generators.append(generator)
        q = deque()
        q.append(id) # provide id
        queues.append(q)

    try:
        for step in count():
            ic(step)

            for id, g in enumerate(generators):
                ic(id)
                to_id = next(g)
                ic(id, to_id)

                #if to_id is None:
#                    continue
                    
                new_x = next(g)
                ic(id, new_x)
                new_y = next(g)
                ic(id, new_y)
                    
                if to_id == 255:
                    return new_y
                    
                to_q = queues[to_id]
                to_q.extend((new_x, new_y))

        ic("stopped", combo, step)
    except GeneratorExit:
        ic("exited", combo, step)
    return None


# %%
def part1(inp):
    parsed = parse_data(inp)
    result = process(parsed)
    print_result(result)


# %% [markdown]
# # Process2

# %%
def process2(parsed):
    ics(parsed)
    return None


# %%
def part2(inp):
    return
    parsed = parse_data(inp)
    result = process2(parsed)
    print_result(result)


# %% [markdown]
# # Actual data

# %% editable=true slideshow={"slide_type": ""}
real_inp = get_aocd_data()
insert_sample_functions(True, globals())
part1(real_inp)
part2(real_inp)

# %% [markdown]
# # Sample data processing

# %%
insert_sample_functions(False, globals())
part1(real_inp)
part2(real_inp)

# %% [markdown]
# # Others' solutions
