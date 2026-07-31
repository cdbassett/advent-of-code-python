from functools import *
from collections import *
from itertools import *
from math import *
from statistics import *
from builtins import pow

from colorama import Fore, Style
from functional import seq # https://github.com/EntilZha/PyFunctional
import iteration_utilities as it_ut # https://pypi.org/project/iteration-utilities/
import pyperclip
from icecream import ic

from timer_utils import timefunction
from aoc_utils import * # this includes adding c:\ut to sys.path
from Utilities import *
import seq_extensions # these extend PyFunctional seq objects, don't need to directly use anything in it
#from fz import _1
from quicklambda import _1, _2
#from mini_lambda import s, _, x


@timefunction
def run(inp1, inp2, is_real):
    insert_sample_functions(is_real, globals())

    def data_parse(inp):
        lines = inp.strip().split('\n')
        parsed = map_list(partial(str.split, sep=")"), lines)
        ic(len(parsed))
        return parsed



    def process1(parsed):
        orbits = defaultdict(list)

        for a, b in parsed:
            orbits[a].append(b)

        def count_orbits(key, level=1):
            sub_orbits = orbits[key]
            count = len(sub_orbits) * level

            for orbiter in sub_orbits:
                count += count_orbits(orbiter, level + 1)

            ics(key, count)
            return count

        return count_orbits("COM")

    @timefunction
    def part1(inp):
        parsed = data_parse(inp)
        ics(parsed)
        result = process1(parsed)
        print_result(result)

    process2 = process1

    def p_rep(path):
        return ".".join(path)

    def process2(parsed):
        parents = dict((b, a) for a, b in parsed)
#        ics(parents)

        def get_path(child):
            key = child
            path = []

            while (key := parents.get(key)) is not None:
                path.append(key)

            return list(reversed(path))

        san_path = get_path("SAN")
        you_path = get_path("YOU")
        ic(p_rep(san_path), p_rep(you_path))


        for i, c in enumerate(san_path):
            if c != you_path[i]:
                unique_path_san = san_path[i:]
                unique_path_you = you_path[i:]
                break

        ic(p_rep(unique_path_san), p_rep(unique_path_you))
        return len(unique_path_san) + len(unique_path_you)


    @timefunction
    def part2(inp):
        parsed = data_parse(inp)
        result = process2(parsed)
        # 139 is too low
        print_result(result)

    part1(inp1)
    part2(inp2)

def main():
    if 1:
        if samp_inps:
            for n, samp_inp in enumerate(samp_inps, 1):
                print_preface(False, n)
                run(samp_inp, samp_inp, False)
        elif samp_inp1.strip():
            print_preface(False)
            run(samp_inp1, samp_inp2, False)

    if 1:
        print_preface(True)
            # needs env var AOC_SESSION
        real_inp = get_aocd_data()
        run(real_inp, real_inp, True)
#        aocd.submit(my_answer)




samp_inp1 = r"""
COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L"""

samp_inp2 = r"""
COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
K)YOU
I)SAN"""


samp_inps = """
""".strip().split("\n")

samp_inps = [
    ]

main()

