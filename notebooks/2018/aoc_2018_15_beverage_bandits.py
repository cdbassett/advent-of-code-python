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
from dataclasses import dataclass
import dataclasses

import numpy as np
from icecream import ic
from tabulate import tabulate

# %autoreload explicit
# import and reload these automatically
# %aimport aoc_utils, Utilities, iter_utils, seq_extensions, func_utils, pathfinding_redblob
from utils.aoc_utils import * # this includes adding c:\ut to sys.path
from utils.utilities import *
from utils.iter_utils import *
from utils.pathfinding_redblob import *
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

# %% [markdown]
# # Parse

# %%
def parse(inp):
    return build_numpy_array_from_string_graph(inp)


# %% [markdown]
# # Process

# %% [markdown]
# each round, collect units in read order (y then x)
# each unit's turn:
#   move if not already in range of an enemy:
#     for each enemy:
#       determine open in-range squares
#       determine closest (ties broken by read order)
#       move one step along shortest path (ties broken by read order)
#   attack if in range of an enemy
#       choose target: lowest hp, read order
#       deal damage: target hp -= attacker power
#       if target dies remove it

# %%
from utils.aoc_utils import *
import utils.pathfinding_redblob
from utils.pathfinding_redblob import *
from tabulate import tabulate

@dataclass
class Unit():
    id: int
    typ: str
    pos: np.ndarray
    attack: int = 3
    hp: int = 200

    def dist(self, unit):
        return manhattan(self.pos, unit.pos)

    def is_neighbor(self, unit):
        #return abs(self.pos[0]-unit.pos[0]) == 1 or abs(self.pos[1]-unit.pos[1]) == 1
        #ics(self.pos-unit.pos, abs(self.pos-unit.pos), sum(abs(self.pos-unit.pos)))
        return sum(abs(self.pos-unit.pos)) == 1

def process(parsed, elf_attack_power=3):
    def build_units(typ, start, elf_attack_power=3):
        positions = np.argwhere(data == typ)
        #ic(typ, positions)
        return [Unit(n, typ, pos, elf_attack_power) for n, pos in enumerate(positions, start)]

    def alive_units(units):
        return [unit for unit in units if unit.id not in died]

    def remove_unit(unit):
        data[*unit.pos] = "."

    def add_unit(unit):
        assert unit.typ != "."
        data[*unit.pos] = unit.typ

    def get_targets_in_range(unit, enemy_units):
        #ics("get_targets_in_range", unit, enemy_units)
        return [enemy_unit for enemy_unit in enemy_units if unit.is_neighbor(enemy_unit)]

    def to_xy(pos):
        return tuple(pos)
        #return pos[1], pos[0]

    def to_yx(pos):
        return np.array(pos)
        #return np.array([pos[1], pos[0]])

    def units_sorted_by_read_order(units):
        return sorted(units, key= lambda u: (u.pos[1], u.pos[0]))

    #ic(len(parsed))
    #ics(parsed)
    H = height(parsed)
    W = width(parsed)
    #ic(W, H)
    data = np.copy(parsed)
    ic(elf_attack_power)

    goblin_units = build_units("G", 0)
    elf_units = build_units("E", len(goblin_units), elf_attack_power)
    # all_units can be referred to by id as id matches its index
    all_units = goblin_units + elf_units
    #ics(all_units)

    if 0:
        indices = np.logical_or(data == "G", data == "E")
        positions = np.argwhere(indices)
        ic(positions)
    #data[np.where(indices)] = "." # "heal" the grid
    #ics(data)
    died = set()
    opposing_units = { "E": goblin_units, "G": elf_units }
    grid = SquareGridNeighborOrder(W, H)
    # we want read order, and numpy movements are y first
    #ics(movements_np)
    grid.NEIGHBOR_ORDER = sorted(movements, key = lambda t: (t[1], t[0]))
    grid.priority = lambda new_cost, current, next: (new_cost, next[1], next[0])

    #grid.NEIGHBOR_ORDER = [to_xy(pos) for pos in sorted(map(tuple, movements_np))]
    #ics(grid.NEIGHBOR_ORDER)
    #print_sample(get_numpy_char_array_repr(data))
    #print_sample(tabulate_table(maplist(dataclasses.asdict, all_units), headers="keys"))

    def callback(cbi):
        ics(cbi.iterations, cbi.current, cbi.neighbors, cbi.queue_len)

    for nround in count():
    #for nround in range(50):
        #ics(nround)
        any_moved, any_died = False, False
        remaining_units = units_sorted_by_read_order(alive_units(all_units))

        #if not remaining_units:
            #return nround * sum(unit.hp for unit in remaining_units)

        for attacking_unit in remaining_units:
            if attacking_unit.id not in died:
                #ics(attacking_unit)
                enemy_units = alive_units(opposing_units[attacking_unit.typ])

                if not enemy_units:
                    print_sample(get_numpy_char_array_repr(data))
                    print_sample(tabulate(maplist(dataclasses.asdict, all_units), headers="keys"))
                    return attacking_unit.typ, sum(1 for unit in elf_units if unit.hp <= 0), nround * sum(unit.hp for unit in alive_units(all_units))

                targets_in_range = get_targets_in_range(attacking_unit, enemy_units)
                #ics(attacking_unit, enemy_units, targets_in_range)

                # movement
                if not targets_in_range:
                    # open squares next to targets
                    #ics(data[*(enemy_units[0].pos + movements_np[0])])
                    start = to_xy(attacking_unit.pos)
                    start_char = [("0", start[0], start[1])]
                    goals = set([to_xy(p) for enemy_unit in enemy_units for d in movements_np if data[*(p := enemy_unit.pos + d)] == "."])
                    assert start not in goals
                    special_chars = [("?", x, y) for x, y in goals] + start_char
                    #print_sample(get_numpy_char_array_repr(data, special_chars = special_chars))
                    grid.walls = set(map(to_xy, np.argwhere(data != ".")))
                    came_from, cost_so_far, current = dijkstra_search(grid, start, goal = goals, is_goal = lambda current, goals: current in goals, callback=None) # priority must be in read order
                    #ics("    ", goals, start, current)

                    if current in goals:
                        path = reconstruct_path(came_from, start, current)
                        assert len(path) > 1, f"path {path} is too short"
                        new_pos = path[1] # first after start
                        #print_sample(get_numpy_char_array_repr(data, special_chars = [("@", current[0], current[1]), ("*", new_pos[0], new_pos[1])] + start_char))
                        remove_unit(attacking_unit)
                        attacking_unit.pos = to_yx(new_pos)
                        add_unit(attacking_unit)
                        #ics("moved:", attacking_unit)
                        any_moved = True
                        targets_in_range = get_targets_in_range(attacking_unit, enemy_units)

                # attack
                if targets_in_range:
                    #ics(sorted((target.hp, target.pos, target.id) for target in targets_in_range))
                    best_target = all_units[sorted((target.hp, tuple(target.pos), target.id) for target in targets_in_range)[0][2]]
                    #ics("    ", best_target, targets_in_range)
                    best_target.hp -= attacking_unit.attack

                    if best_target.hp < 0:
                        #ics("died:", best_target)
                        died.add(best_target.id)
                        remove_unit(best_target)
                        any_died = True

        if 0 and is_sample and (any_moved or any_died):
            print_sample(get_numpy_char_array_repr(data))
        #ics(alive_units(all_units))
        #print_sample(tabulate(maplist(dataclasses.asdict, units_sorted_by_read_order(alive_units(all_units))), headers="keys"))
        #break


# %%
def part1(inp):
    parsed = parse(inp)
    _, _, result = process(parsed)
    print_result(result)

# %% [markdown]
# # Process2


# %%
def process2(parsed):
    def one_battle(elf_attack_power):
        winner, dead_elves, outcome = process(parsed, elf_attack_power)
        ic(elf_attack_power, dead_elves, winner)
        return winner == "E" and dead_elves == 0

    if 1:
        elf_attack_power = find_lowest_int(one_battle, 4, 10)
        winner, dead_elves, outcome = process(parsed, elf_attack_power)
        ic(elf_attack_power, dead_elves, winner)

        if winner == "E" and dead_elves == 0:
            return outcome
    else:
        for elf_attack_power in range(4, 201): # no point in trying anything higher than hp, can only attack one at a time
        #for elf_attack_power in range(4, 20): # no point in trying anything higher than hp, can only attack one at a time
            winner, dead_elves, outcome = process(parsed, elf_attack_power)
            ic(elf_attack_power, dead_elves, winner)

            if winner == "E" and dead_elves == 0:
                return outcome


# %%
def part2(inp):
    parsed = parse(inp)
    result = process2(parsed)
    print_result(result)


# %% [markdown]
# # Sample data processing

# %%
insert_sample_functions(False, globals())

if 0:
    for sample_data1 in sample_data1s:
        part1(sample_data1)
else:
    part1(sample_data1s[0])

part2(sample_data2)

# %% [markdown]
# # Actual data

# %% editable=true slideshow={"slide_type": ""}
real_inp = get_aocd_data()
insert_sample_functions(True, globals())
part1(real_inp) # 197025
part2(real_inp) # 44423
