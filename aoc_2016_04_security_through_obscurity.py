from functools import *
from collections import *
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
import aocd # https://github.com/wimglenn/advent-of-code-data
# aocd.lines  # like data.splitlines()
# aocd.numbers # uses regex pattern -?\d+ to extract integers from data


from aoc_utils import * # this includes adding c:\ut to sys.path
from Utilities import *
import seq_extensions # these extend PyFunctional seq objects, don't need to directly use anything in it
from quicklambda import _1, _2



@timefunction
def run(inp1, inp2, is_real):
    insert_sample_functions(is_real, globals())

    def data_parse(inp):
        lines = inp.strip().replace("["," ").replace("]","").split('\n')
#        parsed = map_list(str.split, lines)
        parsed = seq(lines).map(str.split).multimap(dash_splitter).to_list()
        return parsed


    def room_is_valid(room):
        mcl = Counter(sjoin(room[0])).most_common()
#        [('a', 5), ('b', 2), ('r', 2)]
#        ics(mcl)
#        ics(list((-b, a) for a, b in mcl))
#        ics(sorted((-b, a) for a, b in mcl))
        letters = sjoin(map(itemgetter(1), sorted((-b, a) for a, b in mcl)))[:5]
        valid = letters == room[-1]
#        ics(room, letters, valid)
        return valid

    def valid_rooms(parsed):
        rooms = [(room[0][:-1], int(room[0][-1]), room[1]) for room in parsed]
        return [room for room in rooms if room_is_valid(room)]

    def process1(parsed):
        rooms = valid_rooms(parsed)
        ics("process1", rooms)
        return sum(room[1] for room in rooms)

    @timefunction
    def part1(inp):
        parsed = data_parse(inp)
#        ics(parsed)
        result = process1(parsed)
        print_result(result)

    process2 = process1

    orda = ord("a")

    def shift(sector, c):
        return chr(((ord(c) - orda) + sector) % 26 + orda)

    def shifted(room):
        return " ".join(map(compose(partial(map, partial(shift, room[1])), sjoin), room[0]))



    def process2(parsed):
        rooms = valid_rooms(parsed)

        for room in rooms:
            room_name = shifted(room)
            ics(room_name)

            if "north" in room_name:
                ic(room_name, room[1])
                return room[1]

        return 0


    @timefunction
    def part2(inp):
        parsed = data_parse(inp)
        result = process2(parsed)
        print_result(result)

    part1(inp1)
    part2(inp2)

def main():
    example = get_aocd_example()
    samp_inps = split_example(example)

    for n, samp_inp in enumerate(samp_inps, 1):
        print(f"{Fore.BLUE}{Style.BRIGHT}Sample {n}:{Style.RESET_ALL}")
        run(samp_inp, samp_inp, False)

    if 1:
        print(f"{Fore.BLUE}{Style.BRIGHT}Actual:{Style.RESET_ALL}")
        # needs env var AOC_SESSION
        real_inp = get_aocd_data()
        run(real_inp, real_inp, True)
#        aocd.submit(my_answer)


main()

