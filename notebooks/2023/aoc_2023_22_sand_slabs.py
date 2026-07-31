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
from dataclasses import dataclass,field

from icecream import ic

# %autoreload explicit
# import and reload these automatically
# %aimport aoc_utils, Utilities, iter_utils, seq_extensions
from utils.aoc_utils import * # this includes adding c:\ut to sys.path
from utils.utilities import *
from iter_utils import *
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
print(sample_data1)


# %% [markdown]
# # Parse

# %%
def parse_line(line):
    return seq(string_to_integers(line)).map(int).grouped(3).map(tuple).to_tuple()

def parse(inp):
    return seq(inp.strip().split("\n")).map(parse_line).list()


# %% [markdown]
# # Process

# %%
Brick = namedtuple("Brick","positions,axis,idx")

def z_above(p, p2):
    return p.x == p2.x and p.y == p2.y and p2.z > p.z

def down_shifted(p):
    return Point3D(p.x, p.y, p.z-1)

def down_shifted_positions(positions):
    return tuple(down_shifted(p) for p in positions)

def down_shifted_brick(brick):
    return Brick(down_shifted_positions(brick.positions), brick.axis, brick.idx)

def up_shifted(p):
    return Point3D(p.x, p.y, p.z-1)

def up_shifted_positions(positions):
    return tuple(up_shifted(p) for p in positions)

def bl(bi):
    return chr(bi + ord("A"))

@dataclass
class BrickPositions:
    occupied: dict = field(default_factory=dict)
    bricks_points_by_z_then_xy: dict = field(default_factory=lambda: defaultdict(dict))

    def add_brick_pos(self, p, idx):
        self.occupied[p] = idx
        self.bricks_points_by_z_then_xy[p.z][p[:2]] = idx

    def remove_brick_pos(self, p):
        del self.occupied[p]
        del self.bricks_points_by_z_then_xy[p.z][p[:2]]

    def calc_max_z(self):
        return max(p.z for p in self.occupied.keys())


# %%
def setup(parsed):
    brick_count = len(parsed)
    bricks = []
    brick_positions = BrickPositions()
    occupied = brick_positions.occupied
    bricks_points_by_z_then_xy = brick_positions.bricks_points_by_z_then_xy

    for brick_index, (start, end) in enumerate(parsed):
        #ic(start, end)
        axis = 2 if start == end else first_index(zip(start, end), key = lambda e: e[0] != e[1])
        assert start[axis] <= end[axis]
        brick = []

        for x in range(start[axis], end[axis]+1):
            p = list(start)
            p[axis] = x
            p = Point3D(*p)
            brick_positions.add_brick_pos(p, brick_index)
            brick.append(p)

        bricks.append(Brick(tuple(brick), axis, brick_index))

    ics(len(occupied))
    max_z = brick_positions.calc_max_z()
    ic(max_z)
        # don't shift any that area already at 1 (the lowest we can go)
    to_shift_brick_indexes = set(range(brick_count)) - set(bricks_points_by_z_then_xy[1].values())

        # move down
    for z in range(2, max_z+1):
        move_brick_indexes = set(bricks_points_by_z_then_xy[z].values()) & to_shift_brick_indexes
        #ics(z, move_brick_indexes)

        for brick_index in move_brick_indexes:
            brick = bricks[brick_index]
            other_positions = seq(occupied.items()).where(lambda e: e[1] != brick_index).dict()
            #ics(brick_index, len(brick.positions), len(other_positions))
            down_pos = brick.positions
            use_down_pos = None

            for test_z in range(z - 1):
                down_pos = down_shifted_positions(down_pos)
                #ics(bl(brick_index), down_pos, other_positions)

                if not any(p in other_positions for p in down_pos):
                    #ics("fit", brick_index)
                    use_down_pos = down_pos
                else:
                    #ics("no fit", brick_index)
                    break

            if use_down_pos:
                #ics("moving", bl(brick_index), brick.positions, use_down_pos)

                for p in brick.positions:
                    brick_positions.remove_brick_pos(p)

                bricks[brick_index] = brick._replace(positions = use_down_pos)

                for p in use_down_pos:
                    brick_positions.add_brick_pos(p, brick_index)

            to_shift_brick_indexes.remove(brick_index)

    support_bricks = defaultdict(list) # [brick_index][list of indexes] list of bricks this brick is holding up
    resting_bricks = defaultdict(list) # [brick_index][list of indexes] list of bricks this brick is resting on

    for brick in bricks:
        check_positions = up_shifted_positions(brick.positions)
        touching = set()

        for p in check_positions:
            existing = occupied.get(p)

            if existing is not None and existing != brick.idx:
                touching.add(existing)

        resting_bricks[brick.idx].extend(touching)

        for touch in touching:
            support_bricks[touch].append(brick.idx)

    #ics(support_bricks, resting_bricks)
    ic(len(support_bricks), len(resting_bricks))
    return bricks, brick_positions, support_bricks, resting_bricks


# %%
def process(parsed):
    #ics(parsed)
    bricks, brick_positions, support_bricks, resting_bricks = setup(parsed)
    brick_count = 0

    # check for disintegratable
    for brick in bricks:
        supporting_bricks = support_bricks[brick.idx]

            # bricks above us that aren't supported by anything else
        if not supporting_bricks or all(len(resting_bricks[bi]) > 1 for bi in supporting_bricks):
            ics("can disintegrate", brick.idx)
            brick_count += 1
        else:
            ics("can't disintegrate", brick.idx, brick.positions)

        #ics(brick)
    return brick_count


# %%
def part1(inp):
    parsed = parse(inp)
    result = process(parsed)
    print_result(result)


# %% [markdown]
# # Process2

# %% editable=true slideshow={"slide_type": ""}
# now we want the sum of all secondary bricks that would fall if one brick was disintegrated
def process2(parsed):
    def removal_count(brick_idx, removed = set(), level = 0):
        supporting_bricks = support_bricks[brick_idx]
            # all bricks this brick is holding up that no other brickes currently holding up (determined by removed)
        fall_bricks = [bi for bi in supporting_bricks if len(set(resting_bricks[bi]) - removed) == 0]
        next_removed = removed.union(fall_bricks).union([brick_idx])
        sub_fall_bricks = sets_union([removal_count(sbi, next_removed, level + 1) for sbi in fall_bricks])
        hdr = "   " * level
        ics(hdr, bl(brick_idx), supporting_bricks, fall_bricks, sub_fall_bricks, removed)
        return sub_fall_bricks.union(fall_bricks).union(removed)

    bricks, brick_positions, support_bricks, resting_bricks = setup(parsed)
    ics(resting_bricks, support_bricks)
    brick_count = 0

    # check for disintegratable
    for brick in bricks:
        ics("==============================")
        fallen = removal_count(brick.idx, set([brick.idx]))
        ics(brick.idx, len(fallen))
        more_work = True

        while more_work:
            more_work = False

                # check for unsupported bricks we may have missed
            for brick_idx, resting in resting_bricks.items():
                if resting and brick_idx not in fallen and fallen.issuperset(resting):
                    ics(brick_idx, more_work, resting, fallen)
                    fallen = removal_count(brick_idx, fallen.union([brick_idx]))
                    more_work = True

        ics(brick.idx, len(fallen))
        brick_count += len(fallen) - 1 # don't count base brick

    #for brick_idx in range(len(bricks)):
    return brick_count


# %%
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

