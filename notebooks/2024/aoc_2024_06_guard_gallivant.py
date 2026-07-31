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
import re
import math

from icecream import ic

# %autoreload explicit
# import and reload these automatically
# %aimport aoc_utils, Utilities, iter_utils, seq_extensions, func_utils
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


# %% [markdown]
# # Parse

# %%
def parse_data(inp):
    return inp.strip().split("\n")


# %% [markdown]
# # Process

# %%
def iter_route_complex(grid, pos, dir, get_new_pos = operator.add):    
    yield pos, dir

    while True:
        while (c := grid.get(new_pos :=get_new_pos(pos, dir))) == "#":
            dir = dir * 1j

        if c is None:
            break
        else:
            yield (pos := new_pos), dir


# %%
def pos_and_dir_to_pos(positions):
    return seq(positions).map(itemgetter(0)).set()


# %%
def process(parsed):
    ics(parsed)
    grid = build_complex_points_dict(parsed)
    guard_pos = first(build_complex_points(parsed, sig_char="^"))
    grid[guard_pos] = "."
    up = -1j
    return len(pos_and_dir_to_pos(iter_route_complex(grid, guard_pos, up)))


# %%
def part1(inp):
    parsed = parse_data(inp)
    result = process(parsed)
    print_result(result)


# %%
# for 130x130 grid, dict of points was faster than complexindexlist (23s -> 13s)
# checking bounds via real and imag went from 23s -> 28s
# dict of tuples was noticeably slower than dict of complex 26s vs. 13/14s, possbily due to add_tuple vs. complex multiply

# %%
# ComplexIndexedList method
def plot_routea(grid, pos, dir, add_pos=None, dbg=False):
    positions = set([(pos, dir)])
    W, H = width_height(grid)

    try:
        while True:
            new_pos = pos + dir

            if new_pos == add_pos or grid[new_pos] == "#":
                dir = dir * 1j
            else:
                pos = new_pos
                
                if (pos, dir) in positions:
                    return True, positions

                positions.add((pos, dir))
    except IndexError as e:
        return False, positions

@timefunction
def process2aex(parsed):
    grid = ComplexIndexedList(parsed)
    guard_pos = first(build_complex_points(parsed, sig_char="^"))
    up = -1j
    _, positions = plot_routea(grid, guard_pos, up)
    obstruction_positions = set()
    checks = pas_and_dir_to_pos(positions)
    ics(checks)

    checks.discard(guard_pos)
    ic(len(positions), len(checks)) # positions incldues direction, checks does not
    
    for pos in checks:
        infinite, new_positions = plot_routea(grid, guard_pos, up, pos)
        
        if infinite:
            ics("infinite", pos)
            obstruction_positions.add(pos)
    

    if 0:
        route = seq(positions).map(itemgetter(0)).map(complex_to_tuple).sorted()
        points = sorted(map(complex_to_tuple, obstruction_positions))
        points = list(map(complex_to_tuple, obstruction_positions))
        ics(points)
        xs, ys = xs_and_ys(coords)
    
        for point in points:
            print_lines(f"{point}", get_vis_map_multiline_str(xs, ys, special_chars=[("*", x, y) for x, y in route] + [("O", point[0], point[1]), ("^",) + complex_to_tuple(guard_pos)]))
            print()
    
    return obstruction_positions
    
def process2a(parsed):
    return len(process2aex(parsed))


# %%
def iter_route_tuple(grid, pos, dir):
    yield pos, dir

    try:
        while True:
            if grid[(new_pos := add_tuple(pos, movements[dir]))] == "#":
                dir = (dir + 1) % 4
            else:
                yield (pos := new_pos), dir
    except IndexError as e:
        pass


# %%
# dict of complex positions method reduced to 13, plus starting loop check at obstruction reduced it to 5, skip_map brought it under 1s
@timefunction
def process2ex(parsed):
    def build_skip_map():
        def extend(ob_pos, dir):
            pos, reverse = ob_pos, dir * -1

            try:
                if grid[jump_pos := ob_pos + dir] != "#":
                    while grid[(new_pos := pos+dir)] != "#":
                        if jump_pos != (pos := new_pos):
                            skip_map[reverse][pos] = jump_pos
            except KeyError:
                pass
            
        obstruction_positions = list(build_complex_points(parsed, sig_char="#"))
        skip_map = defaultdict(dict)

        for ob_pos in obstruction_positions:
            for dir in movements_c:
                extend(ob_pos, dir)

        right = W-1
        bot = H-1
        
        for edge_pos in square_boundary_points_c(0, tuple_to_complex((W, H))):
            if edge_pos.real == 0:
                extend(edge_pos, 1)
            if edge_pos.real == right:
                extend(edge_pos, -1)
            if edge_pos.imag == 0:
                extend(edge_pos, 1j)
            if edge_pos.imag == bot:
                extend(edge_pos, -1j)
                            
        return skip_map

    def get_new_pos(ob_pos, pos, dir):
        if dir.imag and ob_pos.real == pos.real or dir.real and ob_pos.imag == pos.imag:
            return pos + dir
        
        try:
            return skip_map[dir][pos]
        except KeyError:
            return pos + dir

    W, H = width_height(parsed)
    grid = build_complex_points_dict(parsed)
    guard_pos = first(build_complex_points(parsed, sig_char="^"))
    grid[guard_pos] = "."
    up = -1j
    positions = list(iter_route_complex(grid, guard_pos, up))
    obstruction_positions, checked = set(), set()
    skip_map = build_skip_map()
    #ics(skip_map)

    # bug was that bc obstruction positions can be in the path more than once, we were counting crossing more than once and starting from the wrong positions for later crossings
    for (from_pos, from_dir), (ob_pos, _) in pairwise(positions):
        # we want the first occurrence of the obstruction in the path only            
        if ob_pos not in checked:
            grid[ob_pos] = "#"
            
            if repeats(iter_route_complex(grid, from_pos, from_dir, get_new_pos=partial(get_new_pos, ob_pos))):
                ics("infinite", ob_pos)
                obstruction_positions.add(ob_pos)
            
            grid[ob_pos] = "."
            checked.add(ob_pos)

    return obstruction_positions
    
def process2(parsed):
    return len(process2ex(parsed))


# %% [markdown]
# # Process2

# %%
def part2(inp):
    parsed = parse_data(inp)
    correct = process2ex(parsed)
    result = len(correct)
    #bogus = process2aex(parsed)
    #result = len(bogus)
    #ic(bogus - correct)
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

# %%
130*130

# %% editable=true slideshow={"slide_type": ""}
real_inp = get_aocd_data()
insert_sample_functions(True, globals())
part1(real_inp)
part2(real_inp)

# %%
# diagnostics to realize bug in ComplexIndexedList - was only checking for negative with real part twice and not imaginary
real_inp = get_aocd_data()
insert_sample_functions(True, globals())

parsed = parse_data(real_inp)
grida = ComplexIndexedList(parsed)
gridb = build_complex_points_dict(parsed)
guard_pos = first(build_complex_points(parsed, sig_char="^"))
org_ob_positions = seq(build_complex_points(parsed, sig_char="#")).map(complex_to_tuple).list()
ob_pos = 8+4j

infinitea, new_positionsa = plot_routea(grida, guard_pos, -1j, ob_pos)
new_positionsa = seq(pas_and_dir_to_pos(new_positionsa)).map(complex_to_tuple).set()
infiniteb, new_positionsb = plot_route(gridb, guard_pos, -1j, ob_pos)
new_positionsb = seq(pas_and_dir_to_pos(new_positionsb)).map(complex_to_tuple).set()
#ic(infinitea, infiniteb, new_positionsa - new_positionsb, new_positionsb - new_positionsa)
#ic(seq(new_positionsb).where(lambda p: not isinstance(p, complex)).first())
#assert all(isinstance(p, complex) for p in new_positionsb)
#assert all(isinstance(p, complex) for p in new_positionsa)
xs, ys = xs_and_ys(new_positionsa)
stra = get_vis_map_multiline_str(xs, ys, special_chars=[("*", x, y) for x, y in new_positionsa] + [("O",) + complex_to_tuple(ob_pos), ("^",) + complex_to_tuple(guard_pos)] + [("#",) + p for p in org_ob_positions])
#stra = get_vis_map_multiline_str(xs, ys, min_val=0, special_chars=[("*", x, y) for x, y in new_positionsa] + [("O",) + complex_to_tuple(ob_pos), ("^",) + complex_to_tuple(guard_pos)] + [("#",) + p for p in org_ob_positions])
print_lines("a", stra)
#pyperclip.copy("a\n" + stra)

xs, ys = xs_and_ys(new_positionsb)
strb = get_vis_map_multiline_str(xs, ys, special_chars=[("*", x, y) for x, y in new_positionsb] + [("O",) + complex_to_tuple(ob_pos), ("^",) + complex_to_tuple(guard_pos)] + [("#",) + p for p in org_ob_positions])
print_lines("b", strb)
#time.sleep(1000)
pyperclip.copy("b\n" + strb)
""

# %% [markdown]
# # Others' solutions

# %%
# https://old.reddit.com/r/adventofcode/comments/1h7tovg/2024_day_6_solutions/m0y49yx/
import itertools

def solution():
    class Table:
      def __init__(self, lines):
        self.table = lines
        self.w = len(self.table[0])
        self.h = len(self.table)
    
      def iter_all(self, conditional=lambda x: True):
        for j, i in itertools.product(range(self.h), range(self.w)):
          if conditional(self.table[j][i]):
            yield j, i
    
      def valid(self, j, i):
        return 0 <= j < self.h and 0 <= i < self.w
    
      def cvalid(self, complex_pos):
        return 0 <= complex_pos.imag < self.h and 0 <= complex_pos.real < self.w
    
    
      def __getitem__(self, j):
        return self.table[j]
    
      def get(self, complex_position):
        return self.table[int(complex_position.imag)][int(complex_position.real)]
    
      def put(self, complex_position, value):
        self.table[int(complex_position.imag)][int(complex_position.real)] = value
    

    def walk(t, start):
      vdir = -1j
      visited, prevmap, pos = set(), {}, start
        
      while t.cvalid(pos) and (pos, vdir) not in visited:
        visited.add((pos, vdir))
        prev = (pos, vdir)
          
        while t.cvalid(pos + vdir) and t.get(pos + vdir) == "#":
          vdir *= 1j
            
        if t.cvalid(pos + vdir):
          pos += vdir
            
        if pos not in prevmap:
          prevmap[pos] = prev
            
      return pos, visited, prevmap
    
    def run(t, start, skipmap, cpos):
      pos, vdir = start
      visited = set()
        
      while t.cvalid(pos) and (pos, vdir) not in visited:
        visited.add((pos, vdir))
          
        while t.cvalid(pos + vdir) and t.get(pos + vdir) == "#":
          vdir *= 1j
            
        if (t.cvalid(pos + vdir) and not          ((pos+vdir).real == cpos.real or (pos+vdir).imag == cpos.imag)):
          pos = skipmap[vdir][pos]
        else:
          pos += vdir
      return pos
    
    def original_path(t):
      j, i = next(t.iter_all(lambda x: x=="^"))
      start = j * 1j + i
      t[j][i] = "."
      pos, visited, prevmap = walk(t, start)
      return visited, start, prevmap
    
    def is_loop(t, start, skipmap, cpos):
      return t.cvalid(run(t, start, skipmap, cpos))
    
    def build_skipmap(t):
      dirs = [1, -1, 1j, -1j]
      axis = [1j, 1j, 1, 1]
      limits = [t.w, -1, 1j * t.h, -1j]
      skipmap = {k: {} for k in dirs}
        
      for vdir, hdir, limit in zip(dirs, axis, limits):
        for col in itertools.count(0):
          pos = col * hdir + limit - vdir      
          last = col * hdir + limit
            
          if not t.cvalid(pos):
            break
              
          while t.cvalid(pos):
            skipmap[vdir][pos] = last
              
            if t.get(pos) == "#":
              last = pos - vdir
                
            pos -= vdir
              
      return skipmap
    
    def find_blockers(t, visited, start, prevmap):
      skipmap = build_skipmap(t)
      ans = 0
        
      for cpos in set(cpos for cpos, vdir in visited):
        t.put(cpos, "#")
          
        if is_loop(t, prevmap.get(cpos, (start, -1j)), skipmap, cpos):
          ans += 1
            
        t.put(cpos, ".")
          
      return ans

    t = Table(list(map(list, get_aocd_data().splitlines())))
    visited, start, prevmap = original_path(t)
    print(len(set(cpos for cpos, vdir in visited)))
    print(find_blockers(t, visited, start, prevmap))
solution()    
