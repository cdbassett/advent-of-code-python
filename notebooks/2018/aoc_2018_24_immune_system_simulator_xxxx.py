# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.15.2
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% editable=false jupyter={"source_hidden": true}
from aoc_utils import *
if is_notebook():
    print(get_aoc_url())

# %% [markdown]
# # Imports

# %%
# %load_ext autoreload

# %%
from collections import *
import re

from icecream import ic
import parse

# %autoreload explicit
# import and reload these automatically
# %aimport aoc_utils, Utilities, iter_utils, seq_extensions, func_utils
from aoc_utils import * # this includes adding c:\ut to sys.path
from Utilities import *
from iter_utils import *
import seq_extensions # when running standalone, apparently need this import explicitly in main module
import aoc_utils

# %% [markdown]
# # Sample Data

# %%
sample_data1 = \
"""Immune System:
17 units each with 5390 hit points (weak to radiation, bludgeoning) with an attack that does 4507 fire damage at initiative 2
989 units each with 1274 hit points (immune to fire; weak to bludgeoning, slashing) with an attack that does 25 slashing damage at initiative 3

Infection:
801 units each with 4706 hit points (weak to radiation) with an attack that does 116 bludgeoning damage at initiative 1
4485 units each with 2961 hit points (immune to radiation; weak to fire, cold) with an attack that does 12 slashing damage at initiative 4"""
sample_data1s = [sample_data1]
sample_data2 = sample_data1

# %% [markdown]
# # Parse

# %%
Unit = namedtuple("Unit","count,hp,weaknesses,immunities,attack,attack_type,initiative")

def parse_line(line):
    weaknesses = immunities = tuple()
    cnt, hp, weakness_string, attack, attack_type, initiative = parse.parse("{:d} units each with {:d} hit points{}with an attack that does {:d} {} damage at initiative {:d}", line)

    for part in weakness_string.strip(" ()").split(";"):
        if part:
            words = part.split()
            severity = words[0]
            types = tuple(w.strip(" ,") for w in words[2:])

            if words[0] == "weak":
                weaknesses = types
            else:
                immunities = types

    return Unit(cnt,hp,weaknesses,immunities,attack,attack_type,initiative)

def parse_data(inp):
    immunity_strings, infection_strings = seq(inp.strip().split("\n")).split()
    #ic(immunity_strings,infection_strings)
    immunity_units = seq(immunity_strings[1:]).map(parse_line).list()
    infection_units = seq(infection_strings[1:]).map(parse_line).list()
    return immunity_units, infection_units

#parse_data(sample_data1)


# %% [markdown]
# # Process

# %%
def build_working_units(units, desc):
    return [[unit.count, unit, desc+str(n)] for n, unit in enumerate(units, 1)] # count is just initial count, here we create mutable count to allow reducing from attacks

def calc_damage(attacking_group, defending_group):
    attacking_count, attacking_unit, attacking_id = attacking_group
    defending_count, defending_unit, defending_id = defending_group

    if attacking_unit.attack_type in defending_unit.immunities:
        return 0

    attack_amount = attacking_unit.attack * attacking_count

    if attacking_unit.attack_type in defending_unit.weaknesses:
        attack_amount *= 2

    return attack_amount

# effective power = unit count * unit attack
# returns [attacking initiative, attacking group, defending group]
def pick_targets(attacking, defending):
    attackers = sorted(attacking, key = lambda a: (a[0] * a[1].attack, a[1].initiative), reverse=True)
    remaining_defenders = seq(defending).map(itemgetter(2)).set()
    targets = []

    for attacker in attackers:
        cnt, unit, id = attacker
        # sort (in decreasing order) by damage attacker would deal to defender, then defender's effective power, then defender's initiative
        defenders = list((((calc_damage(attacker, d), d[0] * d[1].attack, d[1].initiative), d) for d in defending if d[2] in remaining_defenders))

        if not defenders:
            break

        defenders = sorted(defenders, reverse=True)

        if 1 and is_sample:
            for (dmg, eff_power, initiative), defender in defenders:
                print(f"  {id} (ep={attacker[0] * attacker[1].attack}, in={attacker[1].initiative}, {attacker[1].attack_type}) would deal {defender[-1]} (ep={eff_power}, in={initiative}, weak={defender[1].weaknesses}, imm={defender[1].immunities}, {dmg} damage)")

        #ics(id, defenders[0])
        (dmg, eff_power, initiative), defender = defenders[0]
        # if attacker can actually damage defender
        if dmg:
            targets.append((unit.initiative, attacker, defender))
            remaining_defenders.remove(defender[-1])

    return targets

def group_health(group):
    return sum(w[0] * w[1].hp for w in group)

def battle(parsed, add_to_immune = 0):
    #ic("battle", add_to_immune)
    immunity_units, infection_units = parsed

    if add_to_immune:
        immunity_units = [unit._replace(attack=unit.attack+add_to_immune) for unit in immunity_units]

    working_immunity_units = build_working_units(immunity_units, "immune")
    working_infection_units = build_working_units(infection_units, "infection")
    alive = seq(working_immunity_units).concat(working_infection_units).map(itemgetter(2)).set()
    #ics(alive)
    last_immunity_health, last_infection_health = 0, 0

    # attacks happen in order of initiative, later (lower initiative) attackeing groups may have fewer or no units left to attack
    for round in count(1):
        immunity_health, infection_health = group_health(working_immunity_units), group_health(working_infection_units)
        ics(round, immunity_health, infection_health, len(working_immunity_units), len(working_infection_units))

        if immunity_health == last_immunity_health and infection_health == last_infection_health:
            print(f"STALEMATE!!!!! at round {round} for add_to_immune={add_to_immune}")
            ics(working_immunity_units, working_infection_units)
            return False, -1

        if 0 and is_sample:
            for group in working_immunity_units + working_infection_units:
                print(f"{group[-1]} contains {group[0]} units")

        last_immunity_health, last_infection_health = immunity_health, infection_health
        # target selection phase
        targets = pick_targets(working_infection_units, working_immunity_units) + pick_targets(working_immunity_units, working_infection_units)
        #ics(targets)

        targets.sort(reverse=True)

        # attacking phase
        for attacking_initiative, attacking_group, defending_group in targets:
            attacking_count, attacking_unit, attacking_id = attacking_group
            defending_count, defending_unit, defending_id = defending_group

            if attacking_id in alive and defending_id in alive:
                attack_amount = calc_damage(attacking_group, defending_group)
                killed = attack_amount // defending_unit.hp

                if is_sample:
                    print(f"    {attacking_id} ({attacking_unit.initiative}/{attacking_unit.attack*attacking_count}) attacks {defending_id} ({defending_unit.weaknesses}/{defending_unit.immunities}) with {attacking_unit.attack_type} for {attack_amount} killing {killed}/{defending_count}")

                if killed > defending_count:
                    alive.remove(defending_id)
                else:
                    defending_group[0] -= killed

        working_immunity_units = [w for w in working_immunity_units if w[-1] in alive]
        working_infection_units = [w for w in working_infection_units if w[-1] in alive]
        #ics("end")

        if not working_immunity_units or not working_infection_units:
            break
        if 0 and round == 5:
            break

    #ics(alive, working_immunity_units, working_infection_units)
    return bool(len(working_immunity_units)), sum(w[0] for w in working_immunity_units + working_infection_units)

def process(parsed, add_to_immune=0):
    #ic(len(parsed))
    #ics(parsed)
    immunity_won, num_units = battle(parsed, add_to_immune)
    ic(immunity_won, add_to_immune)
    return num_units


# %%
def part1(inp, add_to_immune=0):
    parsed = parse_data(inp)
    result = process(parsed, add_to_immune)
    print_result(result)


# %% [markdown]
# # Process2

# %%
def process2(parsed):
    def one_battle(add_to_immune):
        immunity_won, num_units = battle(parsed, add_to_immune)
        return immunity_won

    ic("started")

    if 0:
        for boost in count(32000):
            if one_battle(boost):
                return boost

    res = aoc_utils.find_lowest_int(one_battle, 1, 16)
    #ic(res)
    immunity_won, num_units = battle(parsed, res)
    #ic(res, immunity_won, num_units)
    #res -= 1
    #immunity_won, num_units = battle(parsed, res)
    #ic(res, immunity_won, num_units)
    return num_units


# %%
def part2(inp):
    parsed = parse_data(inp)
    result = process2(parsed)
    print_result(result)


# %% [markdown]
# # Sample data processing

# %%
insert_sample_functions(False, globals())

#for sample_data1 in sample_data1s:
#    part1(sample_data1)

#part1(sample_data1, 1570)
#part2(sample_data2)
#part1(real_inp, 51)
#part1(real_inp, 2048)

# %% [markdown]
# # Actual data

# %% editable=true slideshow={"slide_type": ""}
real_inp = get_aocd_data()
insert_sample_functions(True, globals())
part1(real_inp)

if 0:
    part1(real_inp, 50)
    part1(real_inp, 51)
    part1(real_inp, 52)
    part1(sample_data1, 1570)
    part1(sample_data1, 1569)

part2(real_inp) # 47372 is too high, 26366 is too high


# %% [markdown]
# # Others

# %%
def solve2():
    def binary_search(f, lo=0, hi=None):
        """
        Returns a value x such that f(x) is true.
        Based on the values of f at lo and hi.
        Assert that f(lo) != f(hi).
        """
        lo_bool = f(lo)

        if hi is None:
            offset = 1
            while f(lo+offset) == lo_bool:
                offset *= 2
            hi = lo + offset
        else:
            assert f(hi) != lo_bool

        best_so_far = lo if lo_bool else hi

        while lo <= hi:
            mid = (hi + lo) // 2
            result = f(mid)

            if result:
                best_so_far = mid

            if result == lo_bool:
                lo = mid + 1
            else:
                hi = mid - 1

        return best_so_far

    inp = real_inp

    def doit(boost=0, part1=False):
        lines = inp.splitlines()
        immune, infection = inp.split("\n\n")
        teams = []
        REGEX = re.compile(r"(\d+) units each with (\d+) hit points (\([^)]*\) )?with an attack that does (\d+) (\w+) damage at initiative (\d+)")

        # namedtuple? who needs namedtuple with hacks like these?
        UNITS, HP, DAMAGE, DTYPE, FAST, IMMUNE, WEAK = range(7)
        blah = boost

        for inps in [immune, infection]:
            lines = inps.splitlines()[1:]
            team = []
            for line in lines:
                s = REGEX.match(line)
                units, hp, extra, damage, dtype, fast = s.groups()
                immune = []
                weak = []

                if extra:
                    extra = extra.rstrip(" )").lstrip("(")

                    for s in extra.split("; "):
                        if s.startswith("weak to "):
                            weak = s[len("weak to "):].split(", ")
                        elif s.startswith("immune to "):
                            immune = s[len("immune to "):].split(", ")
                        else:
                            assert False

                u = [int(units), int(hp), int(damage) + blah, dtype, int(fast), set(immune), set(weak)]
                team.append(u)
            teams.append(team)
            blah = 0

        def power(t):
            return t[UNITS] * t[DAMAGE]

        def damage(attacking, defending):
            mod = 1
            if attacking[DTYPE] in defending[IMMUNE]:
                mod = 0
            elif attacking[DTYPE] in defending[WEAK]:
                mod = 2
            return power(attacking) * mod

        def sort_key(attacking, defending):
            return (damage(attacking, defending), power(defending), defending[FAST])

        while all(not all(u[UNITS] <= 0 for u in team) for team in teams):
            teams[0].sort(key=power, reverse=True)
            teams[1].sort(key=power, reverse=True)
            targets = []

            # target selection
            for team_i in range(2):
                other_team_i = 1 - team_i
                team = teams[team_i]
                other_team = teams[other_team_i]

                remaining_targets = set(i for i in range(len(other_team)) if other_team[i][UNITS] > 0)
                my_targets = [None] * len(team)

                for i, t in enumerate(team):
                    if not remaining_targets:
                        break

                    best_target = max(remaining_targets, key= lambda i: sort_key(t, other_team[i]))
                    enemy = other_team[best_target]

                    if damage(t, enemy) == 0:
                        continue

                    my_targets[i] = best_target
                    remaining_targets.remove(best_target)
                targets.append(my_targets)

            # attacking
            attack_sequence = [(0, i) for i in range(len(teams[0]))] + [(1, i) for i in range(len(teams[1]))]
            attack_sequence.sort(key=lambda x: teams[x[0]][x[1]][FAST], reverse=True)
            did_damage = False

            for team_i, index in attack_sequence:
                to_attack = targets[team_i][index]

                if to_attack is None:
                    continue

                me = teams[team_i][index]
                other = teams[1-team_i][to_attack]

                d = damage(me, other)
                d //= other[HP]

                if other[UNITS] > 0 and d > 0:
                    did_damage = True

                other[UNITS] = max(0, other[UNITS] - d)

            if not did_damage:
                return None

        if part1:
            return sum(u[UNITS] for u in teams[0]) or sum(u[UNITS] for u in teams[1])

        asd = sum(u[UNITS] for u in teams[0])

        if asd == 0:
            return None
        else:
            return asd

    print(doit(part1=True))
    # I did a manual binary search, submitted the right answer, then added in did_damage.
    # Turns out that doit can infinite loop without the did_damage check!
    # WARNING: "doit" is not guaranteed to be monotonic! You should manually check values yourself.
    # print(doit(33))

    for t in (33,50,51,52):
        print(t, doit(t))
    maybe = binary_search(doit)
    ic(maybe)
    print(doit(maybe))
    print(doit(33))

#solve2()


# %%
def solve1():
    class Group:
        def __init__(self, side, line, boost=0):
            self.side = side

            attribs, attack = line.split(';')
            units, hp, *type_mods = attribs.split()
            units=int(units)
            hp=int(hp)
            weak = []
            immune = []
            cur = None
            for w in type_mods:
                if w == "weak":
                    cur = weak
                elif w == "immune":
                    cur = immune
                else:
                    cur.append(w)

            self.units = units
            self.hp = hp
            self.weak = weak
            self.immune = immune

            attack_amount, attack_type, initiative = attack.split()
            attack_amount = int(attack_amount)
            initiative = int(initiative)

            self.attack = attack_amount + boost
            self.attack_type = attack_type
            self.initiative = initiative

            self.attacker = None
            self.target = None

        def clear(self):
            self.attacker = None
            self.target = None

        def choose(self, groups):
            assert self.target is None
            cands = [group for group in groups
                    if group.side != self.side
                    and group.attacker is None
                    and self.damage_prio(group)[0] > 0]
            if cands:
                self.target = max(cands, key=lambda group: self.damage_prio(group))
                assert self.target.attacker is None
                self.target.attacker = self

        def effective_power(self):
            return self.units * self.attack

        def target_prio(self):
            return (-self.effective_power(), -self.initiative)

        def damage_prio(self, target):
            if target.units == 0:
                return (0, 0, 0)
            if self.attack_type in target.immune:
                return (0, 0, 0)
            mul = 1
            if self.attack_type in target.weak:
                mul = 2
            return (mul * self.units * self.attack, target.effective_power(), target.initiative)

        def do_attack(self, target):
            total_attack = self.damage_prio(target)[0]
            killed = total_attack // target.hp
            target.units = max(0, target.units - killed)

    # immune_system_input = """17 5390 weak radiation bludgeoning;4507 fire 2
    # 989 1274 immune fire weak bludgeoning slashing;25 slashing 3"""
    #
    # infection_input = """801 4706 weak radiation;116 bludgeoning 1
    # 4485 2961 immune radiation weak fire cold;12 slashing 4"""

    immune_system_input, infection_input = real_inp.split("\n\n")
    immune_system_input = njoin(immune_system_input.split("\n")[1:])
    infection_input = njoin(infection_input.split("\n")[1:])
    print("immune_system_input:")
    print(immune_system_input)
    print("infection_input:")
    print(infection_input)
    #print(immune_system_input, infection_input)
    #ic(immune_system_input, infection_input)

    def solve(boost):
        immune_system_groups = [Group(False, line, boost) for line in immune_system_input.split("\n")]
        infection_groups = [Group(True, line) for line in infection_input.split("\n")]

        groups = immune_system_groups + infection_groups

        old = (-1, -1)
        while True:
            groups = sorted(groups, key=lambda group: group.target_prio())
            for group in groups:
                group.clear()
            for group in groups:
                group.choose(groups)
            groups = sorted(groups, key=lambda group: -group.initiative)
            for group in groups:
                if group.target:
                    group.do_attack(group.target)

            immune_system_units = sum(group.units for group in groups if group.side == False)
            infection_units = sum(group.units for group in groups if group.side == True)
            if (immune_system_units, infection_units) == old:
                return (immune_system_units, infection_units)
            old = (immune_system_units, infection_units)

    # star 1
    print(solve(0)[1])

    # star 2
    for boost in range(1000000):
        ans = solve(boost)
        if ans[1] == 0:
            print(ans[0])
            break
#solve1()

