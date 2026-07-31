from functools import *
from collections import *
#from sympy import *
from itertools import *
from math import *
from statistics import *
from builtins import pow
#import numpy as np
#import shapely
#import shapely.ops
from timer_utils import timefunction
#import networkx as nx
#import matplotlib.pyplot as plt
#from construct import *

#from Levenshtein import distance as levenshtein_distance
#from sympy import *

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
#from fz import _1
#from quicklambda import _1
from mini_lambda import s, _


@timefunction
def run(inp1, inp2, is_real):
    ics = nothing if is_real else ic
    print_result = partial(print_result_aoc, is_real)

#    numbers = string_to_integers(inp)

    def data_parse(inp):
#        lines = inp.strip().split('\n')
        lines = inp.strip("\n").split('\n')
        data_lines, my_ticket_lines, near_ticket_lines = split_iterable(lines, "")
        ics(data_lines, my_ticket_lines, near_ticket_lines)

        data = seq(data_lines).map(colon_space_splitter).multimap(identity, string_to_integers).to_dict()

        for field, values in data.items():
            values[:] = map(abs, values)

        ics(data)
        my_ticket = seq(my_ticket_lines[1]).map(string_to_integers).to_list()[0]
        ics(my_ticket)
        near_tickets = seq(near_ticket_lines[1:]).map(string_to_integers)
        ics(near_tickets)

        all_valid = set()

        for field, values in data.items():
            cur_set = set(range(values[0], values[1]+1))
            cur_set.update(range(values[2], values[3]+1))
            all_valid.update(cur_set)
            data[field] = cur_set

        ic(len(all_valid))
        return data, my_ticket, near_tickets, all_valid


    @timefunction
    def part1(inp):
        data, my_ticket, near_tickets, all_valid = data_parse(inp)
        result = 0

        for near_ticket in near_tickets:
            for num in near_ticket:
                if num not in all_valid:
                    result += num

        print_result(result)


    @timefunction
    def part2(inp):
        data, my_ticket, near_tickets, all_valid = data_parse(inp)
        valid_tickets = [my_ticket]
#        valid_tickets = []

        for near_ticket in near_tickets:
            for num in near_ticket:
                if num not in all_valid:
                    break
            else:
                valid_tickets.append(near_ticket)

        ics(valid_tickets)

        assert len(data) == len(my_ticket)

        known_fields = {}
        known_indexes = set()

        while len(known_fields) < len(data):
            ics(len(known_fields), len(data))

            for n in range(len(data)):
                if n not in known_indexes:
                    field_values = set(t[n] for t in valid_tickets)

                    possible_fields = [(field, valid) for field, valid in data.items() if field not in known_fields and not (field_values - valid)]
                    ics(n, field_values, possible_fields)

                    if len(possible_fields) == 1:
                        known_fields[list(possible_fields)[0][0]] = n
                        known_indexes.add(n)

        ics(known_fields)

        if is_real:
            result = products(my_ticket[index] for field, index in known_fields.items() if field.startswith("departure"))
            print_result(result)

    part1(inp1)
    part2(inp2)

def main():
    if 1:
        if samp_inps:
            for samp_inp in samp_inps:
                print(f"{Fore.GREEN}{Style.BRIGHT}Sample:{Style.RESET_ALL}")
                run(samp_inp1, samp_inp2, False)
        else:
            print(f"{Fore.BLUE}{Style.BRIGHT}Sample:{Style.RESET_ALL}")
#            print("Sample:")
            run(samp_inp1, samp_inp2, False)

    if 1:
        print(f"{Fore.YELLOW}{Style.BRIGHT}Actual:{Style.RESET_ALL}")
#        print("Actual:")
            # needs env var AOC_SESSION
        real_inp = aocd.data # supposed to work if filename is clear enough (year would need to be 4-digit)
        run(real_inp, real_inp, True)
#        aocd.submit(my_answer)




samp_inp1 = r"""
class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12
"""

samp_inp2 = r"""
class: 0-1 or 4-19
row: 0-5 or 8-19
seat: 0-13 or 16-19

your ticket:
11,12,13

nearby tickets:
3,9,18
15,1,5
5,14,9
"""


short_samp = """
"""


samp_inps = [
#    short_samp,
#    samp_inp,
    ]


main()

