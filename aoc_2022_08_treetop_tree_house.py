from functools import *
from collections import *
from itertools import *
from math import *
from builtins import pow
import pyperclip
from icecream import ic


from aoc_utils import * # this includes adding c:\ut to sys.path
from Utilities import *
import seq_extensions # these extend PyFunctional seq objects, don't need to directly use anything in it

def run(inp, is_real):
    ics = nothing if is_real else ic
    print_result = partial(print_result_aoc, is_real)

    inp = inp.strip('\n').split('\n')
    h_map = [list(map(int, line)) for line in inp]
    width = len(h_map[0])
    height = len(h_map)
    ics(h_map)

    def pval(x, y):
        assert x < width
        assert x >= 0
        assert y < height
        assert y >= 0
        return h_map[y][x]

    def row_vals(y):
        return h_map[y]

    def col_vals(x):
        return [r[x] for r in h_map]

    def split_seq(point, seq):
        return seq[:point], seq[point+1:]

    def all_less(value, seq):
        return all(v < value for v in seq)

    def all_visible(x, y):
        if x == 0 or x == width -1 or y == 0 or y == height - 1:
            return True

        row = row_vals(y)
        col = col_vals(x)
        value = pval(x, y)

        left, right = split_seq(x, row)
        up, down = split_seq(y, col)

        if all_less(value, left) or all_less(value, right):
            return True

        if all_less(value, up) or all_less(value, down):
            return True

        return False

    def part1():
        vis_count = 0
        vis_map = [[0] * width for r in h_map]

        for x, y in product(range(width), range(height)):
            if all_visible(x, y):
                vis_count += 1
                vis_map[y][x] = 1

        ics(vis_map)

        result = vis_count
        print_result(result)


    def view_dist_line(val, seq):
        for n, v in enumerate(seq, 1):
            if v >= val:
                return n

#        return len(seq) - 1 if seq else 0
        return len(seq)

    def view_dist(x, y):
        row = row_vals(y)
        col = col_vals(x)
        value = pval(x, y)

        left, right = split_seq(x, row)
        up, down = split_seq(y, col)
        left = list(reversed(left))
        up = list(reversed(up))

#        ics(x, y)
#        ics(left, right, row)
#        ics(up, down, col)
        xl_dist = view_dist_line(value, left)
#        ics(xl_dist)
        xr_dist = view_dist_line(value, right)
#        ics(xr_dist)
        yu_dist = 0
        yu_dist = view_dist_line(value, up)
#        ics(yu_dist)
        yd_dist = view_dist_line(value, down)
#        ics(yd_dist)
        return yu_dist * yd_dist * xr_dist * xl_dist

    def part2():
        if 0:
            result = view_dist(2, 1)
            ics(result)
            result = view_dist(2, 3)
        else:
            view_distances = [view_dist(x, y) for x, y in product(range(width), range(height))]
            ics(view_distances)
            result = max(view_distances)
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
