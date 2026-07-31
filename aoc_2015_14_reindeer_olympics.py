from functools import *
from collections import *
#from sympy import *
from itertools import *
from math import *
from statistics import *
from builtins import pow
from timer_utils import timefunction

from colorama import Fore, Style
from functional import seq # https://github.com/EntilZha/PyFunctional
import iteration_utilities as it_ut # https://pypi.org/project/iteration-utilities/
import pyperclip
from icecream import ic

from aoc_utils import * # this includes adding c:\ut to sys.path
from Utilities import *
import seq_extensions # these extend PyFunctional seq objects, don't need to directly use anything in it
#from fz import _1
#from quicklambda import _1, _2
from mini_lambda import s, _, x


@timefunction
def run(inp1, inp2, is_real):
    insert_sample_functions(is_real, globals())

    def data_parse(inp):
        lines = inp.strip().split('\n')
#        ics(lines)
        data = seq(lines).map(compose(str.split, partial(it_ut.getitem, idx=(0,3,6,13)))).multimap(identity, int, int, int).to_list()
#        ics(data)
        return data


    def process1(parsed, end_time):
        ic(end_time)
        distances = []

        for name, speed, on, off in parsed:
            interval = on + off
            full, rem = divmod(end_time, interval)
            flying_rem = min(on, rem)
            distance = full * speed * on + flying_rem * speed
            ics(name, speed, on, off, interval, full, rem, flying_rem, distance)
            distances.append(distance)

        ics(distances)
        return max(distances)



    @timefunction
    def part1(inp):
        parsed = data_parse(inp)
        ics(parsed)
        result = process1(parsed, 2503 if is_real else 1000)
        print_result(result)

    process2 = process1

    def process2(parsed, end_time):
        ic(end_time)
        distances = []
        runners = []
        traveled = [0] * len(parsed)
        points = [0] * len(parsed)

        for name, speed, on, off in parsed:
            runners.append(cycle(chain(repeat(speed, on), repeat(0, off))))

            # each entry from runners is the distance traveled this second  by each reindeer
        for i, distances in zip(range(end_time), zip(*runners)):
            traveled = add_tuple(traveled, distances)
            winner_val = max(traveled)

            for n, val in enumerate(traveled):
                if val == winner_val:
                    points[n] += 1

#            winner = it_ut.argmax(traveled)
#
#            if winner is not None:
#                points[winner] += 1
#            else:
#                print(f"No winner at {i}!")



        ics(traveled)
        ics(points)
        return max(points)


    @timefunction
    def part2(inp):
        parsed = data_parse(inp)
        result = process2(parsed, 2503 if is_real else 1000)
        # 1064 is too low
        print_result(result)

    part1(inp1)
    part2(inp2)

def main():
    if 1:
        if samp_inps and samp_inps[0]:
            for n, samp_inp in enumerate(samp_inps, 1):
                print_preface(False, n)
                run(samp_inp, samp_inp, False)
        else:
            print_preface(False)
            run(samp_inp1, samp_inp2, False)

    if 1:
        print_preface(True)
        real_inp = get_aocd_data()
        run(real_inp, real_inp, True)
#        aocd.submit(my_answer)




samp_inp1 = r"""
Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.
Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds.
"""

samp_inp2 = samp_inp1
#samp_inp2 = r"""
#"""


samp_inps = \
"""
""".strip().split("\n")


main()


