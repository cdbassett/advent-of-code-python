from functools import *
from collections import *
from itertools import *
from math import *
from statistics import *
from dataclasses import dataclass
from builtins import pow
import numpy as np
from utils.timer_utils import timefunction
from construct import *

from functional import seq
import scipy
from icecream import ic


from utils.aoc_utils import * 
from utils.utilities import *
import utils.seq_extensions # these extend PyFunctional seq objects, don't need to directly use anything in it


# https://adventofcode.com/2021/day/19


rotations = scipy.spatial.transform.Rotation.create_group("O").as_matrix().astype(int)
# ic(rotations)
ic(len(rotations))
print("Generated {} rotation matrices".format(len(rotations)))


ScannerTuple = namedtuple("Scanner", "beacons,by_dist,index")

def scanner_index(s):
    return s.index

def build_by_dist(beacons):
    by_dist = {}

    for p1, p2 in combinations(beacons.T, 2):
        fingerprint = distance_sq(p1, p2)
        by_dist[fingerprint] = tuple(p1), tuple(p2)

    return  by_dist

@dataclass
class ScannerData:
    beacons: [arithtuple]
    by_dist: dict
    index: int
    location: tuple = (0,0,0)


def Scanner(n, beacons):
    beacons = np.array(beacons).T
    by_dist = build_by_dist(beacons)
    return ScannerData(beacons, by_dist, n)

def get_beacons_by_dist(base_scanner, scanner):
    base_pairs = [pair for dist, pair in base_scanner.by_dist.items() if dist in scanner.by_dist]
    base_beacons = np.array(list(set(pair[0] for pair in base_pairs) | set(pair[1] for pair in base_pairs))).transpose()
    return base_beacons

def beacons_tuples(beacons):
    return seq(beacons.T).map(tuple)

def beacons_tuples_sorted(beacons):
    return sorted(seq(beacons.T).map(tuple))

def get_rotation_and_translation(base_beacons, scanner_beacons):
    # each beacon should be in each list, so we should be able to grab any beacon, try a rotation, determine translation between it and one base beacon at a time,
    # then apply that rotation and translation to every other beacon and they will all match
    base_beacons_set = set(beacons_tuples(base_beacons))

    for test_scanner_beacon in scanner_beacons.T:
            # when dealing with an individual point, we have to reshape to be like list of beacons (3, 1)
        test_scanner_beacon = test_scanner_beacon.reshape(3, 1)
    #    ic(test_scanner_beacon)
    #    ic(base_beacons_set)

        for rot in rotations:
    #        ic(rot)
            rotated_test_beacon = (rot @ test_scanner_beacon).reshape(3, 1)
    #        ic(rotated_test_beacon)

            for base_beacon in base_beacons.T:
                base_beacon = base_beacon.reshape(3, 1)
    #            ic(base_beacon)
                translation = base_beacon - rotated_test_beacon
                assert ((rotated_test_beacon + translation) == base_beacon).all()
    #            ic(translation.shape)
    #            ic(translation)
    #            ic(translation.T)
                translated_scanner_beacons = tuple(beacons_tuples(rot @ scanner_beacons + translation))
    #            ic(tuple(base_beacon.T))
    #            ic(tuple((rotated_test_beacon + translation).T))
    #            ic(tuple((rotated_test_beacon + translation)))

                if len(base_beacons_set.intersection(translated_scanner_beacons)) >= 12:
                    return rot, translation

    return None, None
    # assert False, "Couldn't find rotation and translation"


@timefunction
def run(inp, is_real):
    insert_sample_functions(is_real, globals())
    inp = inp.strip().split('\n')
    scanner_chunks = list(split_iterable(inp, ""))
    scanners = [Scanner(n, [tuple(map(int, line.split(","))) for line in scanner_chunk[1:]]) for n, scanner_chunk in enumerate(scanner_chunks)]
#    ics(scanners[:2])
    base_scanners, other_scanners = scanners[0:1], scanners[1:]
    new_base_scanners = base_scanners[:]

    while other_scanners:
        processing_base_scanners = new_base_scanners[:]
        new_base_scanners = []
#        print(f"Processing scanners {[base_scanner.index for base_scanner in processing_base_scanners]} against {}")
        print(f"Processing scanners {seq(processing_base_scanners).map(scanner_index)} against {[seq(other_scanners).map(scanner_index)]}")

        for base_scanner in processing_base_scanners:
            base_scanner_keys = base_scanner.by_dist.keys()
            remaining_other_scanners = []

            for scanner in other_scanners:
                distances = sorted(dist for dist in base_scanner_keys if dist in scanner.by_dist)
                beacon_count = len(distances)

                    # If two scanners detect 12 identical beacons in common, the pairwise Euclidean distances between those 12 beacons (12 × 11 / 2 = 66) will match regardless of the scanners' rotations or orientations.
                if beacon_count >= 66:
                    print(f"    scanner {scanner.index} potentially shares {beacon_count} beacons with {base_scanner.index}")
                    new_base_scanners.append(scanner)
                    base_beacons = get_beacons_by_dist(base_scanner, scanner)
#                    ics(beacons_tuples_sorted(base_beacons))
                    scanner_beacons = get_beacons_by_dist(scanner, base_scanner)
#                    ics(beacons_tuples_sorted(scanner_beacons))
                    R, t = get_rotation_and_translation(base_beacons, scanner_beacons)

                    if R is not None:
    #                    ics(R, t, t.shape)
    #                    ics(tuple(t.T[0]))
                        scanner.beacons = R @ scanner.beacons + t
                        scanner.by_dist = build_by_dist(scanner.beacons)
                        scanner.location = subtract_tuple((0,0,0), t.T[0])
    #                    ics(beacons_tuples_sorted(scanner.beacons))
                    else:   
                        remaining_other_scanners.append(scanner)
                else:
#                    print(f"    scanner {scanner.index} doesn't share beacons with {base_scanner.index}")
                    remaining_other_scanners.append(scanner)

            other_scanners = remaining_other_scanners

    unique_beacons = sorted(sets_union(seq(s.beacons.transpose()).map(tuple) for s in scanners))
#    ics(unique_beacons)

    
    @timefunction
    def part1():
        result = len(unique_beacons)
#        ic(num_beacons)
        len_original_beacons = sum(np.shape(s.beacons)[1] for s in scanners)
        ics(len_original_beacons)
        print_result(result)


    @timefunction
    def part2():
        result = int(max(manhattan(s1.location, s2.location) for s1, s2 in combinations(scanners, 2)))
        print_result(result)


    part1() # 79
    part2() # 3621

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
