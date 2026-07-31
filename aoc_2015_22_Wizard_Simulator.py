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


char = namedtuple("char", "hp,damage")


@timefunction
def run(inp1, inp2, is_real):
    insert_sample_functions(is_real, globals())

    def data_parse(inp):
        lines = inp.strip().split('\n')
        parsed = seq(lines).map(compose(colon_space_splitter, second_elem, int))
        return parsed

    def countdown(val):
        return max(val-1, 0)

#    Magic Missile costs 53 mana. It instantly does 4 damage.
#    Drain costs 73 mana. It instantly does 2 damage and heals you for 2 hit points.
#    Shield costs 113 mana. It starts an effect that lasts for 6 turns. While it is active, your armor is increased by 7.
#    Poison costs 173 mana. It starts an effect that lasts for 6 turns. At the start of each turn while it is active, it deals the boss 3 damage.
#    Recharge costs 229 mana. It starts an effect that lasts for 5 turns. At the start of each turn while it is active, it gives you 101 new mana.

    def process1(parsed, player_hp, player_mana=500, health_dec = 0):
        boss = char(*parsed)
        queue = []
        put, get = get_queue_functions_smallest(queue) # first element is mana spent
        put((0, True, player_mana, player_hp, boss.hp, 0, 0, 0, ()))

        while queue:
            mana_spent, player_turn, mana, player_hp, boss_hp, shield_turns, poison_turns, recharge_turns, spells = get()

            if recharge_turns:
                mana += 101

            if poison_turns:
                boss_hp -= 3

            shield_turns, poison_turns, recharge_turns = map(countdown, (shield_turns, poison_turns, recharge_turns))
            player_hp -= health_dec

            if player_hp <= 0:
                continue

            if boss_hp <= 0:
                ic(mana, spells, player_hp, shield_turns, poison_turns, recharge_turns)
                return mana_spent

            if player_turn:
                    # magic missile
                if mana >= 53:
                    put((mana_spent + 53, False, mana - 53, player_hp, boss_hp - 4, shield_turns, poison_turns, recharge_turns, spells+("Missile",)))

                    # Drain
                if mana >= 73:
                    put((mana_spent + 73, False, mana - 73, player_hp + 2, boss_hp - 2, shield_turns, poison_turns, recharge_turns, spells+("Drain",)))

                    # Shield
                if mana >= 113 and not shield_turns:
                    put((mana_spent + 113, False, mana - 113, player_hp, boss_hp, 6, poison_turns, recharge_turns, spells+("Shield",)))

                    # Poison
                if mana >= 173 and not poison_turns:
                    put((mana_spent + 173, False, mana - 173, player_hp, boss_hp, shield_turns, 6, recharge_turns, spells+("Poison",)))

                    # Recharge
                if mana >= 229 and not recharge_turns:
                    put((mana_spent + 229, False, mana - 229, player_hp, boss_hp, shield_turns, poison_turns, 5, spells+("Recharge",)))
            else:
                armor = 7 if shield_turns else 0
                player_hp -= max(1, (boss.damage - armor))

                if player_hp > 0:
                    put((mana_spent, True, mana, player_hp, boss_hp, shield_turns, poison_turns, recharge_turns, spells))

    @timefunction
    def part1(inp):
        parsed = data_parse(inp)
        ics(parsed)
        result = process1(parsed, 50 if is_real else 10, 500 if is_real else 250)
        print_result(result)

    process2 = process1

    @timefunction
    def part2(inp):
        parsed = data_parse(inp)
        result = process2(parsed, 50 if is_real else 10, 500 if is_real else 250, 1)
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
Hit Points: 13
Damage: 8
"""

samp_inp2 = samp_inp1


samp_inps = [
"""
Hit Points: 13
Damage: 8
""",
"""
Hit Points: 14
Damage: 8
"""

    ]


main()

