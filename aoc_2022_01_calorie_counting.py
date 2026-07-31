from functools import *
from collections import *
from itertools import *
from math import *
from builtins import pow
import iteration_utilities as it_ut

from aoc_utils import * # this includes adding c:\ut to sys.path
from Utilities import *
import seq_extensions # these extend PyFunctional seq objects, don't need to directly use anything in it


def main(inp, is_real):
    insert_sample_functions(is_real, globals())
    print_preface(is_real)
    inp = inp.strip().split('\n')

    def get_chunks(l):
        return list(it_ut.split(l, it_ut.complement(bool)))

    def get_chunks(l):
        return list(split_iterable(l, ""))

    chunks = get_chunks(inp)
    print_list("chunks", chunks)
    n_chunks = [list(map(int, c)) for c in chunks]
    print_list("n_chunks", n_chunks)
    n_sums = [sum(c) for c in n_chunks]
    print_list("n_sums", n_sums)

    def part1(inp, is_real):
        print_result(max(n_sums))

    def part2(inp, is_real):
        sorted_sums = sorted(n_sums, reverse = True)
        top3 = sorted_sums[:3]
        sum_top3 = sum(top3)
        print_result(sum_top3)

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

