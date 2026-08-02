from functools import *
from collections import *
from itertools import *
from math import *
from statistics import *
from builtins import pow
import pyperclip
from icecream import ic
import shapely
import shapely.ops
from utils.timer_utils import timefunction
import networkx as nx
import matplotlib.pyplot as plt
from construct import *

from utils.aoc_utils import * # this includes adding c:\ut to sys.path
from utils.utilities import *
import utils.seq_extensions # these extend PyFunctional seq objects, don't need to directly use anything in it


# https://adventofcode.com/2022/day/16


Valve = namedtuple("Valve", "key,rate,conns")

def to_num(a):
    return int(a.split("=")[1].rstrip(":,"))

def run(inp, is_real):
    insert_sample_functions(is_real, globals())
    print_preface(is_real)
    inp = inp.strip().split('\n')
    valves = [Valve((p := line.split())[1], int(p[4].split("=")[1][:-1]), "".join(p[9:]).split(",")) for line in inp]
    ics(valves)
    valves_by_key = dict((v.key, v) for v in valves)
    start = valves_by_key["AA"]
    rate_valves = [v for v in valves if v.rate]
    valves_with_rates = set(v.key for v in valves if v.rate)
    ics(valves_with_rates)
    valves_by_key = dict((v.key, v) for v in valves)
    ic(len(rate_valves))
#    ics(it_ut.count_items(permutations(rate_valves)))
    ic(factorial(len(rate_valves)))

    g = nx.DiGraph()
    # a dictionary of dictionaries with path[source][target]=[list of nodes in path].

    for valve in valves:
        for conn in valve.conns:
           g.add_edge(valve.key, conn)

    paths  = nx.shortest_path(g)
    paths = dict(paths)
    needed_paths = dict((start_key, dict((target_key, path) for target_key, path in paths_dict.items() if target_key in valves_with_rates and target_key != start_key)) for start_key, paths_dict in paths.items() if start_key=="AA" or start_key in valves_with_rates)
    ics(needed_paths)


    def first_rate(valve_key):
        dest_valve = valves_by_key[valve_key]
        min_lengths = [len(path) for key, path in needed_paths[dest_valve.key].items()]
        ics(valve_key, min_lengths)
        min_length = min(len(path) for key, path in needed_paths[dest_valve.key].items())
        ics(valve_key, min_length)
        return (30 - len(paths["AA"][valve_key])) * dest_valve.rate -  min_length

#    for valve in sorted(rate_valves, key = lambda v: v.rate):
#        print(f"{valve.key}: {first_rate(valve.key)}")

    """
        for each path, need to track which valves already visited
        no point in turning on valve with no flow, but could be shortest route to another
        brute force:
            calculate distance between all valves with rate (and AA)
            actual data would result 131 billion combos
        time_to_travel
        maybe shortest_path with costs being rate of all others?
            probably not, costs changes through traversal?
    """

    @cache
    def max_flow(cur_key, opened, min_left):
        if min_left <= 0:
            return 0

        best = 0
        valve = valves_by_key[cur_key]

        if cur_key in opened:
            for conn_valve in valve.conns:
                best = max(best, max_flow(conn_valve, opened, min_left - 1))
        else:
            cur_flow_total = (min_left - 1) * valve.rate
            cur_opened = tuple(sorted(opened + (cur_key,)))

            for conn_valve in valve.conns:
                if cur_flow_total:
                    best = max(best, cur_flow_total + max_flow(conn_valve, cur_opened, min_left - 2))

                best = max(best, max_flow(conn_valve, opened, min_left - 1))

        return best


    def part1():
        result = max_flow("AA", (), 30)
        print_result(result)



    def part2():
        distances = dict(((a.key, b.key), len(needed_paths[a.key][b.key])-1) for a, b in product(rate_valves + [start], rate_valves) if a != b)
#        adj = dict((a.key, [b.key for b in rate_valves if a != b]) for a in rate_valves + [start] )
        cost_and_adj = defaultdict(list)

        keep = ['OT', 'IS', 'WI', 'QQ', 'ZL', 'OM', 'NG', 'AA', 'YW', 'DG', 'MX', 'HV', 'GB', 'IC', 'VX', 'FM']

        for a, b in product(rate_valves + [start], rate_valves):
            if a != b:
                cost_and_adj[a.key].append((distances[a.key, b.key], b.key))


        # paths where we activate each stop
        def get_paths(cur_key, min_left, exclude=None):
            if exclude is None:
                exclude = set()

            if min_left >= 1:
                yield (cur_key,)

            source_paths = paths[cur_key]

            for cost, conn_valve in cost_and_adj[cur_key]:
                if conn_valve in exclude:
                    continue

                if min_left >= cost + 2:
                    for path in get_paths(conn_valve, min_left - cost - 1, exclude | {cur_key}):
                        yield (cur_key,) + path

        @cache
        def value(path, time, debug = False):
            result = 0

            for a, b in zip(path, path[1:]):
                # walk from a to b
                # open valve b
#                time -= dist2[a,b]
#                time -= len(paths[a][b])
                dist = distances[a, b]
                time -= dist
                time -= 1
                rate = valves_by_key[b].rate
                result += time * rate

                if debug:
                    ics((a,b), dist, time, rate, time * rate )

            return result#, time

        best_value = 0
        ctr = 0
#        ics(value(('AA', 'JJ', 'BB', 'CC'), 26, True))
#        ics(value(('AA', 'DD', 'HH', 'EE'), 26, True))
#        ics(value(('AA', 'DD', 'EE', 'HH'), 26, True))
#        ics(value(('AA', 'DD', 'EE', 'HH'), 26) + value(('AA', 'JJ', 'BB', 'CC'), 26))
        best_paths = ((), ())

        for i, path1 in enumerate(get_paths("AA", 26, set())):
            if i % 100 == 0:
                print(i)

            p1v = value(path1, 26)

            for path2 in get_paths("AA", 26, exclude=set(path1)):
                ctr += 1
                p2v = value(path2, 26)
                new_value = p1v + p2v

                if new_value > best_value:
                    best_value = new_value
                    best_paths = path1, path2

#                best_value = max(best_value, p1v + p2v)

        ics(ctr)
        ics(best_paths)
        result = best_value
        print_result(result)

    part1()
    part2()

def main():
    if 1: # samples from aocd don't work yet, replaced from hardcoded to put on github
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
