from functools import *
from collections import *
from sympy import *
from itertools import *
from math import *
from statistics import *
from dataclasses import dataclass
from builtins import pow
import pyperclip
from icecream import ic
#import numpy as np
#import shapely
#import shapely.ops
from timer_utils import timefunction
#import matplotlib.pyplot as plt
#from construct import *

from aoc_utils import * # this includes adding c:\ut to sys.path
from Utilities import *
import seq_extensions # these extend PyFunctional seq objects, don't need to directly use anything in it

PointBase = Point2D

Point = build_arithmetic_namedtuple(PointBase)

CheckAndMove = namedtuple("CheckAndMovement", "checks,move,dir")
#CheckAndMoveBase = namedtuple("CheckAndMovement", "checks,move,dir")
#CheckAndMove = build_arithmetic_namedtuple(CheckAndMoveBase)

@dataclass
class Blizzard:
    initial: Point
    movement: Point
    limit: int

    def pos_at_minute(self, m):
        return (self.initial + self.movement * m) % self.limit



movements = [
    (0, -1), # North
    (0, 1), # South
    (-1, 0), # West
    (1, 0), # East
    ]

movements_and_still = movements + [(0,0)]

movements = [Point(*m) for m in movements]
movements_and_still = [Point(*m) for m in movements_and_still]
#    ics(movements)

north, south, west, east = movements

char_to_movement = dict(zip("^v<>", movements))

movements_c = [
    -1j, # North
    1j, # South
    -1, # West
    1, # East
    ]


def run(inp, is_real):
    ics = nothing if is_real else ic
    print_result = partial(print_result_aoc, is_real)

    inp = inp.strip().split('\n')
#    inp = inp.strip("\n").split('\n')
    stripped = [line[1:-1] for line in inp[1:-1]]
#    ic(len(inp))
    full_width = width(stripped)
    ic(full_width)
    full_height = height(stripped)
    ic(full_height)
    ics(stripped)

    minutes = 1000 if is_real else 20
    real_full_width = full_width
    real_full_height = full_height

    if 0:
        full_width = 3
        full_height = 3
        minutes = 5


    blizzards = []
    x_range = tuple(range(full_width))
    real_x_range = tuple(range(real_full_width))
    y_range = tuple(range(full_height))
    real_y_range = tuple(range(real_full_height))
    minute_range = tuple(range(minutes))
    repeats = lcm(real_full_width, real_full_height)
    ic(repeats)

    for x, y in product(real_x_range, real_y_range):
        c = stripped[y][x]
        movement = char_to_movement.get(c)

        if movement:
            blizzards.append(Blizzard(Point(x, y), movement, (real_full_width, 5000) if c in "<>" else (5000, real_full_height)))

##    ics(blizzards)
#    first_state = set(blizzard.pos_at_minute(0) for blizzard in blizzards)
#    ics(get_vis_map(first_state))
#    states = [set(blizzard.pos_at_minute(m) for blizzard in blizzards) for m in range(min(repeats, minutes+2))]
#    ics(get_vis_map(set(blizzard.initial for blizzard in blizzards)))
#    ics(get_vis_map(states[0]))
#    ics(get_vis_map(states[1]))
#    ics(get_vis_map(states[2]))
#    ics(get_vis_map(states[3]))
#    ics(get_vis_map(states[4]))
#    ics(get_vis_map(states[5]))


    def mappit(start, end, m):
        positions = set([start])
#        position = start

        while True:
            next_positions = set()
#            state = states[m % repeats]
            state = set(blizzard.pos_at_minute(m) for blizzard in blizzards)


            for position in positions:
                for new_pos in (position + adj for adj in movements_and_still):
                    if new_pos == end:
                        return m

                    x, y = new_pos

                    if x < 0 or x >= full_width or y < 0 or y >= full_height:
                        continue

                    if new_pos not in state:
                        next_positions.add(new_pos)

            positions = next_positions

            if not positions:
                positions.add(start)

            m += 1



    start = Point(0, -1)
    end = Point(full_width-1, full_height)
    first = mappit(start, end, 1)



    @timefunction
    def part1():
        result = first
        print_result(result)



    @timefunction
    def part2():
        result = mappit(start, end, mappit(end, start, first))
        print_result(result)

    part1()
    part2()

def main():
#    print(real_inp)

    if 1:
        for samp_inp in samp_inps:
            print("Sample:")
            run(samp_inp, False)

    if 1:
        print("Actual:")
        run(real_inp, True)




samp_inp = r"""
#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#
"""

short_samp = """
.....
..##.
..#..
.....
..##.
.....
"""


samp_inps = [
#    short_samp,
    samp_inp,
    ]



real_inp = r"""
#.####################################################################################################
#>.^>^v<^v>>>v<.>v><vv<<<.^^>>^v.^^v^vv<<><>v><v>v^>^<<>vvv<<>v>>.^>>^.^>..<<v<v<^.>.>^^<><><><^^.^<>#
#>vv<<v<<<<v>v<v^.<.v<<><v<<.<>>^^.>.^v>^^.^^.><v>><<^^^^<^>>.v.><v.v.<<<<<v>v<^>v^<>^v<^.<^^>^>vv>^>#
#>^.^>^^^v<>v><>v^vv>v>>v<v<<..><><<>v<>v>v^v>vv<v.<.v^vv<v>.>v<^>v>>v..v<>^v.>v.><^><<v<vvv<^>v>.^<>#
#<.v.v^<>^v<<^>v^>v^<.<>>^<><>v.<v>^^><><v>^^>^>.^.v>.<vv>^.>.vv^v^^<^>^.<>.^>^>^><.>>>>^<<v>^^><^v<>#
#<<v<^^v^><.v<v.^>^^<..^^.>v^<^^^^.<><v<^^><^>><^>^v^>.vvvvv^<^>^v<^>^<^>><<>^v<>^^^v<<^>vvv>v^^^<.<<#
#<v^v><<>^^.<v^.v><<>>v^vv<^<^^.v<.v><>><<<.v<.<<<<v>.<><^<v^<>vv^>v<v>^^><^^^v>.^^^<><>>v>v<>^v>>v^<#
#<..^vv>^vv^>v<^<>..^<^v<^><<<>>.vvv^v^>>v>^^>.<<vvv<v.>^>><vv<^^.v^v.v>>><^<<<>^v.>><v>^^>^v<v>^vv>>#
#<^^>v^v^v^>.>v<<>>>^^>vvvvv<>^.v>><>^<>>v^^^^^v<>>>^^>>>^.>><.>v>v^><.^vv^<<<<^v<><^^>vv..^^v^<<^<v>#
#>.v<v^.<v.^vvv^>>^<v^^<<^><><v>>^^>.^v<vv<>><^<.v.v<.<.^vvv^.^v^v><v<<.<>^<v>>v<^^>^vv<.vvv<<^<vv<v<#
#<<v<>>v<<^>v><v.><<.<>^^vvvv^<>.v>v^v.^^>.^^^>^>^>^^><v>.v^>v^vv><<>><^<<vvvv^v<>v^<<.^^v>.>>>><^>^<#
#<>>>>vv>^^<^<^^^^^><v^^<>vvv<><<>v^.vvv^>^v^>v<^<^v>>vvvv^vv<<>.vv<.<vv^^>>>v>>^>v><<v<><v.><v^vvv<>#
#><vv^v<vv<<v^>^.^^>>v>v.^<^v<^v>.vv.^>><><>^<^v>>v<.^.<^.>.^v<.<.>^>^.^>>>>v<^>v>^..^.v<^.><.<<.<^>>#
#<>>^<^v<.<v^v>^^>^>.v^<v>v<^<>^>>.^v><^>vv<<>v>>v>.v<>>^^v>>v<<^^v^v...^.^><^^^.^vvv>vv><<>^<<><<.^>#
#>v^<^^^v^>><.>.v<v>^.v^^.<^^v^.<v<<.>v<.^v>^^...^^^<^>^^vv>v>v>v^v<>vv>>vv^>>>><>^vv^v^<<vv^.><^v<^<#
#<><><><v><><<^^v.^v<>v^<v>>v^v<<^^.^>.<<<>.><^^vv>v<<<<>>v^^^>^<<^^<^.<>>><^^v.<>v>.<.<>>v>>v>>>>v^.#
#>^v>>>>.^<^.v>>><^<<v.<<^vv.^<.>><>v.><>vv>v<.^v.<<^<v<^.v<<^^<<^^<^<v.v>vv^v<vv.^v.<^^>^>^..vv^^>>>#
#..<.><.v<>^>>v<>.>^v.>^vv>>...<.>><<v^v<<>>vv>>v^><<^^>^^.>v.>>>v^^^<.<<v>>^<v<^^<v<v<>>^.<^v>.^^<<<#
#<.<v.><vv<v<^<v<.vv^.v>v^v<.<>v^>>^<^vv>.<^<>.^><<>>.<.<<<><<<^v<^^<><>^^<v.<v>>>>vv.>v^><>v.><^<v.>#
#>^>^>^<<<^v^<<^v>^<.^vvv<>>^>>v>>>^><v<>..>v>>>^^vvv><v^^>^v^.^<v><v.>.<<^vv>^^.<^^v>^><^<^^v<>>>.<>#
#<v^<v><.>v>vv.^>v^^.vv^><^>^^^v^<v^^vvv>><.<..v^v^>^<<^>>^>^>^.>>vv.^>>.v>>><<<>>^<<.>v.v>.<><v<>v>>#
#>^.<<>>vv^<v^v<<>>>>^><vv<^v>>>^v><>v<><v>.>v>^v>><vv><.><<<^^v<>.^<v><><v^>>><<vv.v>^vv>v<<>^<^v^v<#
#<<.vv.<v^vv><>^<^^v^<<<<^>>^><^vv>^^<^.v^>^.v<^^<v<<.<v<^^.<^v^.<^.v>v<v><.>^vv.vv^vv^<<<>.>v^v.v.><#
#<>>>>>v>v.v^>><>v^<^<<<^<vv>>v<<<><v<>.^^<^vvv^.>>><v<<.^v<v<v.^v.v<>v<v<v>v^>>>v>^v<<>>.<>vvv^>>>v<#
#<^.<<^<v>v<^^v<^<<>v.<<^^<.<>><<><>v<><.<<<^>v.^>v<<>.^><vv^>>>vvvv^<^v^>v<^v<>.<vv>^v><v<v^>.v<<v>>#
#<.<v><>^>>.>v^vv>^^<^><.>>^v^<><>v^^v<>>.v.>v>.^^vvvv<><>v^>v>v<<.^v^^<v^^v>v^^v>v><>v>vvv<^>^>^<v<>#
#<v<.<>^^^<vv.^^>v>^.>>>.<<><vvv^>vvv.<v<.v>v<.<<v<^<^^><^^^.>^<.v>><<^^.^.<^v^.<>v.v^><<<^.<.^^vvv^>#
#<v.v><.>>><.><<>>.^>.<<v>>^>.>^>v>v>>..v^^><v.><<^vv>^v^>.>>><>^.vvv^.<<>vv>><<>>vv>v<<<^<>v>><>vv<<#
#>v^^v<><>^^>v^><^^<>.^vv>vv^^^<<.^^vv^<^^^v>.v^^<^><^<<v>>^..^<<<<^vv>><v<^<>^>v>^>.>.<<<>.^^>vv^^>>#
#>.>^<^>.v^>>>vv<>>^>><<>v^.^>.>>><^^^<><>^v>^vv><vv>.>v^<^^v>vv^vv<v.<>vv.>.<^^<><v>v>^^<.<vv<<^vv^>#
#>.>>^<^.^><<v.^<^^v<^^<v<<><v^><^.>^><>v>>>^.^^>>><><^>>>><>^^.v^>><.>.^>.<^.v^<<<>>>>><.^vv<>>vv<^>#
#>v>^^<v.<>^v.<v>v^v>^^.>>>.>.<<^<<>^v>><.v>v^<>>vv^>v<.<^^v<>vv^^<v>>v>^v>^<^v<>^v^<.^>^.<>>><.^v>..#
#>.^^.<>.>v^^>>^>^^<.<<>..>>^><><<v<^><<^v^<>v><v>^>><><<v^<^<v<v.v<.>.>>>>^^^v<.v><><><v<^<vv.>>><.>#
#<>^>.v>v>v<v<v>v.>^<v^vv<vvv>^v<^>^v><>.<><vv>v<<.<v>>^^v>^<vv.><>v.^^.>.^<^v<.><^^>><<>.^^v.>v><<.<#
#>>v.v>^^.>>>.<>>^v<^>.<>^^<<><.v><v.>>>^^<>>>^>v>>^>^v>><><^.^^><^^^><v^><v><v^>^.>v>>>v<><vv<v^.>.>#
#>>>>>^<<^v^v<<^>.vv.vv^^v^<vv.>>>v^.<..^v^^v<><v>^<<^.^.v<^.<<<>vv>..^v>>><>^<v<>><^^.^^>^.^^>v>><v>#
####################################################################################################.#
"""

main()

