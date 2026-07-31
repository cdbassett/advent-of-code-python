from functools import *
from collections import *
from itertools import *
from math import *
from statistics import *
from builtins import pow
import pyperclip
from icecream import ic

from utils.aoc_utils import * # this includes adding c:\ut to sys.path
from utils.utilities import *
import utils.seq_extensions # these extend PyFunctional seq objects, don't need to directly use anything in it

PointVal = namedtuple("PointVal", "val,x,y")

def run(inp, is_real):
    ics = nothing if is_real else ic
    print_result = partial(print_result_aoc, is_real)

    inp = inp.strip().split('\n')
    h_map = [list(map(int, line)) for line in inp]
    width = len(h_map[0])
    height = len(h_map)
    ics(h_map)
    org_line_length = len(h_map[0])
    blank_line = [9] * (org_line_length + 2)
    x_map = h_map[:]

    for line in x_map:
        line.insert(0, 9)
        line.append(9)

    x_map = [blank_line] + x_map + [blank_line]
    ics(x_map)

    def pval(x, y):
        return x_map[y+1][x+1]

    def is_lowest(x, y):
        center = pval(x, y)
        return center < pval(x-1, y) and center < pval(x+1, y) and center < pval(x, y-1) and center < pval(x, y+1)

    low_points = []

    for x, y in product(range(width), range(height)):
        if is_lowest(x, y):
            low_points.append(PointVal(pval(x, y), x, y))

    ics(low_points)

    def part1():
        result = sum(lp.val + 1 for lp in low_points)
        print_result(result)


        # recursive
    def search_basin(x, y, tracker):
        if pval(x, y) == 9 or (x, y) in tracker:
            return 0

        tracker[(x, y)] = True
        size = 1
        size += search_basin(x-1, y, tracker)
        size += search_basin(x+1, y, tracker)
        size += search_basin(x, y-1, tracker)
        size += search_basin(x, y+1, tracker)
        return size

    def part2():
        basins = []

        for lp in low_points:
            tracker = {}
            basins.append(search_basin(lp.x, lp.y, tracker))

        basins = sorted(basins)
        ics(basins)
        largest = basins[-3:]
        result = largest[0] * largest[1] * largest[2]
        print_result(result)

    part1()
    part2()

def main():
    example = get_aocd_example()
    samp_inps = split_example(example)

    for n, samp_inp in enumerate(samp_inps, 1):
        print(f"{Fore.BLUE}{Style.BRIGHT}Sample {n}:{Style.RESET_ALL}")
        run(samp_inp, False)

    if 1:
        print(f"{Fore.BLUE}{Style.BRIGHT}Actual:{Style.RESET_ALL}")
        real_inp = get_aocd_data()
        run(real_inp, True)

main()
