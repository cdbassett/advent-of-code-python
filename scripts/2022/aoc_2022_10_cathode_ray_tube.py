from functools import *
from collections import *
from itertools import *
from math import *
from builtins import pow
from icecream import ic

from utils.aoc_utils import * # this includes adding c:\ut to sys.path
from utils.utilities import *
import utils.seq_extensions # these extend PyFunctional seq objects, don't need to directly use anything in it


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
    example = get_aocd_example()
    samp_inps = split_example(example)

    for n, samp_inp in enumerate(samp_inps, 1):
        print(f"{Fore.BLUE}{Style.BRIGHT}Sample {n}:{Style.RESET_ALL}")
        run(samp_inp, False)

    if 1:
        print(f"{Fore.BLUE}{Style.BRIGHT}Actual:{Style.RESET_ALL}")
        real_inp = get_aocd_data()
        run(real_inp, True)

main()
