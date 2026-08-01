from functools import *
from collections import *
from itertools import *
from math import *
from statistics import *
import re
from builtins import pow
from utils.timer_utils import timefunction

from functional import seq # https://github.com/EntilZha/PyFunctional
import iteration_utilities as it_ut # https://pypi.org/project/iteration-utilities/
from icecream import ic

from utils.aoc_utils import * # this includes adding c:\ut to sys.path
from utils.utilities import *
import utils.seq_extensions # these extend PyFunctional seq objects, don't need to directly use anything in it
from utils.quicklambda import _1

required_fields = "ecl pid eyr hcl byr iyr hgt".split()
required_keys = set(required_fields)
Passport = namedtuple('Passport', required_fields)

re_hair = re.compile(r"#[0-9a-f]{6}")

@timefunction
def run(inp, is_real):
    ics = nothing if is_real else ic
    print_result = partial(print_result_aoc, is_real)

    inp = inp.strip().split('\n')
#    inp = inp.strip("\n").split('\n')
#    ic(len(inp))
#    ics(inp)

    passport_entries = seq(inp).split()
#    ics(passport_entries)
    ic(passport_entries.len())
    split_by_colon = partial(str.split, ":")
    passport_dicts = passport_entries.map(lambda pe: dict(kv.split(":") for kv in " ".join(pe).split()))
#    passport_dicts = passport_entries.map(" ".join).map(str.split).map(partial(map, colon_splitter)).to_dict()

#    ics(passport_dicts)

    def validate(passport_dicts, validator):
        return seq(passport_dicts).count(validator)


    @timefunction
    def part1():
        def validator(pd):
            return len(required_keys - pd.keys()) == 0

        result = validate(passport_dicts, validator)
        print_result(result)


    def valid_num(num, length):
        return len(num) == length and num.isdigit()

    def valid_range(num, length, min, max):
        if not valid_num(num, length):
            return False

        num = int(num)
        return num >= min and num <= max

    def valid_year(yr, min, max):
        return valid_range(yr, 4, min, max)


    def valid_height(h):
        num_part = h[:-2]

        if h.endswith("cm"):
            return valid_range(num_part, 3, 150, 193)

        if h.endswith("in"):
            return valid_range(num_part, 2, 59, 76)

        return False

    valid_eyes = set("amb blu brn gry grn hzl oth".split())


    @timefunction
    def part2():
        def validator(pd):
            if required_keys - pd.keys():
                return False

            pd.pop("cid", None)
            pp = Passport(**pd)
#            ics(pp)

            return (
                valid_year(pp.byr, 1920, 2002) and
                valid_year(pp.iyr, 2010, 2020) and
                valid_year(pp.eyr, 2020, 2030) and
                valid_num(pp.pid, 9) and
                pp.ecl in valid_eyes and
                re_hair.fullmatch(pp.hcl) and
                valid_height(pp.hgt)
                )


        result = validate(passport_dicts, validator)
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
        # needs env var AOC_SESSION
        real_inp = get_aocd_data()
        run(real_inp, True)
#        aocd.submit(my_answer)


main()

