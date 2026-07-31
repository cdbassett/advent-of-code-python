from functools import *
from collections import *
#from sympy import *
from itertools import *
from math import *
from statistics import *
import re
from builtins import pow
from timer_utils import timefunction

from functional import seq # https://github.com/EntilZha/PyFunctional
import iteration_utilities as it_ut # https://pypi.org/project/iteration-utilities/
from icecream import ic

from aoc_utils import * # this includes adding c:\ut to sys.path
from Utilities import *
import seq_extensions # these extend PyFunctional seq objects, don't need to directly use anything in it
#from fz import _1
from quicklambda import _1

required_fields = "ecl pid eyr hcl byr iyr hgt".split()
required_keys = set(required_fields)
Passport = namedtuple('Passport', required_fields)

re_hair = re.compile(r"#[0-9a-f]{6}")

@timefunction
def run(inp, is_real):
    ics = nothing if is_real else ic
    print_result = partial(print_result_aoc, is_real)

    lines = inp.strip().split('\n')
#    lines = inp.strip("\n").split('\n')
    ic(len(lines))
#    ics(inp)


    def calc_id(line):
        if 0:
            row_part, col_part = head_tail(line, 7)
            row = int(row_part.replace("F", "0").replace("B", "1"), base=2)
            col = int(col_part.replace("L", "0").replace("R", "1"), base=2)
            ics(row, col)
            return row * 8 + col

        return int(line.replace("F", "0").replace("B", "1").replace("L", "0").replace("R", "1"), base=2)


    if not is_real:
        for line in lines:
            ic(calc_id(line))



    @timefunction
    def part1():
        result = seq(lines).map(calc_id).max()
        print_result(result)

    @timefunction
    def part2():
#        existing = seq(lines).map(calc_id).to_set()
        mask = 0b1000001000
        all = 0b1111111111
#        front_or_rear = _1 >= 0b1111111000 or _1 <= 0b0000000111
        is_front = _1 >= 0b1111111000
        is_rear = _1 <= 0b0000000111
#        ic(front_or_rear)
#        existing = seq(lines).map(calc_id).filter_not(_1 & mask).to_set()
#        possible = seq.range(0b1111111111).filter_not(_1 & mask).to_set()
        existing = seq(lines).map(calc_id).filter_not(is_front).filter_not(is_rear).to_set()
        possible = seq.range(0b1111111111).filter_not(is_front).filter_not(is_rear).to_set()
        ics(existing)
        ic(len(possible))
        ic(len(existing))
#        ic(possible - existing)
        ic(len(possible - existing))
        cnt = 0

        for prev, cur, next in seq(sorted(possible)).sliding(3):
            if prev in existing and next in existing and cur not in existing:
                result = cur
                cnt +=1
#                break
        ic(cnt)

        print_result(result)

    part1()
    part2()

def main():
#    print(real_inp)

    if 0:
        for samp_inp in samp_inps:
            print("Sample:")
            run(samp_inp, False)

    if 1:
        print("Actual:")
        real_inp = get_aocd_data()
        run(real_inp, True)
#        aocd.submit(my_answer)




samp_inp = r"""
FBFBBFFRLR
BFFFBBFRRR
FFFBBBFRRR
BBFFBBFRLL
"""


short_samp = """
"""


samp_inps = [
#    short_samp,
    samp_inp,
    ]


main()

