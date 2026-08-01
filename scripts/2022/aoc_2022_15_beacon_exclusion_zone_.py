from functools import *
from collections import *
from itertools import *
from math import *
from statistics import *
from builtins import pow
import pyperclip
from icecream import ic
import iteration_utilities as it_ut
import shapely
import shapely.ops
from utils.timer_utils import timefunction
import matplotlib.pyplot as plt

from utils.aoc_utils import * # this includes adding c:\ut to sys.path
from utils.utilities import *
import utils.seq_extensions # these extend PyFunctional seq objects, don't need to directly use anything in it

Point = Point2D

def to_num(a):
    return int(a.split("=")[1].rstrip(":,"))


def run(inp, is_real):
    insert_sample_functions(is_real, globals())
    print_preface(is_real)
    inp = inp.strip().split('\n')

    parts = [tuple(it_ut.getitem(line.split(), (2,3,8,9))) for line in inp]
    ics(parts)
    sensor_beacons = [(Point(to_num(p[0]), to_num(p[1])), Point(to_num(p[2]), to_num(p[3]))) for p in parts]
    ics(sensor_beacons)
#    paths = [[Point(*map(int, pair.split(","))) for pair in line.split(" -> ")] for line in inp]

    min_x = min(beacon.x for sensor, beacon in sensor_beacons)
    min_y = min(beacon.y for sensor, beacon in sensor_beacons)
    max_x = max(beacon.x for sensor, beacon in sensor_beacons)
    max_y = max(beacon.y for sensor, beacon in sensor_beacons)
    ic(min_x, max_x, max_x-min_x)
    ic(min_y, max_y, max_y-min_y)

    # determine all points at that distance from the sensor

    sensor_beacon_distances = [(sensor, beacon, manhattan(sensor, beacon)) for sensor, beacon in sensor_beacons]

    def part1():

        check_y = 2000000 if is_real else 10
        row = [0] * (max_x - min_x + 1)

#        positions = [manh_dist(sensor, beacon) <
        for x in range(min_x, max_x+1):
            x_point = Point(x, check_y)
            skip = False

            for sensor, beacon, dist in sensor_beacon_distances:
                if beacon == x_point:
                    skip = True

            if not skip:
                for sensor, beacon, dist in sensor_beacon_distances:
                    if manhattan(sensor, x_point) <= dist:
                        row[x - min_x] = 1
                        break

        ics(row)



#        for sensor, beacon in sensor_beacons:
#            dist = manh_dist(sensor, beacon)


        result = sum(row)
        print_result(result)

        # works but takes too much memory (16 trillion elements)
    def part2():
        max_mag = 4000000 if is_real else 20
#        hits = [[0] * (max_mag +1) for n in range(max_mag + 1)]
#        hits = np.zeros([max_mag+1, max_mag+1], dtype=np.int8)

        for sensor, beacon, dist in sensor_beacon_distances:
            for y in range(max(0, sensor.y - dist), min(sensor.y + dist, max_mag) + 1):
                hit_row = hits[y]
                mag_y = abs(y - sensor.y)

                for x in range(max(0, sensor.x - dist + mag_y), min(sensor.x + dist - mag_y, max_mag) + 1):
                    hit_row[x] = 1

            hits[sensor.y][sensor.x] = 9

        ics(hits)
        vis_hits = set(Point(x, y) for y, line in enumerate(hits) for x, h in enumerate(line) if h)
#        ics(vis_hits)
        ics(get_vis_map(vis_hits))
        holes = [Point(x, y) for y, line in enumerate(hits) for x, h in enumerate(line) if not h]
        assert len(holes) == 1
        hole = holes[0]
        result = hole.x * 4000000 + hole.y
        print_result(result)


    def part2():
        max_mag = (4000000 if is_real else 20) + 1
#        hits = [[0] * (max_mag +1) for n in range(max_mag + 1)]
#        hits = np.zeros([max_mag+1, max_mag+1], dtype=np.int8)
#        polygons = []
#        bounding = shapely.Polygon([(0,0), (max_mag, 0), (max_mag, max_mag), (0, max_mag)])
#
#        for sensor, beacon, dist in sensor_beacon_distances:
#            polygons.append(shapely.Polygon([(sensor.x + dist, sensor.y), (sensor.x, sensor.y + dist), (sensor.x - dist, sensor.y), (sensor.x, sensor.y - dist)]))
#
#        merged = shapely.ops.unary_union(polygons)
#        intersection = bounding.intersection(merged)
#        ics(intersection.boundary)
        discs = [(sensor.x, sensor.y, dist) for sensor, beacon, dist in sensor_beacon_distances]

        def get_boundary(x, y, r):
            temp = (x, y+r)
            while temp != (x+r, y):
                temp = (temp[0]+1, temp[1]-1)
                yield temp
            while temp != (x, y-r):
                temp = (temp[0]-1, temp[1]-1)
                yield temp
            while temp != (x-r, y):
                temp = (temp[0]-1, temp[1]+1)
                yield temp
            while temp != (x, y+r):
                temp = (temp[0]+1, temp[1]+1)
                yield temp

        for x, y, r in discs:
            print("disc {} {} {}".format(x, y, r))

            for px, py in get_boundary(x, y, r+1):
                if 0 <= px < max_mag and 0 <= py < max_mag:
                    for dx, dy, dr in discs:
                        if (abs(px-dx) + abs(py-dy)) <= dr:
                            break
                    else:
                        print("beacon:", px, py)
                        print("tuning freq:", 4000000 * px + py)
                        return
                        break



        return
        ics(hits)
        vis_hits = set(Point(x, y) for y, line in enumerate(hits) for x, h in enumerate(line) if h)
#        ics(vis_hits)
        ics(get_vis_map(vis_hits))
        holes = [Point(x, y) for y, line in enumerate(hits) for x, h in enumerate(line) if not h]
        assert len(holes) == 1
        hole = holes[0]
        result = hole.x * 4000000 + hole.y
        print_result(result)

    part1()
    part2()

def main():
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
