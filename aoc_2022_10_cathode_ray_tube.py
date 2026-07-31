from functools import *
from collections import *
from itertools import *
from math import *
from builtins import pow
from icecream import ic

from aoc_utils import * # this includes adding c:\ut to sys.path
from Utilities import *
import seq_extensions # these extend PyFunctional seq objects, don't need to directly use anything in it


def run(inp, is_real):
    insert_sample_functions(is_real, globals())
    print_preface(is_real)

    inp = inp.strip('\n').split('\n')
#    values = [((l := line.split())[0], int(l[1])) for line in inp]
#    ics(values)
#    cycle_values = [ 0 ] # values are at end of cycle, first is zero and we won't count
    cycle_values = [] # values are at end of cycle
    x = 1

    for line in inp:
        cycle_values.append(x)

        if line.startswith("a"):
            cycle_values.append(x)
            val = int(line.split()[1])
            x += val

#    ics(cycle_values)
    ics(cycle_values[19::40])
#    ics(list(it_ut.getitem(cycle_values, list(x -1 for x in (20,60,100,140,180,220)))))



    def part1():
        look_at_values = list(enumerate(cycle_values, 1))[19::40]
        ics(look_at_values)
        strengths = list(n * v for n, v in look_at_values)
        ics(strengths)

        result = sum(strengths)
        print_result(result)


    def part2():
        ics(len(cycle_values))
        screen = ["#" if abs(x-(n % 40)) <= 1 else "." for n, x in enumerate(cycle_values)]
        screen = list("".join(chunk) for chunk in n_chunks(screen, 6))
        ic(screen)

        if not is_sample:
            print_result(ocr_aoc_letters(njoin(screen)))


    part1()
    part2()

def main():
    run(samp_inp, False)

    real_inp = get_aocd_data()
    run(real_inp, True)




samp_inp = r"""
noop
addx 3
addx -5
"""

samp_inp = r"""
addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop
"""

main()


