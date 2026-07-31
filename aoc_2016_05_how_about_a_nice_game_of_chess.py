from functools import *
from collections import *
from itertools import *
from math import *
from statistics import *
from builtins import pow
import hashlib

from colorama import Fore, Style
from functional import seq # https://github.com/EntilZha/PyFunctional
import iteration_utilities as it_ut # https://pypi.org/project/iteration-utilities/
from icecream import ic

from timer_utils import timefunction
from aoc_utils import * # this includes adding c:\ut to sys.path
from Utilities import *
import seq_extensions # these extend PyFunctional seq objects, don't need to directly use anything in it
from quicklambda import _1, _2


@timefunction
def run(inp1, inp2, is_real):
    insert_sample_functions(is_real, globals())

    def data_parse(inp):
        return inp.strip()

    def find_index(index, parsed, positions=5):
        leading_zeros = "0" * positions
#        ics(parsed)
#        ics(leading_zeros)

        for n in count(index):
            bytes = (parsed + str(n)).encode()
            digest = hashlib.md5(bytes).hexdigest()

            if not n % 100000:
                ics(n, bytes, digest)

#            ics(len(digest), digest)

            if digest.startswith(leading_zeros):
                return n, digest

    def process1(parsed, positions=5):
        index = -1
        pw = []

        for step in range(8):
            index, digest = find_index(index + 1, parsed, positions)
            pw.append(digest[5])
            ic(pw)

        return sjoin(pw)

    @timefunction
    def part1(inp):
        parsed = data_parse(inp)
        ics(parsed)
        result = process1(parsed)
        print_result(result)

    def process2(parsed, positions=5):
        index = -1
        pw = [ None ] * 8

        for step in count():
            index, digest = find_index(index + 1, parsed, positions)

            i = ord(digest[5]) - ord("0")

            if 0 <= i <= 7 and pw[i] is None:
                pw[i] = digest[6]
                ic(step, i, pw)

                if all(c is not None for c in pw):
                    break

        return sjoin(pw)


    @timefunction
    def part2(inp):
        parsed = data_parse(inp)
        result = process2(parsed)
        print_result(result)

    part1(inp1)

    # time-consuming, and sample isn't any faster
    if is_real:
        part2(inp2)

def main():
    example = get_aocd_example()
    samp_inps = split_example(example)

    for n, samp_inp in enumerate(samp_inps, 1):
        print(f"{Fore.BLUE}{Style.BRIGHT}Sample {n}:{Style.RESET_ALL}")
        run(samp_inp, samp_inp, False)

    if 1:
        print(f"{Fore.BLUE}{Style.BRIGHT}Actual:{Style.RESET_ALL}")
        # needs env var AOC_SESSION
        real_inp = get_aocd_data()
        run(real_inp, real_inp, True)
#        aocd.submit(my_answer)



main()

