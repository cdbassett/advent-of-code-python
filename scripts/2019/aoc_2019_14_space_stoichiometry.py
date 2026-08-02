from functools import *
from collections import *
from itertools import *
from math import *
from statistics import *
from builtins import pow

from colorama import Fore, Style
from functional import seq # https://github.com/EntilZha/PyFunctional
import iteration_utilities as it_ut # https://pypi.org/project/iteration-utilities/
import pyperclip
from icecream import ic
import networkx as nx
import matplotlib.pyplot as plt


from utils.timer_utils import timefunction
from utils.aoc_utils import * # this includes adding c:\ut to sys.path
from utils.utilities import *
import utils.seq_extensions # these extend PyFunctional seq objects, don't need to directly use anything in it


# https://adventofcode.com/2019/day/14


@timefunction
def run(inp1, inp2, is_real):
    insert_sample_functions(is_real, globals())

    def data_parse(inp):
        lines = inp.replace(" => ", ", ").strip().split('\n')
        parsed = seq(lines).map(comma_space_splitter).map(partial(map_tuple, str.split)).map(partial_right(multimap, int)).map(tuple)
        return parsed


    def build_dict(parsed):
        build = dict()

        for line in parsed:
            *ing, result = line
            build[result[1]] = result[0], ing

        ics(build)
        return build


    def calc_required(build, fuel_count=1):
        surplus = defaultdict(int)

        def get_required(elem, quant, level = 0):
            if elem == "ORE":
                return quant

            produces, ingredients = build[elem]
            need = 0
            indent = "  " * level
            needed = quant - surplus[elem]
            reactions = ceil(needed / produces)
            rem = reactions * produces - needed
            surplus[elem] = rem
#            ics(indent, elem, quant, produces, reactions, rem)

            for ing_cnt, ing in ingredients:
                amt = get_required(ing, ing_cnt * reactions, level + 1)
#                ics(indent, ing, ing_cnt, quant, amt)
                need += amt

#            ics(indent, elem, need, surplus)
            return need

        result = get_required("FUEL", fuel_count)
        return result

    def process1(parsed):
        build = build_dict(parsed)
        result = calc_required(build)

        if is_sample:
            G = nx.DiGraph()

            for elem, (cnt, ing) in build.items():
                for c, i in ing:
                    G.add_edge(elem, i, amt=c)

            pos = nx.spring_layout(G)
            nx.draw_networkx(G, pos, arrows=True)
            nx.draw_networkx_edge_labels(G, pos)
            plt.show()

        return result



    @timefunction
    def part1(inp):
        parsed = data_parse(inp)
        ics(parsed)
        result = process1(parsed)
        print_result(result)


    def process2(parsed):
        def binary_search(low, high, target_ore):
            most_fuel = 0
                # Check base case
            while high > low:
                fuel = (high + low) // 2
                required_ore = calc_required(build, fuel)

                if required_ore == target_ore:
                    return fuel
                if required_ore > target_ore:
                    high = fuel
                else:
                    most_fuel = max(most_fuel, fuel)
                    low = fuel + 1

            return most_fuel

        build = build_dict(parsed)
        ore_for_one = calc_required(build)
        ics(ore_for_one)
        approximate_fuel = 1000000000000 // ore_for_one
        smallest = approximate_fuel // 2
        largest = approximate_fuel * 2
        result = binary_search(smallest, largest, 1000000000000)
        return result


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


