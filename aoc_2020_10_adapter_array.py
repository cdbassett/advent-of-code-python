from functools import *
from collections import *
from itertools import *
from math import *
from statistics import *
from builtins import pow
import operator
from timer_utils import timefunction


from functional import seq # https://github.com/EntilZha/PyFunctional
import iteration_utilities as it_ut # https://pypi.org/project/iteration-utilities/
import pyperclip
from icecream import ic
import aocd # https://github.com/wimglenn/advent-of-code-data
# aocd.lines  # like data.splitlines()
# aocd.numbers # uses regex pattern -?\d+ to extract integers from data


from aoc_utils import * # this includes adding c:\ut to sys.path
from Utilities import *
import seq_extensions # these extend PyFunctional seq objects, don't need to directly use anything in it
from quicklambda import _1



@timefunction
def run(inp, is_real):
    ics = nothing if is_real else ic
    print_result = partial(print_result_aoc, is_real)

    lines = inp.strip().split('\n')
#    lines = inp.strip("\n").split('\n')
    ic(len(lines))
#    ics(inp)
    numbers = seq(lines).map(int).sorted()
    device_rating = numbers.max() + 3
    joltages = seq(numbers).pad(0, nlead=1).pad(device_rating, ntail=1)
    ics(joltages)


    @timefunction
    def part1():
        differences = joltages.reverse().sliding(2).starmap(operator.sub)
        ics(differences)
        c = Counter(differences)
        result = c[1] * c[3]
        print_result(result)


    next_adapters = {}

    @cache
    def count_paths(start):
        cnt = 0
        neighbors = next_adapters.get(start)

        if neighbors is None:
            return 1

        for next_a in next_adapters[start]:
            cnt += count_paths(next_a)

        return cnt


    invalid = 5000

    @timefunction
    def part2():
        for a, *next_as in joltages.pad(invalid, ntail=2).sliding(4): # invalid entries at end are to make sure we get last connections
            next_adapters[a] = seq(next_as).filter(_1 <= a + 3).to_tuple()

#        ics(next_adapters)
        result = count_paths(0)
        print_result(result)

    part1()
    part2()

def main():
    if 1:
        for samp_inp in samp_inps:
            print("Sample:")
            run(samp_inp, False)

    if 1:
        print("Actual:")
        real_inp = get_aocd_data() # supposed to work if filename is clear enough (year would need to be 4-digit), needs env var AOC_SESSION
        run(real_inp, True)
#        aocd.submit(my_answer)




samp_inp = r"""
28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3
"""


short_samp = """
"""


samp_inps = [
#    short_samp,
    samp_inp,
    ]


main()

