from functools import *
from collections import *
from sympy import *
from itertools import *
from math import *
from statistics import *
from builtins import pow
import pyperclip
from icecream import ic
from Utilities import *
from timer_utils import timefunction

from aoc_utils import * # this includes adding c:\ut to sys.path
from Utilities import *
import seq_extensions # these extend PyFunctional seq objects, don't need to directly use anything in it



def run(inp, is_real):
    ics = nothing if is_real else ic
    print_result = partial(print_result_aoc, is_real)

    inp = inp.strip().split('\n')
#    inp = inp.strip("\n").split('\n')

    snafu_values = dict((str(n), n) for n in range(3))
    snafu_values["-"] = -1
    snafu_values["="] = -2

    num_values = dict((v, k) for k, v in snafu_values.items())
#    num_values = dict((str(n), n) for n in range(3))
#    num_values["-"] = -1
#    num_values[] = "="


    def to_snafu(num):
        if not num:
            return "0"

        val = ""

        while num:
            num, rem = divmod(num, 5)

            if rem > 2:
                num += 1
                rem -= 5

            val = num_values[rem] + val

        return val


    def from_snafu(s):
        val = 0
        mult = 1

        for c in reversed(s):
            val += mult * snafu_values[c]
            mult *= 5

        return val

    ics(from_snafu("1121-1110-1=0")) # 314159265
    ics(to_snafu(314159265)) # 314159265



    @timefunction
    def part1():
        result = to_snafu(sum(from_snafu(line) for line in inp))

        print_result(result)



    @timefunction
    def part2():
        last_config = None

        for round in count(1):
            ic(round)
            process(elves, checks_moves)

            if elves == last_config:
                break

            last_config = set(elves)

        ics(round, get_vis_map(elves))
        result = round
        print_result(result)

    part1()
#    part2()

def main():
#    print(real_inp)

    if 1:
        for samp_inp in samp_inps:
            print("Sample:")
            run(samp_inp, False)

    if 1:
        print("Actual:")
        run(real_inp, True)




samp_inp = r"""
1=-0-2
12111
2=0=
21
2=01
111
20012
112
1=-1=
1-12
12
1=
122
"""

short_samp = """
.....
..##.
..#..
.....
..##.
.....
"""


samp_inps = [
#    short_samp,
    samp_inp,
    ]



real_inp = r"""
2==-1222101=0=
12200
1=1
1=20-212
100
1202=0==111--2
101-0--0-1
1=0--=2=1--
10=0=02
1102-1
2110
20-12-
1110=-12-0=-0-01-0
1-11===212=102---
1=22=00201122-1
10=02=11-212=-0=00
2020222-211=202
12=0-00
1=2--2--01--=-1010
1=011--0=002
1-212--=-
1020==01--1---0
11==0==2-2=011-=
20=000-1--=-00
2202=21-1
2--10=12--
1000
111022
2-022
1=20==01=2-=
1-10=--
2=2=21-=11-1--===20
1==02100
1-=0
2=021-0122=
1-0==
1220-0-0=2
1=0-0=2-=1
10=112201=102
12=0-2-112
1==22102-2
112-0=02=100
1-020-
1001-20-
20-2=1=0110
10=-==-
1-12
20-10==-
1=1111022202=2101
1==1=1-=
10100
2=21--1=11=
22002-021=02
22
1=101-0010111---2===
1==20
1=2211001=-2001=-0
210==-=222-1
1=2-0=0
1-=12-2
20-1-0=---
220==121=
1-1110=2=-0-
1012-01=0002
102=121-0-002==-
2200=2-120212
1=1=22--2
1=2=220-0-22=01
2101-10-1-21
2-0-1=--2==-01-2
1000-=0210=--
1==11=-=1=0-1
1=0020-12-=-
1-220--1=-10-202-
1=-1===-2==02==-=21
21
2=2==-0-=2=-1-11=
1-0==20011201
1-100=
21=212-022=2-
2-10110=-0-2=1=-0=
1012
1==1==
1-11=0
1-20-0=-21111202==
1=0=012=-=2=10-
1=2=1
10-0
100-22==02
1===121-0=0===1-2=2
1-=-1-10222=12-
1==-0--0=2=2-2
10=2=11220021-=
211
202-0=11-===
1==0
1--0221-0
1=-=000-2=101-0
1-
1=02=2
1==
1---==1--
20=0
22-=1-011=2
12-112=
102==-=-021021=-=-2
1--2=2=100=20
12--10=0=2==2==2
1221-=2112-211
1222=12-110
2=--11
2-02
20222=-1222==
20-==-
2=-021
111-110-1=
10200=2010110
21==0=
101
1=-=-=1=1
21002010-20=-
1-122=02=2=2022=1
112--=221
1210
2=102=01102221-2
1=-1102111
2=-
2110=0==2-11001
1-00021100=-011
11
1=-
10000=00-=2=1-0
10=
"""

main()

