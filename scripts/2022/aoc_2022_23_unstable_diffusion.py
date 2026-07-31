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

from utils.aoc_utils import * # this includes adding c:\ut to sys.path
from utils.utilities import *
import utils.seq_extensions # these extend PyFunctional seq objects, don't need to directly use anything in it


PointBase = namedtuple("Point", "x,y")

Point = build_arithmetic_namedtuple(PointBase)

CheckAndMove = namedtuple("CheckAndMovement", "checks,move,dir")
#CheckAndMoveBase = namedtuple("CheckAndMovement", "checks,move,dir")
#CheckAndMove = build_arithmetic_namedtuple(CheckAndMoveBase)


def run(inp, is_real):
    insert_sample_functions(is_real, globals())
    print_preface(is_real)
    inp = inp.strip().split('\n')
#    inp = inp.strip("\n").split('\n')
    ic(len(inp))
    full_width = width(inp)
    ic(full_width)
    full_height = height(inp)
    ic(full_height)

    elves = set()

    for x, y in product(range(full_width), range(full_height)):
        if inp[y][x] == "#":
            elves.add(Point(x, y))

    ic(len(elves))
    ics(get_vis_map(elves))
    intial_directions = "NSWE"

    movements = [
        (0, -1), # North
        (0, 1), # South
        (-1, 0), # West
        (1, 0), # East
        ]

    movements = [Point(*m) for m in movements]
#    ics(movements)

    north, south, west, east = movements

    all_movements = set(a+b for a, b in pairwise((north, west, south, east, north))).union(movements)
#    ics(all_movements)


    def build_check_and_move(d, m):
        if m.y:
            checks = [m, m + east, m + west]
        else:
            checks = [m, m + south, m + north]

#        ics(d, checks)
#        return CheckAndMove(checks, m, d)
        return CheckAndMove([tuple(check) for check in checks], m, d)


    checks_moves = deque(build_check_and_move(d, m) for d, m in zip(intial_directions, movements))
#    ics(checks_moves)

    def dist(t):
        return sqrt(t[0]**2 + t[1]**2)

    def process(elves, checks_moves):
        all_proposals = Counter()
        proposals_by_elf = dict()
        elves_to_propose = set(elves)
        dbg = round == 2

            # first half of round
        for check_and_move in checks_moves:
            if dbg:
                ics(check_and_move)

            for elf in list(elves_to_propose):
                if not any(elf + movement in elves for movement in all_movements):
                    continue

                checks = [elf + check for check in check_and_move.checks]

                if dbg:
                    ics(elf, checks)

                if not elves.intersection(checks):
                    move = elf + check_and_move.move
                    elves_to_propose.remove(elf)
                    all_proposals[move] += 1
                    proposals_by_elf[elf] = move

        if dbg:
            ics(all_proposals)
            ics(elves_to_propose)
            ics(proposals_by_elf)

            # iterate over a copy, we modify original
        for elf in list(elves):
            proposed_move = proposals_by_elf.get(elf)

            if proposed_move:
                if all_proposals[proposed_move] == 1:
                    assert dist(elf - proposed_move) <= 1, ic.format(elf, proposed_move)
                    elves.remove(elf)
                    elves.add(proposed_move)


            # rearrange so next order is different
        checks_moves.append(checks_moves.popleft())






    @timefunction
    def part1():
        last_config = None

        for round in range(1, 11):
            ics(round)
            process(elves, checks_moves)

            if elves == last_config:
                break

#            ics(round, get_vis_map(elves, min_val=0, max_val=7))
#            ics(round, get_vis_map(elves, min_val=0))
            last_config = set(elves)

        ics(round, get_vis_map(elves))

        min_x = min(p.x for p in elves)
        max_x = max(p.x for p in elves)
        max_y = max(p.y for p in elves)
        min_y = min(p.y for p in elves)
        width = max_x - min_x + 1
        height = max_y - min_y + 1
        result = width * height - len(elves)

        print_result(result)



    @timefunction
    def part2():
        last_config = None

        for round in count(1):
            ic(round)
            process(elves, checks_moves)

            if elves == last_config:
                break

            last_config = set(elves)

        ics(round, get_vis_map(elves))
        result = round
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
