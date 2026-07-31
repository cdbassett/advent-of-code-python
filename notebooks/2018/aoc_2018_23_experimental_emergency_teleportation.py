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
import sys
from collections import *
import re

import numpy as np
from scipy import spatial
from icecream import ic
import z3
from z3 import Int, Optimize, If, Real, Solver, Or, And

# %autoreload explicit
# import and reload these automatically
# %aimport aoc_utils, Utilities, iter_utils, seq_extensions, func_utils
from aoc_utils import * # this includes adding c:\ut to sys.path
from Utilities import *
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
sample_data2 = \
"""pos=<10,12,12>, r=2
pos=<12,14,12>, r=2
pos=<16,12,12>, r=4
pos=<14,14,14>, r=6
pos=<50,50,50>, r=200
pos=<10,10,10>, r=5"""

# %% [markdown]
# # Parse

# %%
Robot = namedtuple("Robot","pos,radius")

def parse_line(line):
    return Robot(tuple(line[:3]), line[-1])

def parse_data(inp):
    return seq(inp.strip().split("\n")).map(string_to_integers_list).map(parse_line).list()


# %%
# oops... this finds the nanobot in range of the most, not the coordinate
def process2old(parsed):
    #ics(parsed)
    points = np.array(seq(parsed).map(lambda r: r.pos).list())
    radii = np.array(seq(parsed).map(lambda r: r.radius).list())
    #ics(radii)
    tree = spatial.KDTree(points)
    res = tree.query_ball_point(points, radii, p=1) # p=1 means manhattan
    ics(res)
    res_with_extra = [[-len(el), manhattan(parsed[n].pos)] + el for n, el in enumerate(res)]
    #results = sorted(res, key=len, reversed=True)
    results = sorted(res_with_extra)
    max_length = results[0][0]
    ics(results, max_length)
    return None


# %%
def to_cuboid(robot):
    p = robot.pos
    r = robot.radius
    return tuple((t-r, t+r) for t in p)

# big mistake: area in range of nanorobots is not a cuboids, it's a rough sphere
# with manhattan distance instead of euclidean
def process2old2(parsed):
    ics(parsed)
    points = np.array(seq(parsed).map(lambda r: r.pos).list())
    radii = np.array(seq(parsed).map(lambda r: r.radius).list())
    cuboids = seq(parsed).map(to_cuboid).list()
    ics(cuboids)
    intersections = [[cuboids[0], set([cuboids[0]])]]

    for cuboid in cuboids[1:]:
        found = False

        for one in intersections:
            #ics(cuboid, one)
            intersection = cubes_intersection(cuboid, one[0])

            if intersection:
                one[1].add(cuboid)
                one[0] = intersection
                found = True
                #break

        if not found:
            intersections.append([cuboid, set([cuboid])])

    # one more pass for ealier cuboids that may have missed intersecting with later intersections
    for cuboid in cuboids[1:]:
        for one in intersections:
            #ics(cuboid, one)
            intersection = cubes_intersection(cuboid, one[0])

            if intersection:
                one[1].add(cuboid)
                one[0] = intersection


    if 0:
        for one in intersections:
            if any(cubes_intersection(one[0], other[0]) for other in intersections if one != other):
            #if any(cubes_intersection(one[0], other[0]) for other in intersections):
                print("found additional intersections")

    ics(intersections)
    ic(len(intersections))
    ic(maplist(itemgetter(0), intersections))
    ic(seq(intersections).map(itemgetter(1)).map(len))
    primary_cuboid = seq(intersections).max_by(lambda e: len(e[1]))[0]
    ic(primary_cuboid)
    ic(seq(intersections).map(itemgetter(0)).level2_map(itemgetter(0)).map(list))
    ic(seq(intersections).map(itemgetter(0)).level2_map(itemgetter(0)).map(list).map(manhattan))
    # assuming positive
    p = maplist(itemgetter(0), primary_cuboid)
    ic(p)
    return sum(p)


# %% [markdown]
# # Process

# %%
def process(parsed):
    ic(len(parsed))
    #ics(parsed)
    strongest = seq(parsed).max_by(lambda r: r.radius)
    return seq(parsed).count(lambda r: manhattan(r.pos, strongest.pos) <= strongest.radius)


# %%
def part1(inp):
    parsed = parse_data(inp)
    result = process(parsed)
    #ics(parsed[0])
    #ics(list(product(parsed[0].pos)))
    print_result(result)


# %% [markdown]
# # Process2

# %%
x = Real('x')
y = Real('y')
s = Solver()
s.add(x > 1, y > 1, Or(x + y > 3, x - y < 2))
print ("asserted constraints...")
for c in s.assertions():
    print (c)

print (s.check())
print ("statistics for the last check method...")
print (s.statistics())
# Traversing statistics
for k, v in s.statistics():
    print ("%s : %s" % (k, v))


# %%
def process2(parsed):
    def z3_abs(x):
        return If(x >= 0,x,-x)

    def z3_dist(a, b):
        return z3_abs(a[0] - b[0]) + z3_abs(a[1] - b[1]) + z3_abs(a[2] - b[2])

    x, y, z = (Int(c) for c in "xyz")
    opt = Optimize()
    origin = 0,0,0
    position = x, y, z
    bot_vars = [Int("b"+str(n)) for n, bot in enumerate(parsed)]
    bot_constraints = [ ]
    in_range_cnt = Int("in_range_cnt")

    for bot, bot_var in zip(parsed, bot_vars):
        opt.add(bot_var == If(z3_dist(bot.pos, position) <= bot.radius, 1, 0))

    dist_from_origin = Int("dist")
    opt.add(dist_from_origin == z3_dist(origin, position))
    opt.add(in_range_cnt == sum(bot_vars))
    opt.maximize(in_range_cnt)
    d = opt.minimize(dist_from_origin)

    ics(opt.check())
    ics(opt.lower(d))
    model = opt.model()
    #ics(model)
    ics(model[dist_from_origin])
    ics(model[in_range_cnt])
    return model[dist_from_origin].as_long()


# %%
def part2(inp):
    parsed = parse_data(inp)
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
part2(real_inp) # 99832660 is too low 112997634

# %% [markdown]
# # Other's Solutions
# typical times are ~ 0.5 sec for heapq solution, 1.5m for z3 solution
# but z3 solutions are easy to understand

# %% [markdown]
# # heapq

# %%
# https://www.reddit.com/r/adventofcode/comments/a8s17l/comment/ecfmpy0/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button
import heapq

data = real_inp.split("\n")

def d3(a, b):
    return abs(a[0]-b[0])+abs(a[1]-b[1])+abs(a[2]-b[2])

bots = [tuple(map(int, list(re.findall(r'-?\d+', ln)))) for ln in data]

maxradbot = max(bots, key=itemgetter(3))
maxrad = maxradbot[-1]

print("bots in range of maxrad bot", sum(1 for b in bots if d3(b, maxradbot) <= maxrad))

def shift_bit_length(x):
    return 1<<(x-1).bit_length()

# Find a box big enough to contain everything in range that is a power of 2
maxabscord = max(max(abs(b[i])+b[3] for b in bots) for i in (0, 1, 2))
boxsize = shift_bit_length(maxabscord)
ic(boxsize, maxabscord)

initial_box = ((-boxsize, -boxsize, -boxsize), (boxsize, boxsize, boxsize))

def does_intersect(box, bot):
    # returns whether box intersects bot
    d = 0

        # https://www.desmos.com/calculator/eubniebcio
    for i in (0, 1, 2):
        boxlow, boxhigh = box[0][i], box[1][i] - 1
        d += abs(bot[i] - boxlow) + abs(bot[i] - boxhigh)
        d -= boxhigh - boxlow

    d //= 2
    return d <= bot[3]

def intersect_count(box):
    return sum(1 for b in bots if does_intersect(box, b))


# Set up heap to work on things first by number of bots in range of box,
# then by size of box, then by distance to origin
#
# The idea is that we first work on a box with the most bots in range.
# In the event of a tie, work on the larger box.
# In the event of a tie, work on the one with a min corner closest to the origin.
#
# These rules mean that if I get to where I'm processing a 1x1x1 box,
# I know I'm done:
# - no larger box can intersect as many bots' ranges as what I'm working on
# - no other 1x1x1 box intersecting the same number of bots can be as close

# remember heapq.heappop pulls the smallest off the heap, so negate the two things I want to pull by largest (reach of box, boxsize)
# and do not negate distance-to-origin, since I want to work on smallest distance-to-origin first

workheap = [(-len(bots), -2*boxsize, 3*boxsize, initial_box)]

while workheap:
    (negreach, negsz, dist_to_orig, box) = heapq.heappop(workheap)

    if negsz == -1:
        print("Found closest at %s dist %s (%s bots in range)" %
              (str(box[0]), dist_to_orig, -negreach))
        break

    newsz = negsz // -2

    for octant in [(0, 0, 0), (0, 0, 1), (0, 1, 0), (0, 1, 1),
                   (1, 0, 0), (1, 0, 1), (1, 1, 0), (1, 1, 1)]:
        newbox0 = tuple(box[0][i] + newsz * octant[i] for i in (0, 1, 2))
        newbox1 = tuple(newbox0[i] + newsz for i in (0, 1, 2))
        newbox = (newbox0, newbox1)
        newreach = intersect_count(newbox)
        heapq.heappush(workheap,
                       (-newreach, -newsz, d3(newbox0, (0, 0, 0)), newbox))

# %%
# https://www.reddit.com/r/adventofcode/comments/a8s17l/comment/echkr47/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button
# https://gist.github.com/ephemient/f13c80c6a1ccaa0bb6a81554daa5b788#file-day23-py
"""
This is a O(2n) search using rotated coordinates and simple min/max to narrow down the intersecting region, but optimized for greed.
Particularly:
If we've reached a state where there aren't enough bots left to beat the current best overlap count, immediately bail out.
I also wanted a partial ordering where "smaller region A" is seen before "larger region B which fully encloses A", so when I encounter A I can just immediately take all B's, reducing the amount of backtracking over equivalent states. Originally I sorted on approximated region size, but now I'm sorting on coordinates (Data.Map is sorted in Haskell) and I feel more confident that it's correct.
There's also some trickiness required to handle inputs where intersection loses a dimension, making some of the octahedron's face bounds meaningless.
"""

def heapq_solution2():
    from collections import OrderedDict, defaultdict, namedtuple
    from functools import total_ordering
    from heapq import heappop, heappush
    from itertools import chain

    Bot = namedtuple('Bot', 'x y z r')
    pattern = re.compile(r'pos=<(-?\d+),(-?\d+),(-?\d+)>, r=(\d+)')
    bots = [Bot(*map(int, pattern.match(line).groups())) for line in real_inp.split("\n")]
    maxradbot = max(bots, key=itemgetter(3))
    max_r = maxradbot.r
    print((sum(manhattan(b[:3], maxradbot[:3]) <= max_r for b in bots)))

    @total_ordering
    class Octa_ordering(object):
        def __lt__(self, other):
            return self.min < other.min or self.min == other.min and other.max < self.max

    class Octa(Octa_ordering, namedtuple('Octa', ('min', 'max'))):
        def __new__(cls, *args, **kwargs):
            if 'bot' in kwargs:
                x, y, z, r = kwargs['bot']
                t, u, v, w = x + y + z, x + y - z, x - y - z, x - y + z
                return super(Octa, cls).__new__(cls, (t - r, u - r, v - r, w - r),
                                                (t + r, u + r, v + r, w + r))
            return super(Octa, cls).__new__(cls, *args, **kwargs)

        def intersect(self, other):
            c, d, e, f = self.min
            g, h, i, j = other.min
            k, l, m, n = self.max
            o, p, q, r = other.max
            s, t, u, v = max(c, g), max(d, h), max(e, i), max(f, j)
            w, x, y, z = min(k, o), min(l, p), min(m, q), min(n, r)
            return None if s > w or t > x or u > y or v > z else Octa((s, t, u, v), (w, x, y, z))

        def distance_to_origin(self):
            o, p, q, r = self.min
            s, t, u, v = self.max
            if o < s and p < t and q < u and r < v:
                w = min(abs(o), abs(s)) if o * s >= 0 else 0
                x = min(abs(p), abs(t)) if p * t >= 0 else 0
                y = min(abs(q), abs(u)) if q * u >= 0 else 0
                z = min(abs(r), abs(v)) if r * v >= 0 else 0
                return max(w, x, y, z)
            return min(
                abs((x + z) // 2) + abs((y - z) // 2) + abs((x - y) // 2)
                for x in range(o, s + 1) for y in range(p + ((p ^ x) & 1), t + 1, 2)
                for z in range(q + ((q ^ x) & 1), u + 1, 2) if r <= x - y + z <= v)

    best_count = 0
    octs = defaultdict(set)

    for i, bot in enumerate(bots):
        octs[Octa(bot=bot)].add(i)

    queue = [(0, (), OrderedDict((k, octs[k]) for k in sorted(octs)))]

    while queue:
        n, _, rest = heappop(queue)

        if -n < best_count:
            break

        octa, n = rest.popitem()
        sub = defaultdict(set)

        for octa2, m in rest.items():
            octa3 = octa.intersect(octa2)

            if octa3 is not None:
                (n if octa == octa3 else sub[octa3]).update(m)

        if len(n) > best_count:
            best_count, best_distance = len(n), [octa]
        elif len(n) == best_count:
            best_distance.append(octa)

        m = frozenset(chain.from_iterable(rest.values()))
        heappush(queue, (-len(m), m, rest))
        rest = OrderedDict((k, sub[k].union(n)) for k in sorted(sub))
        m = frozenset(chain.from_iterable(rest.values()))
        heappush(queue, (-len(m), m, rest))

    print(min(octa.distance_to_origin() for octa in best_distance))

heapq_solution2()

# %% [markdown]
# # Z3 (slow)

# %%
# https://www.reddit.com/r/adventofcode/comments/a8s17l/comment/ecdcbin/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button
# https://github.com/msullivan/advent-of-code/blob/master/2018/23b.py
from z3 import Int, If, Optimize

sys.setrecursionlimit(3000)

def z3_solve():
    def extract(s):
        return [int(x) for x in re.findall(r'-?\d+', s)]

    def dist(x, y):
        return abs(x[0] - y[0]) + abs(x[1] - y[1]) + abs(x[2] - y[2])

    def z3_abs(x):
        return If(x >= 0,x,-x)

    def z3_dist(x, y):
        return z3_abs(x[0] - y[0]) + z3_abs(x[1] - y[1]) + z3_abs(x[2] - y[2])

    data = [extract(s.strip()) for s in real_inp.split("\n")]
    data = [(x[3], tuple(x[:-1])) for x in data]
    m = max(data)
    in_range = [x for x in data if dist(x[1], m[1]) <= m[0]]
    print(len(in_range))

    x = Int('x')
    y = Int('y')
    z = Int('z')
    orig = (x, y, z)
    cost = Int('cost')
    cost_expr = x * 0

    for r, pos in data:
        cost_expr += If(z3_dist(orig, pos) <= r, 1, 0)

    opt = Optimize()
    print("let's go")
    opt.add(cost == cost_expr)
    opt.maximize(cost)
    # I didn't do this step in my initial #2 ranking solution but I suppose you should.
    # z3 does them lexicographically by default.
    opt.minimize(z3_dist((0,0,0), (x, y, z)))
    opt.check()
    model = opt.model()
#    print(model)
    pos = (model[x].as_long(), model[y].as_long(), model[z].as_long())
    print("position:", pos)
    print("num in range:", model[cost].as_long())
    print("distance:", dist((0,0,0), pos))

z3_solve()


# %%
# https://www.reddit.com/r/adventofcode/comments/a8s17l/comment/ecdg47x/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button
def z3_solution_3():
    import z3
    def extract(s):
        return [int(x) for x in re.findall(r'-?\d+', s)]

    bots = [extract(s.strip()) for s in real_inp.split("\n")]
    bots = [(x[3],) + tuple(x[:-1]) for x in bots]
    best = max(bots)
    br, bx, by, bz = best
    tot = 0

    for b in bots:
    	r, x, y, z = b

    	if abs(x-bx)+abs(y-by)+abs(z-bz) <= br:
    		tot += 1

    print(tot)

    def dist1d(a, b):
    	d = a - b
    	return z3.If(d >= 0, d, -d)

    def manhattan(ax, ay, az, bx, by, bz):
    	return dist1d(ax, bx) + dist1d(ay, by) + dist1d(az, bz)

    solver = z3.Optimize()

    bestx = z3.Int('bestx')
    besty = z3.Int('besty')
    bestz = z3.Int('bestz')
    distance = z3.Int('distance')

    inside = []

    for i, b in enumerate(bots):
    	br, *bxyz = b
    	bot = z3.Int('b{:4d}'.format(i))
    	ok = z3.If(manhattan(bestx, besty, bestz, *bxyz) <= br, 1, 0)
    	solver.add(bot == ok)
    	inside.append(bot)

    solver.add(distance == manhattan(bestx, besty, bestz, 0, 0, 0))

    solver.maximize(z3.Sum(*inside))
    solver.minimize(distance)
    solver.check()

    m = solver.model()
    min_distance = m.eval(distance)
    print(min_distance)

z3_solution_3()

# %%
# https://www.reddit.com/r/adventofcode/comments/a8s17l/comment/ecdbux2/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button
import re

def gan(s):
  return maplist(int, re.findall(r'-?\d+', s))

def lenr(l):
  return range(len(l))

d = real_inp.split('\n')
nanobots = maplist(gan, d)
#nanobots = [((n[0], n[1], n[2]), n[3]) for n in map(gan, d)]
nanobots = [(tuple(p), r) for *p, r in map(gan, d)]
#ic(nanobots)

if 0:
    def dist(a, b):
      (x0, y0, z0), (x1, y1, z1) = a, b
      return abs(x0-x1) + abs(y0-y1) + abs(z0-z1)
    dist = manhattan

# z3-solver
import z3

def zabs(x):
  return z3.If(x >= 0,x,-x)

x, y, z = (z3.Int(c) for c in "xyz")
in_ranges = [ z3.Int('in_range_' + str(i)) for i in lenr(nanobots) ]
range_count = z3.Int('sum')
o = z3.Optimize()

for i in lenr(nanobots):
  (nx, ny, nz), nrng = nanobots[i]
  o.add(in_ranges[i] == z3.If(zabs(x - nx) + zabs(y - ny) + zabs(z - nz) <= nrng, 1, 0))

o.add(range_count == sum(in_ranges))
dist_from_zero = z3.Int('dist')
o.add(dist_from_zero == zabs(x) + zabs(y) + zabs(z))
h1 = o.maximize(range_count)
h2 = o.minimize(dist_from_zero)
print(o.check())
print("b", o.lower(h2), o.upper(h2))
#print o.model()[x]
#print o.model()[y]
#print o.model()[z]

# %% [markdown]
# # PriorityQueue manhattan (incorrect)

# %%
# https://www.reddit.com/r/adventofcode/comments/a8s17l/comment/ecdqzdg/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button
# # off by one for my input
import sys,re
from queue import PriorityQueue

bots = [map(int, re.findall("-?\d+", line)) for line in real_inp.split("\n")]
q = PriorityQueue()

for x,y,z,r in bots:
  d = abs(x) + abs(y) + abs(z)
  q.put((max(0, d - r),1))
  q.put((d + r + 1,-1))

count = 0
maxCount = 0
result = 0

while not q.empty():
  dist,e = q.get()
  count += e

  if count > maxCount:
    result = dist
    maxCount = count

print(result)

# %% [markdown]
# # networkx cliques (incorrect)

# %%
# https://www.reddit.com/r/adventofcode/comments/a8s17l/comment/ecf885b/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button
# https://github.com/blu3r4y/AdventOfCode2018/blob/master/src/day23.py
# (c) blu3r4y
# off by one for my input

import networkx as nx
import parse

X, Y, Z, RANGE = 0, 1, 2, 3
ORIGIN = (0, 0, 0, 0)


def part1d(bots):
    # find the nanobot with the largest range
    strongest = max(bots, key=lambda bot: bot[RANGE])
    distances = [manhattand(bot, strongest) for bot in bots]

    # number of nanobots in range of the strongest nanobot
    return len([d for d in distances if d <= strongest[RANGE]])


def part2d(bots):
    # build a graph with edges between overlapping nanobots
    graph = nx.Graph()
    for bot in bots:
        # two bots overlap if their distance is smaller or equal than the sum of their ranges
        overlaps = [(bot, other) for other in bots if manhattand(bot, other) <= bot[RANGE] + other[RANGE]]
        graph.add_edges_from(overlaps)

    # find sets of overlapping nanobots (i.e. fully-connected sub-graphs)
    cliques = list(nx.find_cliques(graph))
    cliques_size = [len(c) for c in cliques]

    assert len([s for s in cliques_size if s == max(cliques_size)]) == 1

    # select the largest cluster of overlapping nanobots (maximum clique sub-graph)
    clique = max(cliques, key=len)

    # calculate the point on the nanobots surface which is closest to the origin
    surfaces = [manhattan(ORIGIN, bot) - bot[RANGE] for bot in clique]

    # the furthest away surface point is the minimum manhattan distance
    return max(surfaces)


def manhattand(a, b):
    (x1, y1, z1, _), (x2, y2, z2, _) = a, b
    return abs(x1 - x2) + abs(y1 - y2) + abs(z1 - z2)


def _parse(lines):
    # list of tuples (x, y, z, range)
    return [tuple(parse.parse("pos=<{:d},{:d},{:d}>, r={:d}", line)) for line in lines]


if __name__ == "__main__":
    print(part1d(_parse(real_inp.split("\n"))))
    print(part2d(_parse(real_inp.split("\n"))))
