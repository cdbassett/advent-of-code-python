from functools import *
from collections import *
from itertools import *
from math import *
from builtins import pow
import pyperclip
from icecream import ic
import numpy as np

from utils.aoc_utils import * # this includes adding c:\ut to sys.path
from utils.utilities import *
import utils.seq_extensions # these extend PyFunctional seq objects, don't need to directly use anything in it


Point = Point2D


def run(inp, is_real):
    ics = nothing if is_real else ic
    print_result = partial(print_result_aoc, is_real)

    inp = inp.strip('\n').split('\n')
    values = [((l := line.split())[0], int(l[1])) for line in inp]
    ics(values)

    adjust = {
        "U": np.array((0, 1)),
        "D": np.array((0, -1)),
        "R": np.array((1, 0)),
        "L": np.array((-1, 0)),
        }


    def get_adjust(h, t):
        if h > t:
            return h - 1
        else:
            return h + 1

    def get_dim(dims):
        dims = list(dims)
#        assert(dots)
        negative_x = min(0, min(dims))
        positive_x = max(15, max(dims) + 1)
        return -negative_x, positive_x - negative_x

    def get_vis_map(dots, reversed):
        assert(dots)
        negative_x, width = get_dim(p.x for p in dots)
        negative_y, height = get_dim(p.y for p in dots)
        ics(negative_x, negative_y)
        vis_map = [["."] * width for r in range(height)]

        for p in dots:
            try:
                if reversed:
                    vis_map[height - (p.y + negative_y) - 1][p.x + negative_x] = "#"
                else:
                    vis_map[p.y + negative_y][p.x + negative_x] = "#"
            except IndexError:
                ic(p.y, p.x)
                raise

        vis_map = ["".join(e) for e in vis_map]
#        vis_map = "\n".join("".join(e) for e in vis_map)
        return vis_map

    def part1():
        h_point = np.array((0, 0))
        t_point = np.array((0, 0))
        t_positions = { Point(0,0) }
        h_positions = { Point(0,0) }

        def t_follow(adj):
            h_x, h_y = h_point
            t_x, t_y = t_point

            if abs(h_x - t_x) <= 1 and abs(h_y - t_y) <= 1:
                return

            if h_x == t_x:
                t_point[1] = get_adjust(h_y, t_y)
            elif h_y == t_y:
                t_point[0] = get_adjust(h_x, t_x)
            else:
                if adj[0]: # h moved on x axis
                    t_point[0] = h_x - adj[0]
                    t_point[1] = h_y
                else:
                    t_point[1] = h_y - adj[1]
                    t_point[0] = h_x

            t_positions.add(Point(*t_point))


        for direction, count in values:
            adj = adjust[direction]

            for n in range(count):
                h_point += adj
                ics(direction, n, h_point)
                h_positions.add(Point(*h_point))
                t_follow(adj)
                ics(direction, n, t_point)

#        ics(h_positions)
#        ics(t_positions)
        ics(get_vis_map(h_positions, True))
        ics(get_vis_map(t_positions, True))

        result = len(t_positions)
        print_result(result)


        # keep sign but change magniotude to 1
    def normalized_direction(h, t):
        return (h - t) / abs(h - t)

    def part2():
        num_knots = 10
        knot_points = np.array([(0, 0) for _ in range(num_knots)])
        t_positions = { Point(0,0) }
        h_positions = { Point(0,0) }

        def t_follow(knot_index):
            h_x, h_y = knot_points[knot_index-1]
            t_point = knot_points[knot_index]
            t_x, t_y = t_point
#            if knot_index == 9:
#                ics(h_x, h_x)
#                ics(h_y, t_y)

            if abs(h_x - t_x) <= 1 and abs(h_y - t_y) <= 1:
                return

            if h_x == t_x:
                t_point[1] = get_adjust(h_y, t_y)
            elif h_y == t_y:
                t_point[0] = get_adjust(h_x, t_x)
            else:   # diagonal
                x_adj = normalized_direction(h_x, t_x)
                y_adj = normalized_direction(h_y, t_y)

                if knot_index == 9:
                    ics(h_x, h_x, x_adj)
                    ics(h_y, t_y, y_adj)
                t_point[0] = t_x + x_adj
                t_point[1] = t_y + y_adj

        follow_range = list(range(1, num_knots))
        ics(follow_range)

        for direction, count in values:
            adj = adjust[direction]

            for n in range(count):
                knot_points[0] += adj
#                ics(direction, n, knot_points[0])
                h_positions.add(Point(*knot_points[0]))

                for knot_index in follow_range:
                    t_follow(knot_index)

#                ics(direction, n, knot_points[1])
                t_positions.add(Point(*knot_points[-1]))
#                t_positions.add(Point(*knot_points[1]))

#        ics(h_positions)
#        ics(t_positions)
        ics(get_vis_map(h_positions, True))
        ics(get_vis_map(t_positions, True))

        result = len(t_positions)
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
