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
from mini_lambda import s, _, x


# https://adventofcode.com/2015/day/13


@timefunction
def run(inp1, inp2, is_real):
    insert_sample_functions(is_real, globals())

    def data_parse(inp):
        lines = inp.strip().split('\n')
#        ics(lines)
        data = seq(lines).map(compose(str.split, partial(it_ut.getitem, idx=(0,2,3,-1)))).multimap(identity, lambda x: 1 if x == "gain" else -1, int, rpartial(str.rstrip, ".")).starmap(lambda n1, mult, val, n2: (n1, mult*val, n2)).to_list()
        return data


    def process1(parsed, part = 0):
        happiness_lookup = defaultdict(int)

        for n1, val, n2 in parsed:
            happiness_lookup[(n1, n2)] += val
            happiness_lookup[(n2, n1)] += val

        ics(happiness_lookup)
        names = list(set(d[0] for d in parsed))

        if part:
            names.append("me")

        ic(len(names))
        ics(names)
        first_name_tuple, rest_names = head_tail(tuple(names))

            # circular, so always start with first and get permuations for the rest
        best_happiness = max(sum(happiness_lookup[name_pair] for name_pair in pairwise(first_name_tuple + other_names + first_name_tuple)) for other_names in permutations(rest_names))
        return best_happiness



    @timefunction
    def part1(inp):
        parsed = data_parse(inp)
        result = process1(parsed)
        print_result(result)

    process2 = process1


    @timefunction
    def part2(inp):
        parsed = data_parse(inp)
        result = process2(parsed, 1)
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


