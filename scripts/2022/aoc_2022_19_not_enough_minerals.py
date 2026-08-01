from functools import *
from collections import *
from itertools import *
from math import *
from statistics import *
from builtins import pow
import pyperclip
import operator
from icecream import ic
import shapely
import shapely.ops
from utils.timer_utils import timefunction
import matplotlib.pyplot as plt

from utils.aoc_utils import * # this includes adding c:\ut to sys.path
from utils.utilities import *
import utils.seq_extensions # these extend PyFunctional seq objects, don't need to directly use anything in it

Materials = namedtuple("Materials", "ore,clay,obsidian,geodes")
Blueprint = namedtuple("Blueprint", "ore_robot_cost,clay_robot_cost,obsidian_robot_cost,geode_robot_cost,max_costs,index")

ore, clay, obsidian, geodes = range(4)

def build_materials(ore=0, clay=0, obsidian=0, geodes=0): # actually used
    return Materials(ore,clay,obsidian,geodes)


def run(inp, is_real):
    ics = nothing if is_real else ic
    print_result = partial(print_result_aoc, is_real)

    inp = inp.strip().split('\n')

    costs = [tuple(map(int, (p for p in line.split() if p.isnumeric()))) for line in inp]
#    ics(costs)

    blueprints = []
    robot_costs = []

    for n, e in enumerate(costs):
        build = [
            build_materials(e[0]), # ore_robot_cost
            build_materials(e[1]), # clay_robot_cost
            build_materials(e[2],e[3]), # obsidian_robot_cost
            Materials(e[4],0,e[5],0), # obsidian_robot_cost
        ]
        max_costs = Materials(*(max(m[n] for m in build) for n in range(4)))

        blueprints.append(
            Blueprint(*(build + [max_costs, n]))
            )

#    ics(blueprints)

    def adjusted(p, adjust):
        return tuple(a + b for a, b in zip(p, adjust))

    def is_in(p, adjust):
        check = adjusted(p, adjust)
        return check in points



    """
    """

    max_geodes = []
    starting_robots = build_materials(1)
    starting_materials = build_materials()

    @cache
    def time_for_resources(costs, materials, robots):
        max_time = 0

        for cost, robot, material in zip(costs, robots, materials):
            if not cost:
                continue;

            if not robot:
                return 1000; # Y'know, infinity.

            max_time = max(max_time, (cost - material - 1 + robot) // robot)

        return max_time

        # can't cache bc first check is against running max
    def calc_best_output(blueprint, materials, robots, time):
        if not time:
            return 0

            # don't continue if we can't beat best time already
            # https://en.wikipedia.org/wiki/Triangular_number
        if (time * time - time) / 2 + robots.geodes * time <= max_geodes[blueprint.index] - materials.geodes:
            return 0

        max_mined_geodes = materials.geodes + robots.geodes * time # start with how many we'd mine if we built no more

            # each loop build one robot, waiting long enough for that robot to be built
        for n_robot, robot_cost in enumerate(blueprint[:-2]):
                # don't bother building more of this robot if we already have enough to cover max cost of resource it produces
            if n_robot < 3 and robots[n_robot] >= blueprint.max_costs[n_robot]:
#                ics(n_robot, robots[n_robot], blueprint.max_costs[n_robot])
                continue

            wait = time_for_resources(robot_cost, materials, robots) + 1

            if time - wait < 1:
                continue

            materials_copy = list(materials)
            robots_copy = list(robots)

            for j in range(4):
                materials_copy[j] += robots[j] * wait

            for j in range(3):
                materials_copy[j] -= robot_cost[j]

            robots_copy[n_robot] += 1
            max_mined_geodes = max(max_mined_geodes, calc_best_output(blueprint, Materials(*materials_copy), Materials(*robots_copy), time - wait))

        max_geodes[blueprint.index] = max(max_geodes[blueprint.index], max_mined_geodes)
        return max_mined_geodes;


    @timefunction
    def part1():
        max_geodes[:] = [0] * len(blueprints)

        for blueprint in blueprints:
            calc_best_output(blueprint, starting_materials, starting_robots, 24)

        ics(max_geodes)
        result = sum(m*n for n, m in enumerate(max_geodes, 1))
        print_result(result)



    @timefunction
    def part2():
        use_blueprints = blueprints[:3]
        max_geodes[:] = [0] * len(use_blueprints)

        for blueprint in use_blueprints:
            calc_best_output(blueprint, starting_materials, starting_robots, 32)

        ics(max_geodes)
        result = reduce(operator.mul, max_geodes)
        print_result(result)

    part1()
    part2()

def main():
    if 0: # samples from aocd don't work yet, replaced from hardcoded to put on github
        example = get_aocd_example()
        samp_inps = split_example(example)

        for n, samp_inp in enumerate(samp_inps, 1):
            print(f"{Fore.BLUE}{Style.BRIGHT}Sample {n}:{Style.RESET_ALL}")
            run(samp_inp, False)

    if 1:
        print(f"{Fore.BLUE}{Style.BRIGHT}Actual:{Style.RESET_ALL}")
        real_inp = get_aocd_data()
        run(real_inp, True)

main()
