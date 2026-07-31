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

from aoc_utils import * # this includes adding c:\ut to sys.path
from Utilities import *
import seq_extensions # these extend PyFunctional seq objects, don't need to directly use anything in it
from quicklambda import _1, _2


@timefunction
def run(inp1, inp2, is_real):
    insert_sample_functions(is_real, globals())

    def data_parse(inp):
        lines = inp.strip().split('\n')
#        numbers = map(string_to_integers, lines)
        city_to_city_dist = seq(lines).map(equals_space_splitter).multimap(to_space_splitter, int).to_list()
        ics(city_to_city_dist)
        neighbors = defaultdict(list)
        cities = set()

        for (from_city, to_city), dist in city_to_city_dist:
            neighbors[from_city].append((dist, to_city))
            neighbors[to_city].append((dist, from_city))
            cities.add(from_city)
            cities.add(to_city)

        ic(len(cities))
#        ics(neighbors)

        return city_to_city_dist, neighbors, cities


# start from anywhere, end anywhere, must include all cities

    def process1(parsed, better, final):
        city_to_city_dist, neighbors, cities = parsed

        queue = []
        put, get = get_queue_functions_lifo(queue)
        city_count = len(cities)
        full_paths = {}

        for city in cities:
            put((0, city, {city: None})) # ordered set behavior

        while queue:
#            iterations += 1
            cost, city, path = get()
            start_city = first_element(path)

            if len(path) == city_count:
                existing = full_paths.get(start_city)

                if existing is None or better(cost, existing):
                    full_paths[start_city] = cost

                continue

            for dist, neighbor in neighbors[city]:
                if neighbor not in path:
                    new_cost = cost + dist
                    new_path = dict(path)
                    new_path[neighbor] = None # ordered set behavior
                    put((new_cost, neighbor, new_path))

        ic(len(full_paths))
        ics(full_paths)
        return final(full_paths.values())



    @timefunction
    def part1(inp):
        parsed = data_parse(inp)
        result = process1(parsed, lambda a, b: a < b, min)
        print_result(result)

    process2 = process1


    @timefunction
    def part2(inp):
        parsed = data_parse(inp)
        result = process1(parsed, lambda a, b: a > b, max)
        print_result(result)

    part1(inp1)
    part2(inp2)

def main():
    if 1:
        if samp_inps and samp_inps[0]:
            for n, samp_inp in enumerate(samp_inps, 1):
                print_preface(False, n)
                run(samp_inp, samp_inp, False)
        else:
            print_preface(False)
            run(samp_inp1, samp_inp2, False)

    if 1:
        print_preface(True)
        real_inp = get_aocd_data()
        run(real_inp, real_inp, True)
#        aocd.submit(my_answer)




samp_inp1 = r"""
London to Dublin = 464
London to Belfast = 518
Dublin to Belfast = 141
"""

samp_inp2 = samp_inp1
#samp_inp2 = r"""
#"""


samp_inps = \
"""
""".strip().split("\n")


main()


