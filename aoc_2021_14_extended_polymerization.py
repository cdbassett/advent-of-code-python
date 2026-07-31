from functools import *
from collections import *
from itertools import *
from math import *
from statistics import *
from builtins import pow
import pyperclip
from icecream import ic
from timer_utils import timefunction

from aoc_utils import * # this includes adding c:\ut to sys.path
from Utilities import *
import seq_extensions # these extend PyFunctional seq objects, don't need to directly use anything in it

#Connection = namedtuple("Connection", "start,")
Point = namedtuple("Point", "x,y")


def run(inp, is_real):
    ics = nothing if is_real else ic
    print_result = partial(print_result_aoc, is_real)

    inp = inp.strip().split('\n')
    template = inp[0]
    rules = dict(line.split(" -> ") for line in inp[2:])
#    ics(rules)
    test_steps = 10

    @timefunction
    def part1():
        working = template
#        ics(pairwise(working))

        for step in range(test_steps):
            working = working[0] + "".join(rules.get(a+b, "") + b for a, b in pairwise(working))
#            ics(step, working)

        count = Counter(working)
        mc = count.most_common()
        result = mc[0][1] - mc[-1][1]
        print_result(result)

        # works but too slow
    def part2():
        working = template
        ics(working)

        for step in range(40):
            print(".", end="", flush=True)
            working = working[0] + "".join(rules.get(a+b, "") + b for a, b in pairwise(working))
#            ics(step, working)

        count = Counter(working)
        mc = count.most_common()
        result = mc[0][1] - mc[-1][1]
        print_result(result)

    def build_polymer(a, b, step):
        next_step = step - 1
        ab = a + b

        if next_step < 0:
            return b

        insert = rules.get(ab)

        if insert:
            return build_polymer(a, insert, next_step) + build_polymer(insert, b, next_step)

        return b

    @cache
    def build_polymer_cached(a, b, step):
        next_step = step - 1
        ab = a + b

        if next_step < 0:
            return b

        insert = rules.get(ab)

        if insert:
            return build_polymer(a, insert, next_step) + build_polymer(insert, b, next_step)

        return b

    # works but still too slow
    @timefunction
    def part2():
        parts = [template[0]]

        for a, b in pairwise(template):
            parts.append(build_polymer_cached(a, b, test_steps))

        working = "".join(parts)
#        ics(working)
        ics(len(working))

        count = Counter(working)
        mc = count.most_common()
        result = mc[0][1] - mc[-1][1]
        print_result(result)

    def count_polymer(a, b, step, counter):
        next_step = step - 1

        if next_step < 0:
            return

        insert = rules.get(a + b)

        if insert:
            counter[insert] += 1
            count_polymer(a, insert, next_step, counter)
            count_polymer(insert, b, next_step, counter)

    # works but even this is still too slow
    @timefunction
    def part2():
        counter = Counter(template)

        for a, b in pairwise(template):
            count_polymer(a, b, 40, counter)

#        ics(working)

        mc = counter.most_common()
        result = mc[0][1] - mc[-1][1]
        print_result(result)

    @timefunction
    def part2():
        counter = Counter(a+b for a, b in pairwise(template))
        next_counter = counter
        ics(template, counter)

        for step in range(40):
#            ics(step)
            next_counter = Counter()

            for key, cnt in counter.items():
#                ics(key)
                a, b = key
#                ics(a,b)
                insert = rules[key]
                next_counter[a+insert] += cnt
                next_counter[insert+b] += cnt

#            if step < 5:
#            ics(next_counter)

            counter = next_counter

        single_counts = Counter((template[0], template[-1]))

        for key, cnt in counter.items():
#            half_count = cnt/2
            a, b = key
            single_counts[a] += cnt
            single_counts[b] += cnt

        mc = single_counts.most_common()
        result = (mc[0][1] - mc[-1][1]) // 2
        print_result(result)

    part1()
    part2()

def main():
    print("Sample:")
    run(samp_inp, False)

    print("Actual:")
    run(real_inp, True)




samp_inp = r"""
NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C
"""


real_inp = r"""
CVKKFSSNNHNPSPPKBHPB

OF -> S
VO -> F
BP -> S
FC -> S
PN -> K
HC -> P
PP -> N
FK -> V
KN -> C
BO -> O
KS -> B
FF -> S
KC -> B
FV -> C
VF -> N
HS -> H
OS -> F
VC -> S
VP -> P
BC -> O
HF -> F
HO -> F
PC -> B
CC -> K
NB -> N
KK -> N
KP -> V
BH -> H
BF -> O
OB -> F
VK -> P
FB -> O
NP -> B
CB -> C
PS -> S
KO -> V
SP -> C
BK -> O
NN -> O
OC -> F
VB -> B
ON -> K
NK -> B
CK -> H
NH -> N
CV -> C
PF -> P
PV -> V
CP -> N
FP -> N
SB -> B
SN -> N
KF -> F
HP -> S
BN -> V
NF -> B
PO -> O
CH -> O
VV -> S
OV -> V
SF -> P
BV -> S
FH -> V
CN -> H
VH -> V
HB -> B
FN -> P
OH -> S
SK -> H
OP -> H
VN -> V
HN -> P
BS -> S
CF -> B
PB -> H
SS -> K
NV -> P
FS -> N
CS -> O
OK -> B
CO -> O
VS -> F
OO -> B
NO -> H
SO -> F
HH -> K
FO -> H
SH -> O
HV -> B
SV -> N
PH -> F
BB -> P
KV -> B
KB -> H
KH -> N
NC -> P
SC -> S
PK -> B
NS -> V
HK -> B"""

main()

