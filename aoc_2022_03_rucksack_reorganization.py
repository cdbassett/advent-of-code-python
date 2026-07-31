from functools import *
from collections import *
from itertools import *
from math import *
from builtins import pow
import pyperclip
from icecream import ic

from aoc_utils import * # this includes adding c:\ut to sys.path
from Utilities import *
import seq_extensions # these extend PyFunctional seq objects, don't need to directly use anything in it

priority_string = "_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def priority(c):
    return priority_string.find(c)

def unique_item(ruck):
    return first(sets_intersection(ruck))

def unique_items(rucks):
    return [unique_item(ruck) for ruck in rucks]

def main(inp, is_real):
    insert_sample_functions(is_real, globals())
    print_preface(is_real)
    inp = inp.strip().split('\n')

    def part1(inp, is_real):
        rucks = [n_chunks(line, 2) for line in inp]
#        print_list("rucks", rucks)
        uniques = unique_items(rucks)
        print_list("uniques", uniques)
        priorities = [priority(u) for u in uniques]
        print_list("priorities", priorities)
        score = sum(priorities)
        print_result(score)

    def part2(inp, is_real):
        rucks = list(chunks_of_n(inp, 3))
#        rucks = list(chunk(inp, 3))
#        print_list("rucks", rucks)
        uniques = unique_items(rucks)
        print_list("uniques", uniques)
        priorities = [priority(u) for u in uniques]
        print_list("priorities", priorities)
        score = sum(priorities)
        print_result(score)

    part1(inp, is_real)
    part2(inp, is_real)






samp_inp = r"""
vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
"""

main(samp_inp, False)

real_inp = get_aocd_data()
main(real_inp, True)

