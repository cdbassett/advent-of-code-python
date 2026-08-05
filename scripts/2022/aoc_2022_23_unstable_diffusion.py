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


# https://adventofcode.com/2022/day/23


CheckAndMove = namedtuple("CheckAndMovement", "checks,move,dir")

# was using arithtuple, but part 2 took 4 times as long as using add_tuple2

def run(inp, is_real):
    insert_sample_functions(is_real, globals())
    print_preface(is_real)
    inp = inp.strip().split('\n')
    ic(len(inp))
    full_width = width(inp)
    ic(full_width)
    full_height = height(inp)
    ic(full_height)
    elves = set()

    for x, y in product(range(full_width), range(full_height)):
        if inp[y][x] == "#":
            elves.add((x, y))

    ic(len(elves))
    ics(get_vis_map(tuples_to_points(elves)))
    intial_directions = "NSWE"

    movements = [
        (0, -1), # North
        (0, 1), # South
        (-1, 0), # West
        (1, 0), # East
        ]

    north, south, west, east = movements
    all_movements = set(add_tuple2(a, b) for a, b in pairwise((north, west, south, east, north))).union(movements)

    def build_check_and_move(d, m):
        if m[1]:
            checks = [m, add_tuple2(m, east), add_tuple2(m, west)]
        else:
            checks = [m, add_tuple2(m, south), add_tuple2(m, north)]

        return CheckAndMove([tuple(check) for check in checks], m, d)

    checks_moves = deque(build_check_and_move(d, m) for d, m in zip(intial_directions, movements))

    def dist(t):
        return sqrt(t[0]**2 + t[1]**2)

    def process(proc_elves, checks_moves):
        all_proposals = Counter()
        proposals_by_elf = dict()
        elves_to_propose = set(proc_elves)
        dbg = round == 2

            # first half of round
        for check_and_move in checks_moves:
            if dbg:
                ics(check_and_move)

            for elf in list(elves_to_propose):
                if not any(add_tuple2(elf, movement) in proc_elves for movement in all_movements):
                    continue

                checks = [add_tuple2(elf, check) for check in check_and_move.checks]

                if dbg:
                    ics(elf, checks)

                if not proc_elves.intersection(checks):
                    move = add_tuple2(elf, check_and_move.move)
                    # move = elf + check_and_move.move
                    elves_to_propose.remove(elf)
                    all_proposals[move] += 1
                    proposals_by_elf[elf] = move

        if dbg:
            ics(all_proposals)
            ics(elves_to_propose)
            ics(proposals_by_elf)

            # iterate over a copy, we modify original
        for elf in list(proc_elves):
            proposed_move = proposals_by_elf.get(elf)

            if proposed_move:
                if all_proposals[proposed_move] == 1:
                    assert dist(subtract_tuple2(elf, proposed_move)) <= 1, ic.format(elf, proposed_move)
                    proc_elves.remove(elf)
                    proc_elves.add(proposed_move)

            # rearrange so next order is different
        checks_moves.rotate(-1)


    @timefunction
    def part1():
        last_config = None
        work_elves = set(elves)
        work_checks_moves = checks_moves.copy()

        for round in range(1, 11):
            process(work_elves, work_checks_moves)

            if work_elves == last_config:
                break

            last_config = set(work_elves)

        ics(round, get_vis_map(tuples_to_points(work_elves)))
        min_x = min(p[0] for p in work_elves)
        max_x = max(p[0] for p in work_elves)
        max_y = max(p[1] for p in work_elves)
        min_y = min(p[0] for p in work_elves)
        width = max_x - min_x + 1
        height = max_y - min_y + 1
        result = width * height - len(work_elves)
        print_result(result)


    @timefunction
    def part2():
        last_config = None
        work_elves = set(elves)
        work_checks_moves = checks_moves.copy()

        for round in count(1):
            process(work_elves, work_checks_moves)

            if work_elves == last_config:
                break

            last_config = set(work_elves)

        ics(round, get_vis_map(tuples_to_points(work_elves)))
        result = round
        print_result(result)

    part1() # sample is 110
    part2() # sample is 20


def main():
    example = get_aocd_example()
    samp_inps = split_example(example)
    ic(samp_inps)

    if 1:
        for n, samp_inp in enumerate(samp_inps, 1):
            print(f"{Fore.BLUE}{Style.BRIGHT}Sample {n}:{Style.RESET_ALL}")
            run(samp_inp, False)

    if 2:
        print(f"{Fore.BLUE}{Style.BRIGHT}Actual:{Style.RESET_ALL}")
        real_inp = get_aocd_data()
        run(real_inp, True)


main()
