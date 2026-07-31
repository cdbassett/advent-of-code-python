from functools import *
from collections import *
from itertools import *
from math import *
from statistics import *
from builtins import pow
from utils.timer_utils import timefunction

from colorama import Fore, Style
from functional import seq # https://github.com/EntilZha/PyFunctional
import iteration_utilities as it_ut # https://pypi.org/project/iteration-utilities/
import pyperclip
from icecream import ic
import aocd # https://github.com/wimglenn/advent-of-code-data
# aocd.lines  # like data.splitlines()
# aocd.numbers # uses regex pattern -?\d+ to extract integers from data


from utils.aoc_utils import * # this includes adding c:\ut to sys.path
from utils.utilities import *
import utils.seq_extensions # these extend PyFunctional seq objects, don't need to directly use anything in it

@timefunction
def run(inp1, inp2, is_real):
    insert_sample_functions(is_real, globals())

    def data_parse(inp):
        lines = inp.strip().split('\n')
        return lines


    def process_report(is_valid, line):
        res = is_valid(line)
        ics(line, res)
        return res

    def process1(parsed, is_valid):
#        return seq(parsed).count(is_valid)
        return seq(parsed).count(partial(process_report, is_valid))

    vowel_set = set("aeiou")
    bad_pairs = "ab,cd,pq,xy".split(",")

    @timefunction
    def part1(inp):
        def is_valid(line):
            for part in bad_pairs:
                if part in line:
                    ics(line, "bad_pairs")
                    return False

            if len(list(c for c in line if c in vowel_set)) < 3:
                ics(line, "insufficent vowels", list(c for c in line if c in vowel_set))
                return False

            for c1, c2 in pairwise(line):
                if c1 == c2:
                    return True


            ics(line, "no doubles")
            return False

        parsed = data_parse(inp)
        result = process1(parsed, is_valid)
        print_result(result)

    process2 = process1

    @timefunction
    def part2(inp):
        def is_valid(line):
            pair_counts = Counter(pairwise(line))

            for pair, cnt in pair_counts.items():
                if cnt > 1:
                    pair = sjoin(pair)
                    index = line.index(pair)
                    rindex = line.rindex(pair)

                    if rindex > index+1:
                        break
            else:
                ics(line, "no double pairs with something in between")
                return False

            for c1, c2, c3 in seq(list(line)).sliding(3):
                if c1 == c3:
                    return True


            ics(line, "no doubles with something in between")
            return False

        parsed = data_parse(inp)
        result = process1(parsed, is_valid)
        print_result(result)

    part1(inp1)
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

