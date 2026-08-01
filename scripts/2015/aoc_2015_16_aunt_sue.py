from functools import *
from collections import *
from itertools import *
from math import *
from statistics import *
from builtins import pow
import operator
from utils.timer_utils import timefunction


from colorama import Fore, Style
from functional import seq # https://github.com/EntilZha/PyFunctional
import iteration_utilities as it_ut # https://pypi.org/project/iteration-utilities/
import pyperclip
from icecream import ic
import aocd # https://github.com/wimglenn/advent-of-code-data
# aocd.lines  # like data.splitlines()
# aocd.numbers # uses regex pattern -?\d+ to extract integers from data


from utils.aoc_utils import * # this includes adding c:\ut to sys.path
from utils.utilities import *
import utils.seq_extensions # these extend PyFunctional seq objects, don't need to directly use anything in it
from mini_lambda import s, _, x

aunt_attrs = seq("""
children: 3
cats: 7
samoyeds: 2
pomeranians: 3
akitas: 0
vizslas: 0
goldfish: 5
trees: 3
cars: 2
perfumes: 1
""".strip().split('\n')).map(colon_space_splitter).multimap(identity, int).to_dict()
ic(aunt_attrs)

conditions = {key: operator.eq for key,_ in aunt_attrs.items()}
conditions.update({
    "cats": operator.gt,
    "trees": operator.gt,
    "pomeranians": operator.lt,
    "goldfish": operator.lt,
    })
ic(conditions)

ic(conditions["cats"](5, 0))
ic(conditions["goldfish"](5, 0))
ic(conditions["cats"](5, 5))
ic(conditions["goldfish"](5, 5))


@timefunction
def run(inp1, inp2, is_real):
    insert_sample_functions(is_real, globals())

    def data_parse(inp):
#        lines = inp.strip().split('\n')
        lines = inp.strip().replace(":", "").replace(",", "").split('\n')
#        ics(lines)

#        data = seq(lines).map(compose(comma_space_splitter, partial(map, colon_space_splitter), dict)).to_list()
#        data = seq(lines).map(compose(comma_space_splitter, rpartial(islice, 1, None), partial(map_tuple, colon_space_splitter))).to_list()
#        data = seq(lines).map(compose(str.split, rpartial(islice, 2, None), rpartial(chunks_of_n, 2), rpartial(multimap, identity, int), list)).to_list()
        data = seq(lines).map(compose(str.split, rpartial(islice, 2, None), rpartial(chunks_of_n, 2), rpartial(multimap, identity, int), dict)).to_list()
        ic(data[:10])

        return data


    def process1(parsed):
        for aunt, line in enumerate(parsed, 1):
            for entry, cnt in line.items():
                if aunt_attrs[entry] != cnt:
                    break
            else:
                return aunt

        return 0



    @timefunction
    def part1(inp):
        parsed = data_parse(inp)
        result = process1(parsed)
        print_result(result)

    process2 = process1


    def process2(parsed):
        for aunt, line in enumerate(parsed, 1):
            for entry, cnt in line.items():
                if not conditions[entry](cnt, aunt_attrs[entry]):
                    ic(conditions[entry], entry, aunt_attrs[entry], cnt)
                    break
            else:
                return aunt

        return 0


    @timefunction
    def part2(inp):
        parsed = data_parse(inp)
        result = process2(parsed)
        # 21 is not right
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


