from functools import *
from collections import *
from itertools import *
from math import *
from statistics import *
from builtins import pow
import pyperclip
from icecream import ic
import iteration_utilities as it_ut

from aoc_utils import * # this includes adding c:\ut to sys.path
from Utilities import *
import seq_extensions # these extend PyFunctional seq objects, don't need to directly use anything in it

Point = Point2D


def run(inp, is_real):
    insert_sample_functions(is_real, globals())
    print_preface(is_real)

    inp = inp.strip().split('\n')
    dots_list = sorted(Point(*map(int, line.split(","))) for line in inp if line and not line.startswith("fold"))
#    ics(dots_list)
    ics(len(dots_list))
    folds = [line.split()[-1].split("=") for line in inp if line.startswith("fold")]
    folds = [(f[0], int(f[1])) for f in folds]
#    folds = [(f := fold[-1].split("=")) for fold in folds]
#    ics(folds)

    def get_vis_map(dots):
        xs, ys = xs_and_ys(dots)
        return get_vis_map_multiline_str(xs, ys)

    print_sample(get_vis_map(dots_list))

    def folded_value(fold_val, val):
        return  -val + fold_val * 2

    def fold_once(dots, axis, fold_val):
        ics(axis, fold_val, len(dots))

        if axis == "x":
            preserve, mirror = it_ut.partition(dots, lambda d: d.x > fold_val)
            new_dots = set(Point(folded_value(fold_val, d.x), d.y) for d in mirror)
        else:
            preserve, mirror = it_ut.partition(dots, lambda d: d.y > fold_val)
            new_dots = set(Point(d.x, folded_value(fold_val, d.y)) for d in mirror)

        print_sample(get_vis_map(preserve))
        print_sample(get_vis_map(new_dots))
#        ics(len(new_dots))
#        ics(preserve)
#        ics(new_dots)
        assert all(p.y >= 0 for p in new_dots)
        assert all(p.y >= 0 for p in new_dots)
        new_dots.update(preserve)
        return sorted(new_dots)

    def part1():
        axis, fold_val = folds[0]
        new_dots = fold_once(dots_list, axis, fold_val)
#        ics(new_dots)
        print_sample(get_vis_map(new_dots))
#        axis, fold_val = folds[1]
#        new_dots = fold_once(new_dots, axis, fold_val)
#        ics(new_dots)

#        ics(simple_nodes(paths[0]))
        result = len(new_dots)
        print_result(result)


    def part2():
        new_dots = dots_list

        for axis, fold_val in folds:
            new_dots = fold_once(new_dots, axis, fold_val)
#            ics(new_dots)

#        ic(get_vis_map(new_dots))

        if not is_sample:
            xs, ys = xs_and_ys(new_dots)
            s = get_vis_map_multiline_str(xs, ys, show_axis=False)
            print(s)
            print_result(ocr_aoc_letters(s))


    part1()
    part2()

def main():
    print("Sample:")
    run(samp_inp, False)

    print("Actual:")
    real_inp = get_aocd_data()
    run(real_inp, True)




samp_inp = r"""
6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5
"""



main()

