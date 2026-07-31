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

shop = """
Weapons:    Cost  Damage  Armor
Dagger        8     4       0
Shortsword   10     5       0
Warhammer    25     6       0
Longsword    40     7       0
Greataxe     74     8       0

Armor:      Cost  Damage  Armor
Leather      13     0       1
Chainmail    31     0       2
Splintmail   53     0       3
Bandedmail   75     0       4
Platemail   102     0       5

Rings:      Cost  Damage  Armor
Damage +1    25     1       0
Damage +2    50     2       0
Damage +3   100     3       0
Defense +1   20     0       1
Defense +2   40     0       2
Defense +3   80     0       3
""".replace(" +", "_+").strip().split('\n')

char = namedtuple("char", "hp,damage,armor")
item = namedtuple("item", "desc,cost,damage,armor")

#shop_items = list(split_iterable(seq(shop).map(str.split), ""))
shop_items = list(split_iterable(seq(shop).map(str.split), []))
(weapons_hdr, *weapons), (armor_hdr, *armors), (ring_hdr, *rings) = shop_items

# additions to calcualte with and without more easily
armors += [("NoArmor",0,0,0)]
rings += [("NoRing",0,0,0)]*2

weapons = seq(weapons).multimap(identity,fillvalue=int).starmap(item).to_list()
armors = seq(armors).multimap(identity,fillvalue=int).starmap(item).to_list()
rings = seq(rings).multimap(identity,fillvalue=int).starmap(item).to_list()





#shop_items = list(split_iterable(seq(shop).map(str.split).multimap(identity,fillvalue=int), []))
#ic(shop_items)
ic(weapons, armors, rings)


@timefunction
def run(inp1, inp2, is_real):
    insert_sample_functions(is_real, globals())

    def data_parse(inp):
        lines = inp.strip().split('\n')
        parsed = seq(lines).map(compose(colon_space_splitter, second_elem, int))
        return parsed

    def turns(attacker, defender):
        return ceil(defender.hp / max(1, (attacker.damage - defender.armor)))

    def player_wins(boss, player):
        player_turns = turns(player, boss)
        boss_turns  = turns(boss, player)
#        ics(boss, player)
#        ics(player_turns, boss_turns)
        return player_turns <= boss_turns

    boss = char(12, 7, 2)
    player = char(8, 5, 5)
    ics(player_wins(boss, player))
    ics(player_wins(player, boss))

    def check_win(boss, player_hp, items):
        cost = seq(items).sum(second_elem)
        damage = seq(items).sum(third_elem)
        armor = seq(items).sum(fourth_elem)
        player = char(player_hp, damage, armor)
        return cost, player_wins(boss, player)

    items = [weapons[3]]
    ics(items, check_win(boss, 8, items))
    items = [weapons[3], rings[0]]
    ics(items, check_win(boss, 8, items))
    items = [weapons[1], armors[4]]
    ics(items, check_win(boss, 8, items))

    def process1(parsed, player_hp, better_func):
        boss = char(*parsed)
        # must equip exactly one weapon
        # can equip exactly one armor
        # can equip 0-2 rings
#        queue = []
#        put, get = get_queue_functions_lifo(queue)
        best_cost = None
        best_items = None

        for weapon, armor, ring_pair in product(weapons, armors, combinations(rings, 2)):
            items = (weapon, armor) + ring_pair
            cost, won = check_win(boss, player_hp, items)

            if better_func(won, cost, best_cost):
                best_items = items
                best_cost = cost

        ic(best_items)
        return best_cost

    @timefunction
    def part1(inp):
        parsed = data_parse(inp)
        ics(parsed)
        result = process1(parsed, 100 if is_real else 8, lambda won, cost, best_cost: won and (best_cost is None or cost < best_cost))
        print_result(result)

    process2 = process1

    @timefunction
    def part2(inp):
        parsed = data_parse(inp)
        result = process2(parsed, 100 if is_real else 8, lambda won, cost, best_cost: not won and (best_cost is None or cost > best_cost))
        print_result(result)

    part1(inp1)
    part2(inp2)

def main():
    if 1:
        if samp_inps:
            for n, samp_inp in enumerate(samp_inps, 1):
                print_preface(False, n)
                run(samp_inp, samp_inp, False)
        elif samp_inp1.strip():
            print_preface(False)
            run(samp_inp1, samp_inp2, False)

    if 1:
        print_preface(True)
            # needs env var AOC_SESSION
        real_inp = aocd.data # supposed to work if filename is clear enough (year would need to be 4-digit)
        run(real_inp, real_inp, True)
#        aocd.submit(my_answer)




samp_inp1 = r"""
Hit Points: 12
Damage: 7
Armor: 2
"""

samp_inp2 = samp_inp1


samp_inps = [
    ]


main()

