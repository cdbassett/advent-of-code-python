from functools import *
from collections import *
from itertools import *
from math import *
from builtins import pow
import pyperclip
from icecream import ic
import iteration_utilities as it_ut

from utils.aoc_utils import * # this includes adding c:\ut to sys.path
from utils.utilities import *
import utils.seq_extensions # these extend PyFunctional seq objects, don't need to directly use anything in it


# https://adventofcode.com/2022/day/5


def main(inp, is_real):
    insert_sample_functions(is_real, globals())
    print_preface(is_real)
    inp = inp.strip('\n').split('\n')

    def part1(inp, is_real):
        crate_lines = list(takewhile(lambda line: "[" in line, inp))
        crate_lines = [line for line in inp if "[" in line]
#        print_list("crate_lines", crate_lines)
        crate_parts = [list(map(it_ut.second, chunks_of_n(line, 4),)) for line in crate_lines]
        print_list("crate_parts", crate_parts)
        move_lines = [line for line in inp if line.startswith("move")]
#        print_list("move_lines", move_lines)
        move_parts = [tuple(map(int, it_ut.getitem(line.split(), (1,3,5)))) for line in move_lines]
        print_list("move_parts", move_parts)
        num_stacks = len(crate_lines[-1])

        stacks = [list() for _ in crate_parts[-1]]

        for crate_part in reversed(crate_parts):
            for c, crate in enumerate(crate_part):
                if crate != " ":
                    stacks[c].append(crate)

        print_list("stacks", stacks)

        for cnt, frm, to in move_parts:
            frm -= 1
            to -= 1
            for e in range(cnt):
                stacks[to].append(stacks[frm].pop())

        print_list("stacks", stacks)
        result = "".join(stack[-1] for stack in stacks)

        print_result(result)

    def part2(inp, is_real):
        crate_lines = list(takewhile(lambda line: "[" in line, inp))
        crate_lines = [line for line in inp if "[" in line]
#        print_list("crate_lines", crate_lines)
        crate_parts = [list(map(it_ut.second, chunks_of_n(line, 4),)) for line in crate_lines]
        print_list("crate_parts", crate_parts)
        move_lines = [line for line in inp if line.startswith("move")]
##        print_list("move_lines", move_lines)
        move_parts = [tuple(map(int, it_ut.getitem(line.split(), (1,3,5)))) for line in move_lines]
        print_list("move_parts", move_parts)
        num_stacks = len(crate_lines[-1])

        stacks = [list() for _ in crate_parts[-1]]

        for crate_part in reversed(crate_parts):
            for c, crate in enumerate(crate_part):
                if crate != " ":
                    stacks[c].append(crate)

        print_list("stacks", stacks)
        tmp = list()

        for cnt, frm, to in move_parts:
            frm -= 1
            to -= 1

            for e in range(cnt):
                tmp.append(stacks[frm].pop())

            for e in range(cnt):
                stacks[to].append(tmp.pop())

        print_list("stacks", stacks)
        result = "".join(stack[-1] for stack in stacks)

        print_result(result)

    part1(inp, is_real)
    part2(inp, is_real)

def run_samples():
    example = get_aocd_example()
    samp_inps = split_example(example)
    for n, samp_inp in enumerate(samp_inps, 1):
        print(f"{Fore.BLUE}{Style.BRIGHT}Sample {n}:{Style.RESET_ALL}")
        main(samp_inp, False)

run_samples()

real_inp = get_aocd_data()
main(real_inp, True)

