from functools import *
from collections import *
from sympy import *
from itertools import *
from math import *
from statistics import *
from builtins import pow
import pyperclip
from icecream import ic
from utils.timer_utils import timefunction
from functional import seq

from utils.aoc_utils import * # this includes adding c:\ut to sys.path
from utils.utilities import *
import utils.seq_extensions # these extend PyFunctional seq objects, don't need to directly use anything in it


# https://adventofcode.com/2021/day/22


#@counted
def intersects(a, b):
#    ic(a, b)
#    ic(list(zip(a[1], b[1])))
#    ic(list(f"ar: {ar}, br: {br}" for ar, br in zip(a[1], b[1])))
#    ic(list(f"lr: {lr}, ur: {ur}" for ar, br in zip(a[1], b[1]) for lr, ur in zip(ar, br)))
#    ic(list(zip(zip(a[1], b[1]))))
    new_bounds = tuple((max((ar[0], br[0])), min((ar[1], br[1]))) for ar, br in zip(a[1], b[1]))
#    new_bounds = tuple((max((ar[0], br[0])), min((ar[1], br[1]))) for ar, br in zip(a[1], b[1]))
#    new_bounds = tuple((max(lr), min(ur)) for ar, br in zip(a[1], b[1]) for lr, ur in zip(ar, br))
#    new_bounds = tuple((max(lr), min(ur)) for lr, ur in zip(a[1], b[1]))
    return (-b[0], new_bounds) if all(r[0] <= r[1] for r in new_bounds) else None

@timefunction
def get_intersections(data):
    final_cubes = []

    for cuboid in data:
        new_cubes = [] # all entries will have first element 1 or -1

        if cuboid[0]:
            new_cubes.append(cuboid)

        for final_cube in final_cubes:
            intersection = intersects(cuboid, final_cube)

            if intersection:
                new_cubes.append(intersection)

        final_cubes.extend(new_cubes)

    return final_cubes

def cube_side_width(side):
    return side[1]-side[0]+1

def cube_volume(cuboid):
    return cuboid[0] * products(map(cube_side_width, cuboid[1]))
#    ic(cuboid)
#    return cuboid[0] * products(cube_side_width(s) for s in cuboid[1])

@timefunction
def calc_cubes(cuboids):
#    return seq(cuboids).map(cube_volume).sum()
    return sum(cuboid[0] * products(map(cube_side_width, cuboid[1])) for cuboid in cuboids)

def run(inp, is_real):
    ics = nothing if is_real else ic
    print_result = partial(print_result_aoc, is_real)

#    inp = inp.strip().split('\n')
    inp = inp.strip("\n").split('\n')

    # each data line is (on, ((x1, x2),(y1,y2),(z1,z2)))
    data = [(int(line.startswith("on")),  tuple(chunks_of_n(get_integers_from_string(line), 2))) for line in inp]
#    ics(data)





    @timefunction
    def part1():
        use_data = [d for d in data if abs(d[1][0][0]) <= 50]
#        ics(use_data)
        working_cuboids = get_intersections(use_data)
#        ic(intersects.call_count)
#        ics(working_cuboids)
        ic(len(working_cuboids))
        result = calc_cubes(working_cuboids)
        print_result(result)


    @timefunction
    def part2():
        use_data = data
#        ics(use_data)
        working_cuboids = get_intersections(use_data)
#        ic(intersects.call_count)
#        ics(working_cuboids)
        ic(len(working_cuboids))
        result = calc_cubes(working_cuboids)
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
