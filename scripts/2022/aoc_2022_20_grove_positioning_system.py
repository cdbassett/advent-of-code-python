from functools import *
from collections import *
from itertools import *
from math import *
from statistics import *
from builtins import pow
import pyperclip
from icecream import ic
import shapely
import shapely.ops
from utils.timer_utils import timefunction
import matplotlib.pyplot as plt

from utils.aoc_utils import * # this includes adding c:\ut to sys.path
from utils.utilities import *
import utils.seq_extensions # these extend PyFunctional seq objects, don't need to directly use anything in it


# https://adventofcode.com/2022/day/20


def run(inp, is_real):
    ics = nothing if is_real else ic
    print_result = partial(print_result_aoc, is_real)

    inp = inp.strip().split('\n')

    numbers = list(map(int, inp))
    ics(numbers)
#    ic(len(set(numbers)))


    def proc_repr(process):
#        return process
        return [t[1] for t in process]
        return [t[1] for t in process] + process

    n_max = len(numbers)
    ic(n_max)

    def mix(initial, process):
        for p in initial:
#            ics(proc_repr(process))
            i = process.index(p)
            process.rotate(-i)
            t = process.popleft()
            ndx, val = t
#            ics(i, ndx, val)
            process.rotate(-val)
            process.appendleft(t)


    def get_result(process):
        ics(process)
        new_numbers = [t[1] for t in process]
        ics(new_numbers)
        ic(len(new_numbers))
        zero_index = new_numbers.index(0)
        ics([(zero_index + i) % n_max for i in range(1000,4000,1000)])
        ics([new_numbers[(zero_index + i) % n_max] for i in range(1000,4000,1000)])
        result = sum(new_numbers[(zero_index + i) % n_max] for i in range(1000,4000,1000))
        return result


    @timefunction
    def part1():
        initial = list(enumerate(numbers))
        process = deque(initial)
        mix(initial, process)
        result = get_result(process)
        print_result(result)



    @timefunction
    def part2():
        initial = list(enumerate(n * 811589153 for n in numbers))
        process = deque(initial)

        for _ in range(10):
            mix(initial, process)

        result = get_result(process)
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
