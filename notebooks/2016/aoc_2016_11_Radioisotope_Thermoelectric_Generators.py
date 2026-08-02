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

# %% [markdown]
# [Advent of Code 2016 - Day 11](https://adventofcode.com/2016/day/11)

# %% editable=false jupyter={"source_hidden": true}
from utils.aoc_utils import *
if is_notebook():
    print(get_aoc_url())

# %%
# %load_ext autoreload

# %%
from collections import *

from icecream import ic
ic.configureOutput(outputFunction=print)
import pyperclip

# %autoreload explicit
# import and reload these automatically
# %aimport aoc_utils, Utilities, iter_utils, seq_extensions
from utils.aoc_utils import * # this includes adding c:\ut to sys.path
from utils.utilities import *
from utils.iter_utils import *
import utils.seq_extensions as seq_extensions # when running standalone, apparently need this import explicitly in main module


# %%
def parse_line(line):
    if "contains nothing relevant" in line:
        return []
    
    pieces = line.strip(".").replace("-compatible microchip", "M").replace(" generator", "G").replace(", and a", ", a").replace(" and a", ", a").split("contains a ")[1].split(", a ")
    return pieces


# %%
def parse(inp):
    return seq(inp.strip().split("\n")).take(3).map(parse_line).list()


# %%
def hashable_floors(state):
    ele_floor, floors = state
    return (ele_floor, tuple(frozenset(f) for f in floors))

def is_micro(item):
    return item.endswith("M")

def get_gen(item):
    return item[:-1] + "G"


# %%
def items_can_coexist(all_items):
    if all(is_micro(item) for item in all_items):
        return True

    result = all((get_gen(item) in all_items) for item in all_items if is_micro(item))
    #if not result:
        #ics( all_items)
    #ics(result, all_items)
    return result


# %%
def initl(s):
    return s[0].upper() + s[1] + s[-1]

def repr_state(state):
    def repr_floor(n, floor):
        e = "E " if n == ele_floor else ""
        return "F" + str(n+1) + ":" + e + ",".join(sorted(initl(s) for s in floor))
    ele_floor = state[0]
    return "|".join(repr_floor(n, f) for n, f in enumerate(state[1]))


# %%
repr_state((1, [{'lithiumM'}, set(), {'hydrogenM', 'hydrogenG', 'lithiumG'}, set()]))

# %%
all_items = {'hydrogenM', 'lithiumM', 'hydrogenG'}
items_can_coexist(all_items)

# %%
repr_state(hashable_floors((0,[{'lithiumM'}, {'hydrogenM', 'hydrogenG'}, {'lithiumG'}, set()])))
#hashable_floors((0,[{'lithiumM'}, {'hydrogenM', 'hydrogenG'}, {'lithiumG'}, set()]))

# %% [markdown]
# # heuristic

# %%
def cost_per_items(n):
    return n * 2 - 3 if n >= 3 else 1

# here we want to do a rough estimate of what the minimal cost it would be to transform from current state to final
# elevator must aways carry at east one, so can't move to carry empty
# should take into account moves back down
# maybe also current state of elevetor - and elevator will never be on an empty floor
def heuristic(current_state):
    ele_floor, floors = current_state
    floors = floors[:-1]
    #all_floor_count = sum(len(f) for f in floors) # how many items are on all floors
#    cost = math.ceil(sum((3 - n) * len(f) for n, f in enumerate(floors))/2)
    #cost = math.floor(sum((3 - n) * len(f) for n, f in enumerate(floors)))
    cost = seq(floors).map(len).accumulate().map(cost_per_items).sum()
    #ics(seq(floors).map(len))
    #ic(seq(floors).map(len).accumulate())
    #ic(seq(floors).map(len).accumulate().map(cost_per_items))
    #cost = sum(math.ceil(len(f)/2) for n, f in enumerate(accumulate(floors[:-1], lambda a, b: a + list(b), initial=[]))) # don't calculate anything for those already on top floor
    #cost = 0
    #acc_items = 0

    return cost


# %%
heuristic([0, ["ab","c","d", ""]])

# %%
#for state in recog:
#    ic(heuristic(state), repr_state(state))

# %% [markdown]
# # repr_state_anim

# %%
initials = None
initl_lookup = None

def setup_repr(state):
    global initials, initl_lookup
    initials = sorted(seq(state[1]).flatten().map(initl).set())
    #ic(initials)
    initl_lookup = dict((s, n) for n, s in enumerate(initials))
    #ic(initl_lookup)

def repr_state_anim(state):
    global initials, initl_lookup

    def repr_floor(n, floor):
        e = "E  " if n == ele_floor else ".  "
        floor_slots = [".  "] * len(initials)
        for s in floor:
            i = initl(s)
            floor_slots[initl_lookup[i]] = i
        return "F" + str(n+1) + " " + e + " ".join(floor_slots)
    ele_floor = state[0]
    return "\n".join(repr_floor(n, f) for n, f in reversed(list(enumerate(state[1]))))



# %% [markdown]
# # Process

# %%
def process(parsed):
    def attempt_move_items_to_floor(items, floors, from_floor_ndx, to_floor_ndx):
        from_floor = floors[from_floor_ndx]
        to_floor = floors[to_floor_ndx]
        all_items = set(items)
        all_items.update(to_floor) # add items to new floor
        old_items = set(from_floor)
        old_items.difference_update(items) # remove items from old floor

        if items_can_coexist(all_items) and items_can_coexist(old_items):
            new_floors = [set(floor) for floor in floors]
            new_floors[from_floor_ndx] = old_items
            new_floors[to_floor_ndx] = all_items
            #ics(items, new_floors[from_floor_ndx], new_floors[to_floor_ndx])
            yield hashable_floors((to_floor_ndx, new_floors))

    def gen_states(floors, from_floor_ndx, to_floor_ndx):
        #ics("gen_states", floors, from_floor_ndx, to_floor_ndx)
        from_floor = floors[from_floor_ndx]
        moveable = set(from_floor)

        for item in from_floor:
            yield from attempt_move_items_to_floor((item,), floors, from_floor_ndx, to_floor_ndx)

        for items in seq(from_floor).combinations(2):
            yield from attempt_move_items_to_floor(items, floors, from_floor_ndx, to_floor_ndx)


    #ics(initial_state)
    ic(parsed, len(parsed))
    initial_floors = [set(f) for f in parsed] + [set()] # initially empty 4th floor
    initial_state = hashable_floors((0,initial_floors))
    setup_repr(initial_state)
    #ic(repr_state(initial_state))
    print(f"initial_state:\n{repr_state_anim(initial_state)}")
    queue = []
    final_state = hashable_floors((3, (set(), set(), set(), seq(initial_floors).flatten().set())))
    #ic(repr_state(final_state))
    print(f"final_state:\n{repr_state_anim(final_state)}")
    #ics(final_state, repr_state(final_state))
    put, get = get_queue_functions_smallest(queue)
    put((0, initial_state))
    iterations = 0
    disp_at = 10_000
    cost_so_far = { initial_state: 0}
    came_from = { initial_state: None }

    while queue:
        #costs_in_queue = [estimated_cost for estimated_cost, cur_state in queue]
        #ics(costs_in_queue)
        if iterations == 1:
            for cost, state in queue:
                print(f"iteration {iterations}\n", repr_state_anim(state))

        estimated_cost, cur_state = get() # ignore priority
        current_cost = cost_so_far[cur_state]


        if cur_state == final_state:
            ic(iterations)

            state_seq = [ final_state ]
            prev_state  = final_state

            while prev_state := came_from.get(prev_state):
                state_seq.append(prev_state)

            state_seq = list(reversed(state_seq))
            #ics(state_seq)
            #for state in state_seq:
            #    ics(repr_state(state))
            return current_cost, state_seq

        if not iterations % disp_at:
            ic(iterations, estimated_cost, current_cost, len(queue))

        ele_floor, floors = cur_state

            # elevator can go up or down
            # must carry at least one item
            # cannot have a microchip with a generator of different type unless generator of same type is also present
        repr_floors = repr_state(cur_state)

        ics(iterations, estimated_cost, current_cost, repr_floors)
        possible_states = []

        if ele_floor > 0:
            possible_states.extend(gen_states(floors, ele_floor, ele_floor-1))

        if ele_floor < 3:
            possible_states.extend(gen_states(floors, ele_floor, ele_floor+1))

        for next_state in possible_states:
            new_cost = current_cost + 1

            if next_state not in cost_so_far or new_cost < cost_so_far[next_state]:
                cost_so_far[next_state] = new_cost
                next_cost = heuristic(next_state)
                est_cost = new_cost + next_cost
                #ics("    ", index, est_cost, next_cost, repr_state(next_state))
                put((est_cost, next_state))
                came_from[next_state] = cur_state

        iterations += 1

    ic(iterations)
    print("No solution found!")
    return None, None


# %%
def part1(inp):
    #extra comment
    parsed = parse(inp)
    steps, state_seq = process(parsed)
    result = steps
    #repr_steps = [repr_state(state) for state in steps]
    #ics(steps[0])
    #ics(repr_steps, result)
    print_result(result)
    return state_seq


# %%
def part2(inp):
    parsed = parse(inp)
    parsed[0].extend("eleriumG,eleriumM,dilithiumG,dilithiumM".split(","))
    steps, state_seq = process(parsed)
    result = steps
    print_result(result)
    return state_seq


# %% [markdown]
# # Sample data

# %%
insert_sample_functions(False, globals())
if 1:
    if "example" not in dir() or not example:
        example = get_aocd_example()

    sample_data1s = split_example(example)
    samp_inp1 = sample_data1s[0]
    is_sample = True
    #for line in samp_inp1.strip().split("\n"):
    #    part1(line)
    state_seq = part1(samp_inp1)
    state_seq = part2(samp_inp1)

# %% [markdown]
# Claim is that to move n objects up one floor, it costs 2 * n - 3
# https://www.reddit.com/r/adventofcode/comments/5hoia9/comment/db1v1hd/?utm_source=share&utm_medium=web2x&context=3

# %% [markdown]
# # Actual data

# %% editable=true slideshow={"slide_type": ""}
real_inp = get_aocd_data()
insert_sample_functions(True, globals())
state_seq = part1(real_inp)
state_seq = part2(real_inp)


# %% [markdown]
# # Animation frame render function

# %%
def plotstate(canvas, step):
    #print(f"plotstate(canvas, {step})")
    state = repr_state_anim(state_seq[step])
    lines =  state.split("\n") + ["Step " + str(step)]

    with hold_canvas():
        canvas.clear()  # Clear the old animation step

        for n, t in enumerate(lines):
            canvas.fill_text(t, 0, 25 + 40 * n)


# %% [markdown]
# # Animation display

# %%
if is_notebook():
    from ipycanvas import Canvas, hold_canvas
    import utils.aoc_vis as aoc_vis
    canvas = Canvas(width=1000, height=200)
    canvas.font = "32px monospace"
    canvas.fill_style = "green"
    ic(len(state_seq))
    aoc_vis.canvas_animation(canvas, len(state_seq), plotstate)
