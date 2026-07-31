import os
import sys
import operator
import math
from math import log10
import functools
import inspect
from collections import namedtuple, deque
from heapq import heappush, heappop, heappushpop, heapify, heapreplace
from bisect import bisect_left, bisect_right
import cmath
import re
import hashlib
from dataclasses import dataclass, field

from icecream import ic
import pyperclip
from colorama import Fore, Style
import numpy as np
import iteration_utilities
from functional import seq # https://github.com/EntilZha/PyFunctional
import aocd
import seq_extensions
import z3

# this code executes just by being imported
# =========================================

# token is kept in C:\Users\cbassett\.config\aocd\token


ut_dir = 'C:/ut'
if ut_dir not in sys.path: sys.path.append(ut_dir) # make modules in ut directory available

#print("loaded aoc_utils")

from func_utils import *
from iter_utils import *
from timer_utils import timefunction

try:
    ic.lineWrapWidth = os.get_terminal_size()[0] # make icecream take advantage of wider terminal
except:
    pass

ic.lineWrapWidth = 256
ic.configureOutput(outputFunction=print)

# =========================================

__JUPYTER___ = ""

def is_notebook():
    try:
        __IPYTHON__
        return True
    except NameError:
        return False

def is_marimo_notebook():
    try:
        import marimo as mo
        return mo.app_meta().mode == "edit"
    except ImportError:
        return False


def is_any_notebook():
    return is_notebook() or is_marimo_notebook()

__AOC_LIB_HELPERS__ = ""


aoc_runner_data = None # this gets set by aoc runner, a few things will behave differently
aocd_filename = None # can set this if filename is obscured by e.g. a notebook, although we try to handle jpyter and marimo

def get_aocd_day_and_year():
    override_aocd_filename = aocd_filename

    if is_marimo_notebook():
        frame = inspect.currentframe()

        while frame:
#            ic(inspect.getmodule(frame), inspect.getfile(frame), inspect.getsourcefile(frame), frame.f_globals.get("__file__"))
            frame_file = inspect.getfile(frame)
            frame_alleged_file = frame.f_globals.get("__file__") # marimo sets __file__, which is different than what inspect sees

            if frame_file != __file__ and frame_file != frame_alleged_file:
                override_aocd_filename = frame_alleged_file
                break
#            ic(inspect.getmodule(frame), inspect.getfile(frame), inspect.getsourcefile(frame), frame.f_locals)
#            ic(inspect.getmodule(frame), inspect.getfile(frame), inspect.getsourcefile(frame), frame.f_globals)
            frame = frame.f_back

    if is_notebook() or override_aocd_filename:
        # taken from aocd.get.get_day_and_year, which in current version of Jupyter fails to detect notebook name by itself
        pattern_year = r"201[5-9]|202[0-9]"
        pattern_day = r"2[0-5]|1[0-9]|[1-9]"

        if not override_aocd_filename:
            import ipynbname
            override_aocd_filename = ipynbname.name()

        years = {int(year) for year in re.findall(pattern_year, override_aocd_filename)}

        if len(years) > 1:
            raise Exception("Failed introspection of year")

        year = years.pop() if years else None
        basename_no_years = re.sub(pattern_year, "", override_aocd_filename)

        try:
            [day] = set(re.findall(pattern_day, basename_no_years))
        except ValueError:
            pass
        else:
            assert not day.startswith("0"), "regex pattern_day must prevent any leading 0"
            day = int(day)
            assert 1 <= day <= 25, "regex pattern_day must only match numbers in range 1-25"
#            log.debug("year=%s day=%s", year or "?", day)
            return day, year
    else:
        return aocd.get.get_day_and_year()


def get_aocd_example(aocd_day=None, aocd_year=None):
    if not aocd_day or not aocd_year:
        res = get_aocd_day_and_year()

        if res:
            d, y = res
            aocd_day = aocd_day or d
            aocd_year = aocd_year or y
        else:
            return "Couldn't determine day and year"

    import subprocess
    result = subprocess.run(['aocd',str(aocd_year), str(aocd_day), "-e"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    example = result.stdout.decode('utf-8').replace("\r\n","\n").split("\n")
    return example

def get_aocd_data():
    if aoc_runner_data:
        return aoc_runner_data

    res = get_aocd_day_and_year()

    if res:
        aocd_day, aocd_year = res
        return aocd.get_data(day=aocd_day, year=aocd_year)

    raise Exception("Failed introspection of day/year")

def get_aoc_url():
    aocd_day, aocd_year = get_aocd_day_and_year()
    return f"https://adventofcode.com/{aocd_year}/day/{aocd_day}"

def split_example(example):
    return seq(example).splitby(lambda s: s.startswith("--")).drop(1).grouped(3).map(first_elem).map(njoin).list()

def nothing(*msg, **kwargs):
    return msg[0] if msg else None

def print_preface(is_real, index=None):
    base_text = "Actual" if is_real else "Sample"
    postfix = "" if index is None else f" {index}"
    print(f"{Fore.GREEN}{Style.BRIGHT}{base_text}{postfix}:{Style.RESET_ALL}")


def print_result_aoc(is_real, r, part=None):
    try:
        r = r.item() # convert from numpy type to Python type if possible
    except:
        pass

    if r is None: # don't do anything, should mean we're not ready with answer yet
        return

    previous_frame = inspect.currentframe().f_back
#    ic(previous_frame)
    frame_info = inspect.getframeinfo(previous_frame)
#    ic(frame_info)
    part = part if part else "Part 1" if frame_info.function == "part1" else "Part 2" if frame_info.function == "part2" else "Unknown part"

    if aoc_runner_data:
        if is_real:
            print(f"{part} result: {r}")
    else:
        result_color = Fore.CYAN if is_marimo_notebook() else Fore.BLUE
        print(f"  {Fore.YELLOW}{Style.BRIGHT}{part} result: {result_color}{Style.BRIGHT}{r}{Style.RESET_ALL}")

        if is_real:
            pyperclip.copy(r)


def print_sample_aoc(is_real, *msg):
    if not is_real:
        print(*msg)


def print_lines(*msgs):
    for msg in msgs:
        print(msg)

def print_list_aoc(is_real, title, l):
    print("   ", title +": ", end="")

    if is_real:
        print(l[:10])
        print("      ", l[-10:])
    else:
        print(l)


def insert_sample_functions(is_real, ns):
    if aoc_runner_data:
        ns["is_sample"] = False
        ns["ics"] = nothing
        ns["print_sample"] = nothing
        ns["print_result"] = partial(print_result_aoc, is_real)
        ns["print_list"] = nothing
        ns["print_preface_notebook"] = nothing


    ns["is_sample"] = not is_real
    ns["ics"] = nothing if is_real else ic
    ns["print_sample"] = nothing if is_real else print
    ns["print_result"] = partial(print_result_aoc, is_real)
    ns["print_list"] = nothing if is_real else partial(print_list_aoc, is_real)
    ns["print_preface_notebook"] = nothing if is_any_notebook() else partial(print_preface, is_real)

#    if 0 and not is_any_notebook() and not aoc_runner_data:
    if not aoc_runner_data:
        # if from notebook but not notebook now, we want the execution time like we get in the notebook
        # timefunction now prevents double-wrapping
        if "part1" in ns:
#            ic(getattr(ns["part1"], 'timefunction_wrapped', False))
            ns["part1"] = timefunction(ns["part1"], msg = "    took %s")
#            ic(getattr(ns["part1"], 'timefunction_wrapped', False))

        if "part2" in ns:
#            ns["part2"] = timefunction(ns["part2"], "    ")
            ns["part2"] = timefunction(ns["part2"], msg = "    took %s")

"""
aoc_2016_08_two_factor_authentication.py
aoc_2018_10_the_stars_align.py
aoc_2019_08_space_image_format.py
aoc_2019_11_space_police.py
aoc_2022_10_cathode_ray_tube.py

"""
def ocr_aoc_letters(s):
    lines = s.split("\n")

    if 0 and len(lines) == 6:
        from advent_of_code_ocr import convert_6
        #    return convert_array_6(array, fill_pixel=1, empty_pixel=0)
        return convert_6(s)
    else:
        from aoc_ocr import OCR
        array = build_numpy_array_from_string_graph(s).T
        use = (array == "#").tolist()
        ocr = OCR(use)
        return ocr.as_string()





# =========================================

__STRING_FUNCTIONS__=""

sjoin = "".join
njoin = "\n".join

# string module data entries
#    ascii_letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
#    ascii_lowercase = 'abcdefghijklmnopqrstuvwxyz'
#    ascii_uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
#    digits = '0123456789'
#    hexdigits = '0123456789abcdefABCDEF'
#    octdigits = '01234567'
#    printable = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ \t\n\r\x0b\x0c'
#    punctuation = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
#    whitespace = ' \t\n\r\x0b\x0c'



# taken from aocd after they removed it
def string_to_integers(data):
    result = []
    for line in data.splitlines():
        matches = [int(n) for n in re.findall(r"-?\d+", line)]
        if matches:
            result.append(matches)
    if all(len(n) == 1 for n in result):
        # flatten the list if there is always 1 number per line
        result = [n for [n] in result]
    if len(result) == 1:
        # un-nest the list if there is only one line
        [result] = result
    return result


    # don't reduce to single int when one value
def string_to_integers_list(data):
    result = []
    for line in data.splitlines():
        matches = [int(n) for n in re.findall(r"-?\d+", line)]
        if matches:
            result.append(matches)
    if all(len(n) == 1 for n in result):
        # flatten the list if there is always 1 number per line
        result = [n for [n] in result]
    elif len(result) == 1 :
        # un-nest the list if there is only one line
        [result] = result
    return result




def replace_multi(s, replacements, new_string=""):
    for r in replacements:
        s = s.replace(r, new_string)

    return s


icf = ic.format
bint = functools.partial(int, base=2)


to_space_splitter = functools.partial(str.split, sep=" to ")
equals_space_splitter = functools.partial(str.split, sep=" = ")
colon_space_splitter = functools.partial(str.split, sep=": ")
colon_splitter = functools.partial(str.split, sep=":")
or_splitter = functools.partial(str.split, sep=" or ")
bin_or_splitter = functools.partial(str.split, sep=" | ")
comma_splitter = functools.partial(str.split, sep=",")
comma_space_splitter = functools.partial(str.split, sep=", ")
x_splitter = functools.partial(str.split, sep="x")
dash_splitter = functools.partial(str.split, sep="-")
arrow_splitter = functools.partial(str.split, sep=" -> ")
double_arrow_splitter = functools.partial(str.split, sep=" => ")

def rev_str(s):
    return s[::-1]


def pad_string_list(l):
    w = max(map(len, l))
    return [f'{s:<{w}}' for s in l]

def pad_multiline_string(s):
    return njoin(pad_string_list(s.split("\n")))


# ================================


map_int = partial(map, int)

increment = functools.partial(operator.add, 1)
decrement = rpartial(operator.sub, 1)

chunks_of_2 = rpartial(chunks_of_n, 2)

def z3_abs(x):
    return z3.If(x >= 0,x,-x)


__MATH__ = ""

# inputs just need to be iterable, output is tuple
def add_tuple(*iterables):
#    ic(list(iterables))
    return tuple(sum(p) for p in zip(*iterables))


def add_scalar(a, b):
    return tuple(aa + b for aa in a)

def subtract_tuple(a, b):
#    return tuple(aa - bb for aa, bb in zip(a, b))
    return tuple(starmap(operator.sub, zip(a, b)))

products = math.prod

#def multiply_tuple(a, b):
#    return tuple(aa * bb for (aa, bb) in zip(a, b))

def multiply(*iterables):
    return (products(p) for p in zip(*iterables))


# this version should allow multiplying elements of more than 2 iterables
def multiply_tuple(*iterables):
    return tuple(products(p) for p in zip(*iterables))


def multiply_scalar_tuple(a, b):
    return tuple(aa * b for aa in a)

def count_integer_digits(n):
    return int(log10(n)) + 1

# this version should allow adding elements of more than 2 iterables

def get_state_sequence(came_from, final_state):
    state_seq = [ final_state ]
    prev_state  = final_state

    while prev_state := came_from.get(prev_state):
        state_seq.append(prev_state)

    return list(reversed(state_seq))


#def products(seq):
#    return functools.reduce(operator.mul, seq)

    # split a sequence into two parts, head and tail
    # works for strings too
def head_tail(s, head_length=1):
    return s[:head_length], s[head_length:]


def polygon_area(x,y):
    # coordinate shift
    x_ = x - x.mean()
    y_ = y - y.mean()
    # everything else is the same as maxb's code
    correction = x_[-1] * y_[0] - y_[-1]* x_[0]
    main_area = np.dot(x_[:-1], y_[1:]) - np.dot(y_[:-1], x_[1:])
    return 0.5*np.abs(main_area + correction)
    #return np.abs(main_area + correction) // 2

    # area: determined by e.g. polygon_area, but this top and left grid points and not bottom and right
    # boundary: count of all boundary points in grid
    # this adjusts area to include all points inside bounding line and bounding line itself
def picks_theorem(area, boundary):
    return area + boundary // 2 + 1 # picks theorem https://en.wikipedia.org/wiki/Pick%27s_theorem


def make_tuple(*args):
    return args

def tuple_of(*args):
    return args


# returns radius, phi
def xy_to_polar(x, y):
    return cmath.polar(complex(x, y))

def polar_to_xy(r, phi):
    return r * math.cos(phi), r * math.sin(phi)



__NUMPY__ = ""
##########################################

# return array of chars from newline separated string
def build_numpy_array_from_string_graph(inp, line_func = list):
    return np.array(maplist(line_func, inp.split("\n"))).T

# return newline separated string from numpy array of strings
def build_string_from_numpy_string_array(a):
    return njoin(map(sjoin, a))

# return newline separated string from numpy array of ints, each element is index of character in s
def build_string_from_numpy_int_array(a, s):
    if 0:
        a_to_c = s.__getitem__
        a_to_c = np.vectorize(a_to_c)
        chars = a_to_c(a)
    else:
#        chars = replace_array_elements(a, enumerate(s))
#        chars = replace_array_elements(a, list(range(len(s))), list(s))
        chars = replace_array_elements_by_dict_alt(a, dict(enumerate(s)))

#    ic(chars)
#    ic(maplist(sjoin, chars))
    return njoin(map(sjoin, chars))

def replace_array_elements_in_place(data, from_values, to_values):
    replace = np.array([from_values, to_values])    # Create 2D replacement matrix
    mask = np.in1d(data, replace[0, :])                                   # Find elements that need replacement
    data[mask] = replace[1, np.searchsorted(replace[0, :], data[mask])]   # Replace elements

def replace_array_elements(data, from_values, to_values):
    data = np.copy(data)
    replace = np.array([from_values, to_values])    # Create 2D replacement matrix
    ic(data, replace)
    mask = np.in1d(data, replace[0, :])                                   # Find elements that need replacement
    data[mask] = replace[1, np.searchsorted(replace[0, :], data[mask])]   # Replace elements
    return data

# convert in-place array elements via dictionary (replace)
# https://stackoverflow.com/questions/3403973/fast-replacement-of-values-in-a-numpy-array/43917704#43917704
# rpboems for first use case I wanted: to cnvert numbers to characters of a string
def replace_array_elements_in_place_by_dict(data, replace):
    replace = np.array([list(replace.keys()), list(replace.values())])    # Create 2D replacement matrix
    mask = np.in1d(data, replace[0, :])                                   # Find elements that need replacement
    data[mask] = replace[1, np.searchsorted(replace[0, :], data[mask])]   # Replace elements

# another solution that may perform better with small number of unqiue elements in array
# does not operate in-place
# https://stackoverflow.com/a/16993364
def replace_array_elements_by_dict_alt(data, replace):
    u,inv = np.unique(data, return_inverse = True)
    return np.array([replace[x] for x in u])[inv].reshape(data.shape)


"""
filtsize = (3, 3)
a = np.zeros((10,10), dtype=np.float)
a[5:7,5] = 1

b = rolling_window(a, filtsize)
blurred = b.mean(axis=-1).mean(axis=-1)
So what we get when we do b = rolling_window(a, filtsize) is an 8x8x3x3 array, that's actually a view into the same memory as the original 10x10 array. We could have just as easily used different filter size along different axes or operated only along selected axes of an N-dimensional array (i.e. filtsize = (0,3,0,3) on a 4-dimensional array would give us a 6 dimensional view).

We can then apply an arbitrary function to the last axis repeatedly to effectively calculate things in a moving window.
However, because we're storing temporary arrays that are much bigger than our original array on each step of mean (or std or whatever), this is not at all memory efficient! It's also not going to be terribly fast, either.

The equivalent for ndimage is just:
blurred = scipy.ndimage.uniform_filter(a, filtsize, output=a)
This will handle a variety of boundary conditions, do the "blurring" in-place without requiring a temporary copy of the array, and be very fast. Striding tricks are a good way to apply a function to a moving window along one axis, but they're not a good way to do it along multiple axes, usually....
"""
def rolling_window_lastaxis(a, window):
    """Directly taken from Erik Rigtorp's post to numpy-discussion.
    <http://www.mail-archive.com/numpy-discussion@scipy.org/msg29450.html>"""
    """
    Make an ndarray with a rolling window of the last dimension

    Parameters
    ----------
    a : array_like
        Array to add rolling window to
    window : int
        Size of rolling window

    Returns
    -------
    Array that is a view of the original array with a added dimension
    of size w.

    Examples
    --------
    >>> x=np.arange(10).reshape((2,5))
    >>> rolling_window(x, 3)
    array([[[0, 1, 2], [1, 2, 3], [2, 3, 4]],
           [[5, 6, 7], [6, 7, 8], [7, 8, 9]]])

    Calculate rolling mean of last dimension:
    >>> np.mean(rolling_window(x, 3), -1)
    array([[ 1.,  2.,  3.],
           [ 6.,  7.,  8.]])
    """
    if window < 1:
       raise ValueError("`window` must be at least 1.")
    if window > a.shape[-1]:
       raise ValueError("`window` is too long.")
    shape = a.shape[:-1] + (a.shape[-1] - window + 1, window)
    strides = a.strides + (a.strides[-1],)
    return np.lib.stride_tricks.as_strided(a, shape=shape, strides=strides)

# this should handle multiple dimensions
def rolling_window(a, window):
    if not hasattr(window, '__iter__'):
        return rolling_window_lastaxis(a, window)
    for i, win in enumerate(window):
        if win > 1:
            a = a.swapaxes(i, -1)
            a = rolling_window_lastaxis(a, win)
            a = a.swapaxes(-2, i)
    return a



###############################

# given a 2 level junctions dict of dicts (such as returned from dijkstra_reduced_node_connections)
# convert the keys of the first and second level dict and
def convert_junction_keys(junction_nodes, key_mapper):
    def junction_to_new_keys(dct):
        return dict((key_mapper(k), v) for k, v in dct.items())

    junctions_by_char = dict((key_mapper(k), junction_to_new_keys(v)) for k, v in junction_nodes.items())
    return junctions_by_char

__2D_3D_GRID__ = ""

# allows referring to list of string that represents a 2D array
# by e.g. data[x, y] instead of data[y][x]
# can also get 2D array referenced this way via np.array(maplist(list, parsed)).T (becomes array of chars)
# that also handles proper slicing in both dimensions includign assignemnt
@dataclass
class ParsedCharArray:
    arr: list

    def __getitem__(self, *args):
        if len(args) != 1 or len(args[0]) != 2:
            raise TypeError

        return self.arr[args[0][1]][args[0][0]]

    def width(self):
        return len(self.arr[0])

    def height(self):
        return len(self.arr)

    # width, height
    def shape(self):
        return len(self.arr[0]), len(self.arr)



# originally took Table class from https://github.com/ricbit/advent-of-code/tree/main/aoc
# bc I liked it
# however I flipped so references are x, y instead of y, x
# and [] acccess is with tuple of x, y
class CharTable:
    def __init__(self, lines):
      self.table = lines
      self.w = len(self.table[0])
      self.h = len(self.table)

    def iter_all(self, conditional=lambda x: True):
      for y, x in itertools.product(range(self.h), range(self.w)):
        if conditional(self.table[y][x]):
          yield x, y

    def iter_all_with_char(self, conditional=lambda x: True):
      for y, x in itertools.product(range(self.h), range(self.w)):
        if (conditional(c := self.table[y][x])):
          yield x, y, c

    def get_char_coords(self, find_c="#", build_point = make_tuple):
#        for y, line in enumerate(self.table, y_start):
#            for x, c in enumerate(self.table, x_start):

        for y, x in itertools.product(range(self.h), range(self.w)):
            if self.table[y][x] == find_c:
                yield build_point(x, y)

    def grow(self, empty=" "):
      empty_line = [empty] * (self.w + 2)
      new_table = [empty_line] + [[empty] + line + [empty] for line in self.table] + [empty_line]
      return Table(new_table)

    def valid(self, x, y):
      return 0 <= y < self.h and 0 <= x < self.w

    def cvalid(self, complex_pos):
      return 0 <= complex_pos.imag < self.h and 0 <= complex_pos.real < self.w

    def iter_neigh8(self, x, y, conditional=lambda x: True):
      for dy, dx in itertools.product(range(-1, 2), repeat=2):
        if dy == 0 and dx == 0:
          continue

        yy, xx = y + dy, x + dx

        if self.valid(xx, yy) and conditional(self.table[yy][xx]):
          yield xx, yy

    def iter_neigh4(self, x, y):
      if y > 0:
        yield x, y - 1

      if y < self.h - 1:
        yield x, y + 1

      if x > 0:
        yield x - 1, y

      if x < self.w - 1:
        yield x + 1, y

    # can access by int, tuple or complex

    @singledispatchmethod
    def __getitem__(self, pos):
        raise NotImplementedError(f"Cannot index on {instance(pos)}")

    @__getitem__.register
    def _(self, pos: tuple):
        #if len(args) != 1 or len(args[0]) != 2:
        #    raise TypeError
        return self.table[pos[1]][pos[0]]

    @__getitem__.register
    def _(self, pos: int):
        return self.table[pos]

    @__getitem__.register
    def _(self, pos: complex):
        return self[int(pos.imag)][int(pos.real)]

    @singledispatchmethod
    def __setitem__(self, pos, value):
        raise NotImplementedError(f"Cannot index on {instance(pos)}")

    @__setitem__.register
    def _(self, pos: tuple, value):
        #if len(args) != 1 or len(args[0]) != 2:
        #    raise TypeError
        self.table[pos[1]][pos[0]] = value

    @__setitem__.register
    def _(self, pos: int, value):
        self.table[pos] = value

    @__setitem__.register
    def _(self, pos: complex, value):
        self.table[int(pos.imag)][int(pos.real)] = value


    # get or put however use complex numebrs
    def get(self, complex_position):
      return self.table[int(complex_position.imag)][int(complex_position.real)]

    def put(self, complex_position, value):
      self.table[int(complex_position.imag)][int(complex_position.real)] = value

    def transpose(self):
      return Table([list(t) for t in zip(*self.table)])

    def clock90(self):
      return Table([list(reversed(col)) for col in zip(*self.table)])

    def copy(self):
      return Table([line.copy() for line in self.table])

    def flipx(self):
      return Table([list(reversed(t)) for t in self.table])

    def iter_quad(self, x, y, h, w):
      for j in range(h):
        for i in range(w):
          yield y + j, x + i

    def __repr__(self):
        return repr(self.table)


def distance_sq(a, b):
    return sum(d**2 for d in subtract_tuple(a, b))

distance = math.dist

#def distance(a, b):
#    return math.sqrt(distance_sq(a, b))


def manhattan(a, b=(0,0,0)):
    return sum(abs(d) for d in subtract_tuple(a, b))

def manhattan_c(a, b=0j):
    diff = a - b
    return abs(int(diff.real)) + abs(int(diff.imag))

def manhattan_distance_neighbors(p1, r=20):
    for p2 in product(range(-r, r), repeat=2):
        if manhattan(p2) <= r:
            yield add_tuple(p1, p2)
#    for p2 in product(range(p1[0]-r, p1[0]+r), range(p1[1]-r, p1[1]+r)):
#        if manhattan(p1, p2) <= r:
#            yield p2

def manhattan_distance_neighbors_c(p1, r=20):
    for x, y in product(range(-r, r), repeat=2):
        if manhattan_c((p2 := x + y *1j)) <= r:
            yield p1 + p2


def manhattan_hex(a, b=(0,0,0)):
    return sum(abs(d) for d in subtract_tuple(a, b)) // 2


movements = ( # up, right, down, left
    (0, -1),
    (1, 0),
    (0, 1),
    (-1, 0),
    )

move_up, move_right, move_down, move_left = movements

#movements_np = [np.array([t[1], t[0]]) for t in movements] # we want numpy movements as array with y first
movements_np = maplist(np.array, movements) # we want numpy movements as arrays

movements_3d = [
    (1, 0, 0),
    (0, 1, 0),
    (0, 0, 1),
    (-1, 0, 0),
    (0, -1, 0),
    (0, 0, -1),
    ]

movements_c = [
    -1j, # North
    1, # East
    1j, # South
    -1, # West
    ]

move_up_c, move_right_c, move_down_c, move_left_c = movements_c

# UR, LR, LL, UL
# [(1, -1), (1, 1), (-1, 1), (-1, -1)]
corner_movements = list(starmap(add_tuple, pairwise(movements + movements[:1])))

compass_movements = dict(zip("NESW", movements))
compass_full_movements = dict(zip(("north", "east", "south", "west"), movements))
vertical_movements = dict(zip("URDL", movements))
arrow_movements = dict(zip("^>v<", movements))
arrow_movements_c = dict(zip("^>v<", movements_c))
reverse_arrow_movements = dict(zip("v<^>", movements))
reverse_arrow_movements_c = dict(zip("v<^>", movements_c))


reverse_arrow_lookup = {
    "v": "^",
    "<": ">",
    "^": "v",
    ">": "<",
    }

diag_neighbors = [
    (-1, -1), (0, -1), (1, -1),
    (-1, 0),          (1, 0),
    (-1, 1),  (0, 1), (1, 1),]

diag_neighbors_c = list(starmap(complex, diag_neighbors))

# q, r, s
cart_hex_movement = {
    "ne": (1, -1, 0),
    "nw": (-1, 0, 1),
    "n": (0, -1, 1),
    "se": (1, 0, -1),
    "sw": (-1, 1, 0),
    "s": (0, 1, -1),
    }

left_vector_transform, straight_vector_transform, right_vector_transform = [
    [[0, -1], [1, 0]],
    [[1, 0], [0, 1]],
    [[0, 1], [-1, 0]]
]

# this should work for 2D as well
# a and b are ((x1, x2), (y1,y2), (z1,z2)))
def cubes_intersection(a, b):
    new_bounds = tuple((max((ar[0], br[0])), min((ar[1], br[1]))) for ar, br in zip(a, b))
    return new_bounds if all(r[0] <= r[1] for r in new_bounds) else None

# this should work for 2D as well
rects_intersection = cubes_intersection

    # return a range that covers the overlap
    # if ranges don't overlap a range will still be returned, check if empty via len(rng)
def range_intersection(x, y):
    return range(max(x[0], y[0]), min(x[-1], y[-1])+1)

def rects_intersect(r1, r2):
    return (r2.x <= r1.x < r2.x + r2.w or r1.x <= r2.x < r1.x + r1.w) \
       and (r2.y <= r1.y < r2.y + r2.h or r1.y <= r2.y < r1.y + r1.h)


def cube_side_width(side):
    return side[1]-side[0]+1

# cuboid is ((x1, x2), (y1,y2), (z1,z2)))
def cube_volume(cuboid):
    return math.prod(map(cube_side_width, cuboid))

Point2D = namedtuple("Point2D", "x,y")
Point3D = namedtuple("Point3D", "x,y,z")

def complex_to_point(z):
    return Point2D(int(z.real), int(z.imag))

def complex_to_tuple(z):
    return (int(z.real), int(z.imag))

def tuple_to_complex(t):
    return t[0] + t[1] * 1j

def get_char_coords(lines, find_c="#", build_point = make_tuple, x_start=0, y_start=0):
#    ic(width(lines), height(lines))

    for y, line in enumerate(lines, y_start):
        for x, c in enumerate(line, x_start):
            if c == find_c:
                yield build_point(x, y)

get_hash_coords = get_char_coords

def get_chars_and_coords(lines, build_point = make_tuple, x_start=0, y_start=0):
    for y, line in enumerate(lines, y_start):
        for x, c in enumerate(line, x_start):
            yield c, build_point(x, y)


# parsed is list of strings, # indicates a point should be generated
# returns set of Point2D objects
def build_points(parsed, sig_char="#"):
    full_width = width(parsed)
    full_height = height(parsed)
    #ic(full_width, full_height)
    points = set()

    for x, y in product(range(full_width), range(full_height)):
        if parsed[y][x] == sig_char:
            points.add(Point2D(x, y))

    return points

def build_tuple_points(parsed, sig_char="#"):
    full_width = width(parsed)
    full_height = height(parsed)
    #ic(full_width, full_height)
    points = list()

    for y, x in product(range(full_height), range(full_width)):
        if parsed[y][x] == sig_char:
            points.append((x, y))

    return points

def build_tuple_points_dict(parsed):
    full_width = width(parsed)
    full_height = height(parsed)
    #ic(full_width, full_height)
    points = dict(((x, y), parsed[y][x]) for x, y in product(range(full_width), range(full_height)))
    return points


# parsed is list of strings, # indicates a point should be generated
# returns set of complex numbers
def build_complex_points(parsed, sig_char="#"):
    full_width = width(parsed)
    full_height = height(parsed)
    #ic(full_width, full_height)
    points = set()

    for x, y in product(range(full_width), range(full_height)):
        if parsed[y][x] == sig_char:
            points.add(x+y*1j)

    return points

def build_complex_points_dict(parsed):
    full_width = width(parsed)
    full_height = height(parsed)
    #ic(full_width, full_height)
    points = dict((x+y*1j, parsed[y][x]) for x, y in product(range(full_width), range(full_height)))
    return points

def repr_m(m):
    return ["".join(line) for line in m]


# for 2D array
def height(a):
    return len(a)

# for 2D array
def width(a):
    return len(a[0])

def width_height(a):
    return width(a), height(a)


# returns length (max - min + 1), min, max
def analyze_dimension(numbers):
    numbers = list(numbers)
    max_x, min_x = max(numbers), min(numbers)
    length = max_x - min_x + 1
    return length,  min_x, max_x

# points is sequence of tuples
def analyze_points(points):
    max_x, min_x = max(points, key = first_elem)[0], min(points, key = first_elem)[0]
    max_y, min_y = max(points, key = second_elem)[1], min(points, key = second_elem)[1]
    W, H = max_x - min_x + 1, max_y - min_y + 1
#    ic(W, H, W*H, min_x, max_x, min_y, max_y)
    return W, H, min_x, min_y, max_x, max_y

def get_point_set_bounds(dots):
    assert(dots)
    xs = list(p.x for p in dots)
    ys = list(p.y for p in dots)
    return (min(xs), max(xs)), (min(ys), max(ys))

def get_xy_bounds(xs, ys):
    return (min(xs), max(xs)), (min(ys), max(ys))


# returns generator of tuples that are points in a square
def square_boundary_points(x1, y1, x2, y2):
    yield from zip(range(x1, x2), cycle([y1]))
    yield from zip(cycle([x2]), range(y1, y2))
    yield from zip(reversed(range(x1+1, x2+1)), cycle([y2]))
    yield from zip(cycle([x1]), reversed(range(y1+1, y2+1)))

# maybe someday work out in complex numbers if need better performance
def square_boundary_points_c(p1, p2):
    x1, y1 = complex_to_tuple(p1)
    x2, y2 = complex_to_tuple(p2)
    return map(tuple_to_complex, square_boundary_points(x1, y1, x2, y2))


# for use in ic, use min width of 15 to ensure each element is on own line
# dots is sequence of Point2D objects
def get_vis_map(dots, reversed = False, min_val=None, max_val=None):
    def get_dim(dims):
        dims = list(dims)
#        assert(dots)
        negative_x = min(dims) if min_val is None else min_val
        positive_x = max(dims) + 1 if max_val is None else max_val
        return -negative_x, max(15, positive_x - negative_x)

    assert(dots)
    min_x, width = get_dim(map(first_elem, dots))
    min_y, height = get_dim(map(second_elem, dots))
#    ics(min_x, min_y)
    vis_map = [["."] * width for r in range(height)]

    for px, py, *_ in dots:
        try:
            if reversed:
                vis_map[height - (py + min_y) - 1][px + min_x] = "#"
            else:
                vis_map[py + min_y][px + min_x] = "#"
        except IndexError:
            ic(py, px)
            raise

    vis_map = [f"({-min_x},{-min_y})"] + ["".join(e) for e in vis_map]
#        vis_map = "\n".join("".join(e) for e in vis_map)
    return vis_map

def get_axis_strings(min_val, max_val):
    axis_width = max(len(str(min_val)), len(str(max_val)))
    return axis_width, [str(y).rjust(axis_width) for y in range(min_val, max_val+1)]

def Point(x, y):
    return x, y

graph_char_light_block = "\u2591"
graph_char_circle_cross = "\u2295"
graph_char_small_dot = "\u2218"
graph_char_bullseye = "\u25CE"

def xs_and_ys(points):
    return zip(*points)

def get_vis_map_multiline_str(xs, ys, reversed = False, min_val=None, max_val=None, special_chars=tuple(), blank_char =".", filled_char = "#", show_axis=True):
    def get_dim(dims):
        negative_x = min(dims) if min_val is None else min_val
        positive_x = max(dims) if max_val is None else max_val
        return negative_x, positive_x, positive_x - negative_x + 1

    def put_char(c, x, y):
        if min_x <= x <= max_x and min_y <= y <= max_y:
            try:
                if reversed:
                    vis_map[height - (y - min_y) - 1][x - min_x] = c
                else:
                    vis_map[y - min_y][x - min_x] = c
            except IndexError:
                ic(y, x)
                raise

    dim_xs = list(xs)
    dim_ys = list(ys)

    min_x, max_x, width = get_dim(dim_xs + maplist(second_elem, special_chars))
#    ic(min_x, max_x, width)
    min_y, max_y, height = get_dim(dim_ys + maplist(third_elem, special_chars))
#    ic(min_y, max_y, height)
    vis_map = [[blank_char] * width for r in range(height)]

    seq(zip(cycle((filled_char,)), dim_xs, dim_ys)).starforeach(put_char)
    seq(special_chars).starforeach(put_char)

    if show_axis:
        yaxis_w, yaxis = get_axis_strings(min_y, max_y)
        xaxis_h, xaxis = get_axis_strings(min_x, max_x)
#    ic(yaxis_w, xaxis_h)
            # transpose
        x_axis_hdr = "".rjust(yaxis_w+1)
        xaxis = list(x_axis_hdr + "".join(e) for e in zip(*xaxis)) + [x_axis_hdr + "_" * width]

        vis_map = xaxis + [ya + "|" + "".join(e) for ya, e in zip(yaxis, vis_map)]
        vis_map = "\n".join(vis_map)
    else:
        vis_map = "\n".join(map(sjoin, vis_map))

    return vis_map

def get_vis_map_multiline_str_def(walls_tuples, path, end_pos=None):
    special_chars = [(graph_char_circle_cross, x, y) for x, y in path]

    if end_pos:
        special_chars += [(graph_char_bullseye, end_pos[0], end_pos[1])]

    return get_vis_map_multiline_str(map_list(first_elem, walls_tuples), map_list(second_elem, walls_tuples), special_chars=special_chars, filled_char=graph_char_light_block, blank_char=graph_char_small_dot)


def get_double_axis_strings(min_val, max_val):
    axis_width = max(len(str(min_val)), len(str(max_val)))
    blank = " " * axis_width
    strings = [y for x in range(min_val, max_val+1) for y in (blank, str(x).rjust(axis_width))] + [blank]
    return axis_width, strings


def get_edge_grid_map_multiline_str(edges, start=(0,0), special_chars=tuple(), blank_char =".", filled_char = "#"):
    def get_dim(dims):
        negative_x = min(dims)*2-1
        positive_x = max(dims)*2+1
        return negative_x, positive_x, positive_x - negative_x + 1

    def put_char(c, x, y):
        if min_x <= x <= max_x and min_y <= y <= max_y:
            #x *= 2
            #y *= 2
            try:
                vis_map[y - min_y][x - min_x] = c
            except IndexError:
                ic(y, x)
                raise

    def put_char_t(c, x, y):
#        put_char(c, x*2 + 1, y * 2 + 1)
        put_char(c, x * 2, y * 2)

    points = set(edges.keys())
    #ic(edges, points)
    xs, ys = xs_and_ys(points)
    dim_xs = list(xs)
    dim_ys = list(ys)

    min_x, max_x, width = get_dim(dim_xs + maplist(second_elem, special_chars))
    min_y, max_y, height = get_dim(dim_ys + maplist(third_elem, special_chars))
    vis_map = [[blank_char] * width for r in range(height)]

    xbs, ybs = xs_and_ys(square_boundary_points(min_x, min_y, max_x, max_y))
    seq(zip(cycle((filled_char,)), xbs, ybs)).starforeach(put_char)

    # wall grid before replacing some with edges
    xi_range, yi_range = range(min_x, max_x+1, 2), range(min_y, max_y+1, 2)
    x_range, y_range = range(min_x, max_x+1), range(min_y, max_y+1)
    xis, yis = xs_and_ys(chain(product(x_range, yi_range), product(xi_range, y_range)))
    seq(zip(cycle((filled_char,)), xis, yis)).starforeach(put_char)
    put_char_t("X", start[0], start[1])


    for p1, s in edges.items():
        for p2 in s:
            assert p1[0] == p2[0] or p1[1] == p2[1]

            if p1[0] == p2[0]:
                put_char("-", p1[0]*2, min(p1[1], p2[1])*2+1)
            else:
                put_char("|", min(p1[0], p2[0])*2+1, p1[1]*2)


    #seq(zip(cycle((filled_char,)), dim_xs, dim_ys)).starforeach(put_char)
    #seq(special_chars).starforeach(put_char)

    yaxis_w, yaxis = get_double_axis_strings((min_y+1)//2, (max_y-1)//2)
    xaxis_h, xaxis = get_double_axis_strings((min_x+1)//2, (max_x-1)//2)
        # transpose
    x_axis_hdr = "".rjust(yaxis_w+1)
    xaxis = list(x_axis_hdr + "".join(e) for e in zip(*xaxis)) + [x_axis_hdr + "_" * width]

    vis_map = xaxis + [ya + "|" + "".join(e) for ya, e in zip(yaxis, vis_map)]
    vis_map = "\n".join(vis_map)
    return vis_map


def get_numpy_char_array_repr(data, reversed = False, min_val=None, max_val=None, special_chars=tuple(), show_axis=True):
    special_chars = [(data[y, x], x, y) for x, y in product(range(len(data[0])), range(len(data)))] + list(special_chars)
    return get_vis_map_multiline_str([], [], reversed = reversed, min_val=min_val, max_val=max_val, special_chars=special_chars, show_axis=show_axis)


def get_chartable_list_repr(table, reversed = False, min_val=None, max_val=None, special_chars=tuple(), show_axis=True):
    special_chars = [(table[x, y], x, y) for x, y in product(range(table.w), range(table.h))] + list(special_chars)
    return get_vis_map_multiline_str([], [], reversed = reversed, min_val=min_val, max_val=max_val, special_chars=special_chars, show_axis=show_axis)

#def stitch_multiline_strings_horizontally(strings, gap=1):



# decorator to track how many times a function is called
def counted(f):
    def wrapped(*args, **kwargs):
        wrapped.call_count += 1
        return f(*args, **kwargs)

    wrapped.call_count = 0
    return wrapped

# works for sequence of strings or sequence of sequences
def flatten_2D_array(lines):
    return seq(lines).map(list).flatten().to_list()


# returns list of sequences
def rebuild_2D_array(flattened, w):
    return list(chunks_of_n(flattened, w))


# returns list of strings
def rebuild_2D_string_array(flattened, w):
    return [sjoin(line) for line in chunks_of_n(flattened, w)]

# for BFS
def get_queue_functions_fifo(queue=None):
    if queue is None:
        queue = deque()

    put = queue.append
    get = queue.popleft
    return put, get


def get_queue_functions_lifo(queue=None):
    if queue is None:
        queue = []

    put = queue.append
    get = queue.pop
    return put, get


    # for djikstra or A*, depending on whether we can estimate remaining cost
def get_queue_functions_smallest(queue=None):
    if queue is None:
        queue = []

    put = partial(heappush, queue)
    get = partial(heappop, queue) # then get smallest
    return put, get

    # use when list is sorted smallest first
def binary_search(a, x):
    i = bisect_left(a, x)

    if i != len(a) and a[i] == x:
        return i
    else:
        return -1

    # use when list is sorted largest first
def binary_search_reverse(a, x):
    i = bisect_left(a, -x, key = lambda n: -n)

    if i != len(a) and a[i] == x:
        return i
    else:
        return -1


#    bisect.bisect_left(a, x, lo=0, hi=len(a), *, key=None)
#    Locate the insertion point for x in a to maintain sorted order. The parameters lo and hi may be used to specify a subset of the list which should be considered; by default the entire list is used. If x is already present in a, the insertion point will be before (to the left of) any existing entries. The return value is suitable for use as the first parameter to list.insert() assuming that a is already sorted.
#    The returned insertion point i partitions the array a into two halves so that all(val < x for val in a[lo : i]) for the left side and all(val >= x for val in a[i : hi]) for the right side.
#
#    bisect.bisect_right(a, x, lo=0, hi=len(a), *, key=None)
#    bisect.bisect(a, x, lo=0, hi=len(a), *, key=None)
#    Similar to bisect_left(), but returns an insertion point which comes after (to the right of) any existing entries of x in a.
#    The returned insertion point i partitions the array a into two halves so that all(val <= x for val in a[lo : i]) for the left side and all(val > x for val in a[i : hi]) for the right side.


def binary_search_lt(a, x):
    'Find rightmost value less than x'
    i = bisect_left(a, x)
    if i:
        return a[i-1]
    raise ValueError

def binary_search_le(a, x):
    'Find rightmost value less than or equal to x'
    i = bisect_right(a, x)
    if i:
        return a[i-1]
    raise ValueError

def binary_search_gt(a, x):
    'Find leftmost value greater than x'
    i = bisect_right(a, x)
    if i != len(a):
        return a[i]
    raise ValueError

def binary_search_ge(a, x):
    'Find leftmost item greater than or equal to x'
    i = bisect_left(a, x)
    if i != len(a):
        return a[i]
    raise ValueError


def md5hex(s):
    return hashlib.md5(s.encode("ascii")).hexdigest()

__ALGORITHMS__ = ""


# given a generator that returns hashable values and cycles, look for value to repeat itself and then predict what the value will be
def predict(gen, cycles):
    def state_by_index(idx):
        return first_element(k for k, v in seen.items() if v == idx)

    seen = { }

    for idx, new_state in enumerate(gen):
        if new_state in seen:
            break

        seen[new_state] = idx

    first_idx_of_cycle = seen[new_state]

    if 0:
        ic(idx+1, "=============")
        print_map(all_cube_rocks[0], process_next(round_rocks))
        ics(first_idx_of_cycle+1, "=============")
        print_map(all_cube_rocks[0], points_from_state(state_by_index(first_idx_of_cycle+1)))

    #ics(state_by_index(idx+1), state_by_index(first_idx_of_cycle+1))
    cycle_length = idx - first_idx_of_cycle
    final_cycle_idx = (cycles - 1 - first_idx_of_cycle) % (cycle_length) + first_idx_of_cycle
    ic(idx, first_idx_of_cycle, cycle_length, final_cycle_idx)
    return state_by_index(final_cycle_idx)


def find_lowest(func, low, high):
    "Find lowest value to pass to function to make it return True"

    assert not func(low)

        # first increase until we find a value for which function is true
    while not func(high):
        high *= 2

    while high > low:
        midpoint = (low + high) / 2.0

        if func(midpoint):
            high = midpoint
        else:
            low = midpoint

    return midpoint

# same as find_lowest but with only integer values
def find_lowest_int(func, low, high):
    "Find lowest value to pass to function to make it return True"

    assert not func(low)

        # first increase until we find a value for which function is true
    while not func(high):
        low = high
        high *= 2
        #ic("inc", low, high)

    while high > low + 1:
        midpoint = (low + high) // 2

        if func(midpoint):
            #ic("passed", low, high, midpoint)
            high = midpoint
        else:
            low = midpoint
            #ic("failed", low, high, midpoint)

    return low if func(low) else high


