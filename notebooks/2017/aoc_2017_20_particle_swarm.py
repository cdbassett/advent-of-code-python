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
from math import sqrt

import sympy as sp
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
sample_data2 = """
p=<-6,0,0>, v=< 3,0,0>, a=< 0,0,0>
p=<-4,0,0>, v=< 2,0,0>, a=< 0,0,0>
p=<-2,0,0>, v=< 1,0,0>, a=< 0,0,0>
p=< 3,0,0>, v=<-1,0,0>, a=< 0,0,0>
"""

# %%
for sample in sample_data1s:
    print(sample)
    print("=======================")


# %% [markdown]
# # Parse

# %%
def parse_line(line):
    return seq(string_to_integers_list(line)).grouped(3).list()

def parse(inp):
    return seq(inp.strip().split("\n")).map(parse_line).list()


# %% [markdown]
# # Process

# %%
def process(parsed):
    ics(parsed)
    #ic(seq(parsed).multimap(manhattan, manhattan, manhattan).map(reversed).map(list).zip_with_index().sorted()[:10])
    #ic(seq(parsed).map(itemgetter(2)).map(manhattan).zip(seq(parsed).map(itemgetter(0)).map(manhattan)).zip_with_index().sorted()[:10])
    return seq(parsed).map(itemgetter(2)).map(manhattan).zip_with_index().min()[1]


# %%
def part1(inp):
    parsed = parse(inp)
    result = process(parsed)
    print_result(result)


# %%
# wanted: exrpessions that gives t based on 2 particles' info
if 0:
    unknowns = sp.symbols('x1 x2 v1 v2 a1 a2 t')
    x1, x2, v1, v2, a1, a2, t = unknowns
    equations = []
    if 1:
        equations.append(sp.Eq(position(x1, v1, a1, t), position(x2, v2, a1, t)))
    else:
        equations.append(sp.Eq(position(x1, v1, a1, t), position(x2, v2, a2, t)))
    solution = sp.solve(equations, t)
    ic(solution)
    ic(len(solution))
    ic(len(solution[0]))
    ic(len(solution[1]))
    ic(solution[0][0])
    ic(solution[1][0])

# %%
"""
x=x0+v0*t+a*t**2/2 (constant a)

"""
def position(x0, v0, a, t):
    #res =  x0+v0*t+a*t**2/2
    res =  x0 + (v0+a/2)*t + a*t**2/2
    #assert int(res) == res
    #if int(res) != res:
    #    ic(res, x0, v0, a, t)
    return res

def collision_times(x1, x2, v1, v2, a1, a2):
    if a1 == a2:
        if v1 == v2:
            return tuple()

        initial = ((-x1 + x2)/(v1 - v2),)
        #nitial = -(a1 - a2 + 2*v1 - 2*v2)/(a1 - a2)
        #return tuple(int(r) for r in [(-x1 + x2)/(v1 - v2)] if int(r) == r)
    else:
            # -(v1 - v2)/(a1 - a2) +- sqrt(-2*a1*x1 + 2*a1*x2 + 2*a2*x1 - 2*a2*x2 + v1**2 - 2*v1*v2 + v2**2)/(a1 - a2)
            # (-(a1 - a2 + 2*v1 - 2*v2)/(2*(a1 - a2)) +- sqrt(a1**2 - 2*a1*a2 + 4*a1*v1 - 4*a1*v2 - 8*a1*x1 + 8*a1*x2 + a2**2 - 4*a2*v1 + 4*a2*v2 + 8*a2*x1 - 8*a2*x2 + 4*v1**2 - 8*v1*v2 + 4*v2**2)/(2*(a1 - a2)),),
        try:
            #partial = -2*a1*x1 + 2*a1*x2 + 2*a2*x1 - 2*a2*x2 + v1**2 - 2*v1*v2 + v2**2
            partial = a1**2 - 2*a1*a2 + 4*a1*v1 - 4*a1*v2 - 8*a1*x1 + 8*a1*x2 + a2**2 - 4*a2*v1 + 4*a2*v2 + 8*a2*x1 - 8*a2*x2 + 4*v1**2 - 8*v1*v2 + 4*v2**2

            if partial < 0:
                return tuple()

            #divisor = a1 - a2
            #a, b = (-(v1 - v2)/divisor), sqrt(partial)/divisor
            divisor = 2*(a1 - a2)
            a, b = -(a1 - a2 + 2*v1 - 2*v2)/divisor, sqrt(partial)/divisor
            initial = (a - b, a + b)
            #res = tuple(int(r) for r in (a - b, a + b) if r >= 0 and int(r) == r)
            #return res if len(res) < 2 or res[0] != res[1] else res[:1]
        except ValueError:
            ic(x1, x2, v1, v2, a1, a2)

    res = tuple(int(r) for r in initial if r >= 0 and r.is_integer())
    return res if len(res) < 2 or res[0] != res[1] else res[:1]


# %% [markdown]
# # Process2

# %%
def process2(parsed):
    #ics(parsed)
    ic(len(parsed))

    if 0:
        for p, v, a in parsed[:3]:
            ic(p,v,a, "========")

            for n in range(3):
                ic(n, "    --------")
                for t in range(3):
                    ic(t, "    ", position(p[n], v[n], a[n], t))
        return

    particles = dict(enumerate(parsed)) # index of particle -> particle
    collisions = defaultdict(list) # time -> list of particles that collide
    match_count = 0
    partial_match_count = 0

        # try to calculate collisions based on formula obtained from sympy for one dimension
    if 1:
        #for (n1, (p1, v1, a1)), (n2, (p2, v2, a2)) in combinations(take(5, particles.items()), 2):
        for (n1, (p1, v1, a1)), (n2, (p2, v2, a2)) in combinations(particles.items(), 2):
            #ics("-----------")

            first_match = first_element((n, ct) for n in range(3) if (ct := collision_times(p1[n], p2[n], v1[n], v2[n], a1[n], a2[n])))

            if first_match:
                n_match, times = first_match

                for t in times:
                    if all(math.isclose(position(p1[n], v1[n], a1[n], t), position(p2[n], v2[n], a2[n], t)) for n in range(3) if n != n_match):
                        desc = f"matched at {t}"
                        collisions[t].append((n1, n2))
                        match_count += 1
                    else:
                        desc = f"matched at {t} with n=={n_match} but not the rest"
                        partial_match_count += 1

                    if 0:
                        if partial_match_count < 100:
                            ic(n1, (p1, v1, a1), n2, (p2, v2, a2), desc)
                            for n in range(3):
                                col_time, pos1, pos2 = collision_times(p1[n], p2[n], v1[n], v2[n], a1[n], a2[n]), position(p1[n], v1[n], a1[n], t), position(p2[n], v2[n], a2[n], t)
                                ic("    ", n, col_time, pos1, pos2)
                        else:
                            ics(n1, n2, desc)
            #else:
            #    ics(n1, n2, "no match at all")
            #for n in range(3):
            #    ics(n1, n2, n, collision_times(p1[n], p2[n], v1[n], v2[n], a1[n], a2[n]))
    else:
        unknowns = sp.symbols('x y z t')
        x, y, z, t = unknowns

        for (n1, (p1, v1, a1)), (n2, (p2, v2, a2)) in combinations(particles.items(), 2):
            equations = []

            for n in range(3):
                equations.append(sp.Eq(position(p1[n], v1[n], a1[n], t), position(p2[n], v2[n], a2[n], t)))

            solution = sp.solve(equations, t)
            #ic(len(solution))
            #ics(solution)

            if solution:
                collisions[solution[t]].append((n1, n2))

    ic(match_count, partial_match_count)
    ics(collisions)
    ic(len(collisions))
        #equations.append(sp.Eq(y + t*dy, h_init.y + t*h_velo.y))
        #equations.append(sp.Eq(z + t*dz, h_init.z + t*h_velo.z))

    for time, col_particles in sorted(collisions.items()):
        destroyed = set()

        for npart1, npart2 in col_particles:
            if npart1 in particles and npart2 in particles:
                destroyed.update([npart1, npart2])

        for npart in destroyed:
            del particles[npart]
            #particles.pop(npart, None)
        #particles -= col_particles

    ic(len(particles))
    return len(particles)


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
