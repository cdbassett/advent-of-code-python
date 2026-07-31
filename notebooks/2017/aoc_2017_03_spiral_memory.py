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
import math

from icecream import ic

# %autoreload explicit
# import and reload these automatically
# %aimport aoc_utils, Utilities, iter_utils, seq_extensions
from utils.aoc_utils import * # this includes adding c:\ut to sys.path
from utils.utilities import *
from utils.iter_utils import *
import utils.seq_extensions as seq_extensions # when running standalone, apparently need this import explicitly in main module


# %% [markdown]
# # Parse

# %%
def parse(inp):
    return int(inp.strip())


# %% [markdown]
# # Process

# %%
# lower right corner, last 0-based position in this ring before moving to next ring
def lr(n):
    return 4*n**2 + 4*n

# 0-based ring that 0-based index falls in
def ring(v):
    return math.ceil(math.sqrt(v+1)/2 - 1/2)


# %%
# manhattan distance from position indicated by 0-based index
# lr is last position in ring
def ring_manh(n):
    assert n >= 0 # some value may be off for innermost (0) ring
    if not n:
        return 0
    r = ring(n)
    prev_ring_last_pos = lr(r-1)
    cur_ring_last_pos = lr(r)
    ring_start_pos = prev_ring_last_pos + 1
    ring_length = cur_ring_last_pos - prev_ring_last_pos
    #ic(ring_length, r  * 8)
    assert ring_length == r * 8
    ring_side_length = ring_length // 4
    assert ring_length % 4 == 0
    rel_index = n - ring_start_pos
    quarter_index = rel_index % ring_side_length
    ring_x = r # only actually x and y for first quarter
    ring_y = abs(((quarter_index +1) - ring_side_length // 2))
    #ic(n, r, ring_x, ring_y, prev_ring_last_pos, ring_start_pos, cur_ring_last_pos, ring_length, ring_side_length, rel_index, quarter_index)
    ic(n, r, ring_x, ring_y, ring_length, ring_side_length, rel_index, quarter_index)
    return ring_x + ring_y


# %%
def process(parsed):
    ics(parsed)
    return ring_manh(parsed-1)


# %%
def part1(inp):
    parsed = parse(inp)
    result = process(parsed)
    print_result(result)


# %% [markdown]
# # Process2

# %%
def ring_positions():
    yield 0
    ring_side = 2
    pos = 0+0j
    dir = -1j

    while True:
        pos += 1+1j # move one to right for new ring

            # once for each side
        for s in range(4):
            for n in range(ring_side):
                pos += dir
                yield pos
            dir = -1j*dir # left turn
        ring_side += 2

def test():
    ring_side = 2
    pos = 0+0j
    dir = -1j

    while ring_side < 8:
        ics(ring_side, complex_to_tuple(pos))
        pos += 1+1j # move one to right for new ring
            # once for each side
        for s in range(4):
            for n in range(ring_side):
                pos += dir
                ics(n, complex_to_tuple(pos), complex_to_tuple(dir))

            dir = -1j*dir # left turn
            ics(complex_to_tuple(dir))
        ring_side += 2

def process2(parsed):
    ics(parsed)
    if 0:
        first_positions = seq(ring_positions()).take(25).list()
        ics(first_positions)

    #values = defaultdict(int, { complex(0, 0): 1}) # seed
    values = { 0: 1} # seed
    #ics(values)
    acc = 1

    for n, pos in seq(ring_positions()).drop(1).enumerate(1):
        #ics(seq(diag_neighbors_complex).map(partial(operator.add, pos)).lookup_default(values, 0).list())
        acc = seq(diag_neighbors_c).map(partial(operator.add, pos)).lookup_default(values, 0).sum()
        #sum(map(partial(operator.add, pos), diag_neighbors_complex))
        #ics(n, pos, acc)
        values[pos] = acc

        if acc > parsed:
            return acc

    return None


# %%
def part2(inp):
    parsed = parse(inp)
    result = process2(parsed)
    print_result(result)


# %% [markdown]
# # Sample data

# %%
insert_sample_functions(False, globals())

for n in [1, 12, 23, 1024]:
    part1(str(n))
#ics(diag_neighbors_complex)
if 0:
    part2(str(25))
    #test()
    #positions = seq(ring_positions()).take(27).map(complex_to_point).list()
    #positions = seq(ring_positions()).take(27).map(complex_to_tuple).list()
    #ics(positions)
else:
    part2(str(800))

# %% [markdown]
# # Actual data

# %% editable=true slideshow={"slide_type": ""}
real_inp = get_aocd_data()
insert_sample_functions(True, globals())
part1(real_inp)
part2(real_inp)

# %%
# 1 9 25 49 81
# d(n) = an2 + bn + c
# d(0) = 1, c = 1
# d(1) = 9, an^2 + bn +1 = 9
# d(2) = 25
import sympy as sp

a, b, c = unknowns = sp.symbols('a b c')
equations = []
if 1:
    equations.append(sp.Eq(a*0+b*0+c, 0))
    equations.append(sp.Eq(a*1+b*1+c, 8))
    equations.append(sp.Eq(a*4+b*2+c, 24))
else:
    equations.append(sp.Eq(a*0+b*0+c, 0))
    equations.append(sp.Eq(a*1+b*1+c, 9))
    equations.append(sp.Eq(a*4+b*2+c, 25))


ic(len(equations))
ic(equations)
solution = sp.solve(equations, unknowns)
print(solution)
# d(n) = 4n^2 + 4n + 1

# %%
# lower right corner, last 0-based position in this ring before moving to next ring
def lr(ring):
    return 4*ring**2 + 4*ring


# %%
for n in range(5):
    ic(n, lr(n))

# %%
n, y = sp.symbols('n y')
equations = []
equations.append(sp.Eq(4*n**2+4*n, y))
#equations.append(sp.Eq(n**2*7/2+n*11/2, y))
solution = sp.solve(equations, n)
print(solution)


# %%
# 0-based ring that 0-based index falls in
def ring(v):
    #return math.sqrt(56*v + 121)/14 - 11/1
    #return round(math.sqrt(v)/2)
    #return math.sqrt(v+1)/2 - 1/2
    return math.ceil(math.sqrt(v+1)/2 - 1/2)


# %%
for n in [1, 12, 23, 1024]:
#for n in [1, 2, 3, 4, 5,  8, 9, 10, 11, 14, 19, 20, 24, 25, 26, 55, 80, 81, 82, 100]:
    #ic(n, ring(n))
   ic(ring_manh(n-1))

# %%
