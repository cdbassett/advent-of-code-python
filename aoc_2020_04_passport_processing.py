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
from quicklambda import _1

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
#    print(real_inp)

    if 1:
        for samp_inp in samp_inps:
            print("Sample:")
            run(samp_inp, False)

    if 1:
        print("Actual:")
        real_inp = get_aocd_data()
        run(real_inp, True)
#        aocd.submit(my_answer)




samp_inp = r"""
ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in
"""

# for part 2
samp_inp = r"""
eyr:1972 cid:100
hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926

iyr:2019
hcl:#602927 eyr:1967 hgt:170cm
ecl:grn pid:012533040 byr:1946

hcl:dab227 iyr:2012
ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277

hgt:59cm ecl:zzz
eyr:2038 hcl:74454a iyr:2023
pid:3556412378 byr:2007

pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
hcl:#623a2f

eyr:2029 ecl:blu cid:129 byr:1989
iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm

hcl:#888785
hgt:164cm byr:2001 iyr:2015 cid:88
pid:545766238 ecl:hzl
eyr:2022

iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719

"""

short_samp = """
"""


samp_inps = [
#    short_samp,
    samp_inp,
    ]


main()

