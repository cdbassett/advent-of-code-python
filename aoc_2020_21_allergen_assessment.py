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
from mini_lambda import s, _, x

icf = ic.format

@timefunction
def run(inp1, inp2, is_real):
    insert_sample_functions(is_real, globals())

    def data_parse(inp):
        lines = inp.strip().split('\n')
#        lines = inp.strip("\n").split('\n')
        ingred_and_allergen = seq(lines).map(partial(str.split, sep="(contains ")).multimap(str.split, _(s[:-1].split(", "))).multimap(set, set)
        ics(ingred_and_allergen)
        return ingred_and_allergen

         # Each allergen is found in exactly one ingredient. Each ingredient contains zero or one allergen. Allergens aren't always marked.
    def process(ingred_and_allergen):
        all_ingredients = sets_union(ingreds for ingreds, allergens in ingred_and_allergen)
        all_allergens = sets_union(allergens for ingreds, allergens in ingred_and_allergen)
        allerg_to_possible_ingreds = dict((allerg,  sets_intersection(ingreds for ingreds, allergens in ingred_and_allergen if allerg in allergens)) for allerg in all_allergens)
            # this is not correct, allergens aren't always marked
#        ing_to_possible_allergens = dict((ing,  sets_intersection(allergens for ingreds, allergens in ingred_and_allergen if ing in ingreds)) for ing in all_ingredients)
        ics(allerg_to_possible_ingreds)

        ingreds_with_no_allergens = set()
        ingred_to_allergen = {}

        while allerg_to_possible_ingreds:
            for allerg, possible_ingreds in list(allerg_to_possible_ingreds.items()):
                if len(possible_ingreds) == 1:
                    ing = first(possible_ingreds)
                    ingred_to_allergen[ing] = allerg
                    allerg_to_possible_ingreds.pop(allerg)

                    for chk_allerg, chk_possible_ingreds in allerg_to_possible_ingreds.items():
                        chk_possible_ingreds.discard(ing)

        ics(allerg_to_possible_ingreds)
        ics(ingred_to_allergen)
        return ingred_to_allergen, all_ingredients, all_allergens


    @timefunction
    def part1(inp):
        ingred_and_allergen = data_parse(inp)
        ingred_to_allergen, all_ingredients, all_allergens = process(ingred_and_allergen)
        ingreds_wo_allergens = all_ingredients - ingred_to_allergen.keys()
        ics(ingreds_wo_allergens)
        result = sum(len(ingreds & ingreds_wo_allergens) for ingreds, allergens in ingred_and_allergen)
        print_result(result)

    @timefunction
    def part2(inp):
        ingred_and_allergen = data_parse(inp)
        ingred_to_allergen, all_ingredients, all_allergens = process(ingred_and_allergen)
        result = ",".join(map(itemgetter(0), sorted(ingred_to_allergen.items(), key=itemgetter(1))))
        print_result(result)

    part1(inp1)
    part2(inp2)

def main():
    if 1:
        if samp_inps:
            for n, samp_inp in enumerate(samp_inps, 1):
                print(f"{Fore.BLUE}{Style.BRIGHT}Sample {n}:{Style.RESET_ALL}")
                run(samp_inp, samp_inp, False)
        else:
            print(f"{Fore.BLUE}{Style.BRIGHT}Sample:{Style.RESET_ALL}")
            run(samp_inp1, samp_inp2, False)

    if 1:
        print(f"{Fore.BLUE}{Style.BRIGHT}Actual:{Style.RESET_ALL}")
            # needs env var AOC_SESSION
        real_inp = aocd.data # supposed to work if filename is clear enough (year would need to be 4-digit)
        run(real_inp, real_inp, True)
#        aocd.submit(my_answer)




samp_inp1 = r"""
mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)
"""

samp_inp2 = samp_inp1


short_samp = """
"""


samp_inps = [
#    short_samp,
#    samp_inp,
    ]


main()

