from functools import *
from collections import *
from itertools import *
from math import *
from statistics import *
from builtins import pow
import pyperclip
from icecream import ic
from utils.timer_utils import timefunction
import matplotlib.pyplot as plt

from utils.aoc_utils import * # this includes adding c:\ut to sys.path
from utils.utilities import *
import utils.seq_extensions # these extend PyFunctional seq objects, don't need to directly use anything in it

Point = Point2D

def a_to_z(a1, a2):
    if a1 >= a2:
        return a2, a1

    return a1, a2

def run(inp, is_real):
    ics = nothing if is_real else ic
    print_result = partial(print_result_aoc, is_real)

    inp = inp.strip().split('\n')

    paths = [[Point(*map(int, pair.split(","))) for pair in line.split(" -> ")] for line in inp]
    ics(paths)
    rocks = set()
    sand = set()

        # build rock path map
    for path in paths:
        for p1, p2 in pairwise(path):
            ics(p1, p2)
            assert p1.x == p2.x or p1.y == p2.y

            if p1.x == p2.x:
                x = p1.x
                y1, y2 = a_to_z(p1.y, p2.y)
                rocks.update(Point(x, y) for y in range(y1, y2+1))
            else:
                y = p1.y
                x1, x2 = a_to_z(p1.x, p2.x)
                rocks.update(Point(x, y) for x in range(x1, x2+1))

    ics(rocks)
    max_rock_y = max(p.y for p in rocks)

    def part1():
        ics(get_vis_map(rocks))
        going = True

            # simulate sand falling from 500, 0
        while going: # all grains
            s = Point(500, 0)

            while True: # one grain
                if s.y > max_rock_y: # falling forever
                    going = False
                    break


                next = Point(s.x, s.y+1)

                if next not in rocks and next not in sand:
                    s = next
                    continue

                next = Point(s.x-1, s.y+1)

                if next not in rocks and next not in sand:
                    s = next
                    continue

                next = Point(s.x+1, s.y+1)

                if next not in rocks and next not in sand:
                    s = next
                    continue

                sand.add(s)
                break

        ics(get_vis_map(sand))
        result = len(sand)
        print_result(result)

    def part2():
        rock_line_y = max_rock_y + 2
        diff = rock_line_y + 2
        ics(rock_line_y, diff)
#        ics(get_vis_map(rocks))
        rocks.update(Point(x, rock_line_y) for x in range(500-diff, 500+diff+1))
        ics(get_vis_map(rocks))
        going = True
        start = Point(500, 0)

            # simulate sand falling from 500, 0
        while going: # all grains
            s = start

            if start in sand:
                break

            while True: # one grain
#                if s.y > max_rock_y:
#                    going = False
#                    break

                next = Point(s.x, s.y+1)

                if next not in rocks and next not in sand:
                    s = next
                    continue

                next = Point(s.x-1, s.y+1)

                if next not in rocks and next not in sand:
                    s = next
                    continue

                next = Point(s.x+1, s.y+1)

                if next not in rocks and next not in sand:
                    s = next
                    continue

                sand.add(s)
                break

        ics(get_vis_map(sand))
        result = len(sand)
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
