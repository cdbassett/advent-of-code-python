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
# %aimport aoc_utils, Utilities, iter_utils, seq_extensions, func_utils, aoc_2019_intcode
from aoc_utils import * # this includes adding c:\ut to sys.path
from utilities import *
from iter_utils import *
import seq_extensions # when running standalone, apparently need this import explicitly in main module
from aoc_2019_intcode import process_intcodes, parse_intcodes


# %% [markdown]
# # Parse

# %%
def parse_data(inp):
    return parse_intcodes(inp)


# %% [markdown]
# # Process

# %%
# running with 2-way generator is complicated bc of multiple varying length input and outputs, but seems to work for part1 once I changed to get the correct y value
# running with only collecting output locks up bc nic with no input just keeps polling and since we only get control on output we never get control again
# running with only input might work
def process(parsed, part1):
    def q_next(q):
        return q.popleft() if q else -1 # sending None to input makes it stop
    #ics(parsed)
    generators = []

    for n in range(50):
        generator = process_intcodes(parsed, n)
        generators.append(generator)
        generator.send(None) # start it
        generator.send(n) # send id

    value = 0
    queues = [deque() for _ in generators]
    nat_packet = None
    last_nat_y = None
    
    try:
        for step in count():
            ics(step)

            for id, g in enumerate(generators):
                q = queues[id]
                to_id = g.send(q_next(q))

                    # getting None indicates generator was requesting input rather than sending output
                    # continue sending anything waiting
                while to_id is None and q:
                    to_id = g.send(q_next(q))
                        
                if to_id is not None:
                    ics(id, to_id)
                    
                    while (new_x := g.send(q_next(q))) in (None, -1):
                        pass
                    while (new_y := g.send(q_next(q))) in (None, -1):
                        pass
                        
                    ics("    ", new_x, new_y)

                    if to_id == 255:
                        if part1:
                            return new_y
                            
                        nat_packet = new_x, new_y
                        ics(nat_packet)
                    else:
                        to_q = queues[to_id]
                        to_q.extend((new_x, new_y))
                        
            if not part1 and nat_packet and all(len(q)==0 for q in queues):
                to_q = queues[0]
                to_q.extend(nat_packet)

                if last_nat_y == nat_packet[1]:
                    return last_nat_y
                
                last_nat_y = nat_packet[1]
                nat_packet = None
                
    except StopIteration:
        ics("stopped", id, step)
    except GeneratorExit:
        ics("exited", id, step)
    return None


# %%
def part1(inp):
    parsed = parse_data(inp)
    result = process(parsed, True)
    print_result(result)


# %% [markdown]
# # Process2

# %%
def part2(inp):
    parsed = parse_data(inp)
    result = process(parsed, False)
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
real_inp = get_aocd_data()
insert_sample_functions(False, globals())
part1(real_inp)
part2(real_inp)


# %% [markdown]
# # Others' solutions

# %%
def solve1():
    import utils
    from intcode import IntCodeProgram
    import more_itertools
    
    load = utils.year_load(2019)
    data = load(23, "np")
    bus = [[x] for x in list(range(50))]
    programs = [IntCodeProgram(data, inputs=bus[i]) for i in range(50)]
    idx = 0
    
    while True:
        program = programs[idx]
        values = program.run()
        outputs = []
        
        for value in values:
            if value == 255:
                x = next(values)
                y = next(values)
                return y
                
            if program.state == 1:
                bus[idx].append(-1)
                break
                
            outputs += [value]
            
        for destination, x, y in more_itertools.chunked(outputs, 3):
            bus[destination] += [x, y]
            
        idx = (idx + 1) % 50 if not outputs else destination

solve1()
