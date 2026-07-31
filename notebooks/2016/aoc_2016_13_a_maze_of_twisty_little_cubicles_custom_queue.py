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

from icecream import ic

# %autoreload explicit
# import and reload these automatically
# %aimport aoc_utils, Utilities, iter_utils, seq_extensions
from utils.aoc_utils import * # this includes adding c:\ut to sys.path
from utils.utilities import *
from iter_utils import *
import utils.seq_extensions as seq_extensions # when running standalone, apparently need this import explicitly in main module


# %%
def parse(inp):
    return int(inp.strip())


# %%
def repr_state(state):
    return str(state)


# %% [markdown]
# # heuristic

# %%
# here we want to do a rough estimate of what the minimal cost it would be to transform from current state to final
def heuristic(current_state, final_state):
    return manhattan(current_state, final_state)


fav_num = None

# %%
def is_valid_location(x, y):
    val = x*x + 3*x + 2*x*y + y + y*y + fav_num
    return not (val.bit_count() & 1 )

# %%
#xs_and_ys = [(x, y) for x, y in product(range(10), range(7)) if not is_valid_location(x, y)]
#print(get_vis_map_multiline_str(*zip(*xs_and_ys)))


# %%
def gen_states(cur_state):
    x, y = cur_state

    if x > 0:
        yield x - 1, y

    if y > 0:
        yield x, y - 1

    yield x, y + 1
    yield x + 1, y


# %% [markdown]
# # Process

# %%
def process(parsed, x, y):
    global fav_num
    fav_num = parsed
    initial_state = (1,1)
    ic(repr_state(initial_state))
    queue = []
    final_state = (x, y)
    ic(repr_state(final_state))
    setup_repr(final_state)
    put, get = get_queue_functions_smallest(queue)
    put((heuristic(initial_state, final_state), initial_state))
    iterations = 0
    disp_at = 10_000
    cost_so_far = { initial_state: 0}
    came_from = { initial_state: None }

    while queue:
        estimated_cost, cur_state = get()
        current_cost = cost_so_far[cur_state]

        if cur_state == final_state:
            print(f"Found solution in {iterations} iterations")
            return current_cost, get_state_sequence(came_from, final_state)

        if not is_sample and not iterations % disp_at:
            ic(iterations, estimated_cost, current_cost, len(queue))

        ics(iterations, estimated_cost, current_cost, cur_state, len(queue))

        for next_state in gen_states(cur_state):
            if not is_valid_location(*next_state):
                continue

            new_cost = current_cost + 1

            if next_state not in cost_so_far or new_cost < cost_so_far[next_state]:
                cost_so_far[next_state] = new_cost
                next_cost = heuristic(next_state, final_state)
                est_cost = new_cost + next_cost
                #ics("    ", est_cost, next_cost, repr_state(next_state))
                put((est_cost, next_state))
                came_from[next_state] = cur_state

        iterations += 1

    print(f"No solution found in {iterations} iterations!")
    return None, None


# %%
def part1(inp, x, y):
    #extra comment
    parsed = parse(inp)
    steps, state_seq = process(parsed, x, y)
    result = steps
    print_result(result)
    return state_seq

# %% [markdown]
# # Process2

# %%
def process2(parsed, limit = 50):
    global fav_num
    fav_num = parsed
    initial_state = (1,1)
    ic(repr_state(initial_state))
    queue = []
    put, get = get_queue_functions_lifo(queue)
    put((0, initial_state))
    iterations = 0
    disp_at = 10_000
    cost_so_far = { initial_state: 0}

    while queue:
        step, cur_state = get()
        current_cost = cost_so_far[cur_state]

        if step >= limit:
            continue

        if not is_sample and not iterations % disp_at:
            ic(iterations, step, current_cost, len(queue))

        ics(iterations, step, current_cost, cur_state, len(queue))

        for next_state in gen_states(cur_state):
            if not is_valid_location(*next_state):
                continue

            new_cost = current_cost + 1

            if next_state not in cost_so_far or new_cost < cost_so_far[next_state]:
                cost_so_far[next_state] = new_cost
                #ics("    ", est_cost, next_cost, repr_state(next_state))
                put((step + 1, next_state))

        iterations += 1

    ic(len(cost_so_far))
    #return sum(1 for c in cost_so_far.values() if c <= limit)
    return cost_so_far


# %%
def part2(inp, limit=50):
    parsed = parse(inp)
    cost_so_far = process2(parsed, limit)
    result = len(cost_so_far)
    print_result(result)
    return cost_so_far


# %% [markdown]
# # Sample data

# %%
insert_sample_functions(False, globals())
#state_seq = part1("10", 7, 4)
cost_so_far = part2("10")
xs_and_ys = [(x, y) for x, y in product(range(10), range(7)) if (x, y) in cost_so_far]
print(get_vis_map_multiline_str(*zip(*xs_and_ys)))

# %% [markdown]
# # Actual data

# %% editable=true slideshow={"slide_type": ""}
real_inp = get_aocd_data()
insert_sample_functions(True, globals())
state_seq = part1(real_inp, 31, 39)
cost_so_far = part2(real_inp)
