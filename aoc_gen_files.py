from functools import *
from collections import *
from collections.abc import Iterable
from itertools import *
from math import *
from statistics import *
from sys import exit
from dataclasses import dataclass, field
import re
from builtins import pow
import operator
from typing import Callable
import copy

from colorama import Fore, Style
from functional import seq # https://github.com/EntilZha/PyFunctional
import iteration_utilities as it_ut # https://pypi.org/project/iteration-utilities/
from icecream import ic

from timer_utils import timefunction
from aoc_utils import * # this includes adding c:\ut to sys.path
from Utilities import *
import seq_extensions # these extend PyFunctional seq objects, don't need to directly use anything in it

import shutil


@timefunction
def run(inp1, inp2, is_real):
    insert_sample_functions(is_real, globals())

    def data_parse(inp):
        lines = inp.strip().split('\n')

#        parts = list(batched((list(c) for match, c in itertools.groupby(lines, str.isdigit)), 2))
        parts = seq(lines).groupby(str.isdigit).map(second_elem).grouped(2)
        ics(parts)
#        parsed = map_list(partial(str.split, sep=")"), lines)
        return parts


    def process1(parsed):
        for [year], days in parsed:
            for line in days:
                day, text = line.split(" - ")
#                nday = string_to_integers(day)[0]
                nday = day.split("_")[1]
                text = text.replace("-", "_").replace(",", "_").replace(".", "_").replace("?", "").replace("'", "").replace("__", "_")
                text = "_".join(piece for piece in text.split("_") if not piece.isdigit())
                fname = f"aoc_{year}_{nday.zfill(2)}_{text}.py"
                exists = os.path.exists(fname)
#                ics(fname, exists)

                if not exists:
                    ics(fname)
                    shutil.copyfile("aoc_base.py", fname)


        return 0

    @timefunction
    def part1(inp):
        parsed = data_parse(inp)
#        ics(parsed)
        result = process1(parsed)
        print_result(result)


    part1(inp1)

def main():
    print_preface(False)
    run(samp_inp1, samp_inp2, False)




samp_inp1 = r"""
2019
day_1 - the_tyranny_of_the_rocket_equation
day_2 - 1202_program_alarm
day_3 - crossed_wires
day_4 - secure_container
day_5 - sunny_with_a_chance_of_asteroids
day_6 - universal_orbit_map
day_7 - amplification_circuit
day_8 - space_image_format
day_9 - sensor_boost
day_10 - monitoring_station
day_11 - space_police
day_12 - the_n-body_problem
day_13 - care_package
day_14 - space_stoichiometry
day_15 - oxygen_system
day_16 - flawed_frequency_transmission
day_17 - set_and_forget
day_18 - many-worlds_interpretation
day_19 - tractor_beam
day_20 - donut_maze
day_21 - springdroid_adventure
day_22 - slam_shuffle
day_23 - category_six
day_24 - planet_of_discord
day_25 - cryostasis
2018
day_1 - chronal_calibration
day_2 - inventory_management_system
day_3 - no_matter_how_you_slice_it
day_4 - repose_record
day_5 - alchemical_reduction
day_6 - chronal_coordinates
day_7 - the_sum_of_its_parts
day_8 - memory_maneuver
day_9 - marble_mania
day_10 - the_stars_align
day_11 - chronal_charge
day_12 - subterranean_sustainability
day_13 - mine_cart_madness
day_14 - chocolate_charts
day_15 - beverage_bandits
day_16 - chronal_classification
day_17 - reservoir_research
day_18 - settlers_of_the_north_pole
day_19 - go_with_the_flow
day_20 - a_regular_map
day_21 - chronal_conversion
day_22 - mode_maze
day_23 - experimental_emergency_teleportation
2017
day_1 - inverse_captcha
day_2 - corruption_checksum
day_3 - spiral_memory
day_4 - high-entropy_passphrases
day_5 - a_maze_of_twisty_trampolines,_all_alike
day_6 - memory_reallocation
day_7 - recursive_circus
day_8 - i_heard_you_like_registers
day_9 - stream_processing
day_10 - knot_hash
day_11 - hex_ed
day_12 - digital_plumber
day_13 - packet_scanners
day_14 - disk_defragmentation
day_15 - dueling_generators
day_16 - permutation_promenade
day_17 - spinlock
day_18 - duet
day_19 - a_series_of_tubes
day_20 - particle_swarm
day_21 - fractal_art
day_22 - sporifica_virus
day_23 - coprocessor_conflagration
day_24 - electromagnetic_moat
day_25 - the_halting_problem
2016
day_1 - no_time_for_a_taxicab
day_2 - bathroom_security
day_3 - squares_with_three_sides
day_4 - security_through_obscurity
day_5 - how_about_a_nice_game_of_chess?
day_6 - signals_and_noise
day_7 - internet_protocol_version_7
day_8 - two-factor_authentication
day_9 - explosives_in_cyberspace
day_10 - balance_bots
day_12 - leonardo's_monorail
day_13 - a_maze_of_twisty_little_cubicles
day_14 - one-time_pad
day_16 - dragon_checksum
day_25 - clock_signal
2015
day_1 - not_quite_lisp
day_2 - i_was_told_there_would_be_no_math
day_3 - perfectly_spherical_houses_in_a_vacuum
day_4 - the_ideal_stocking_stuffer
day_5 - doesn't_he_have_intern-elves_for_this?
day_6 - probably_a_fire_hazard
day_7 - some_assembly_required
day_8 - matchsticks
day_9 - all_in_a_single_night
day_10 - elves_look,_elves_say
day_11 - corporate_policy
day_12 - jsabacusframework.io
day_13 - knights_of_the_dinner_table
day_14 - reindeer_olympics
day_15 - science_for_hungry_people
day_16 - aunt_sue
day_17 - no_such_thing_as_too_much
day_18 - like_a_gif_for_your_yard
day_19 - medicine_for_rudolph
day_20 - infinite_elves_and_infinite_houses
day_25 - let_it_snow"""

samp_inp2 = samp_inp1

samp_inps = """
""".strip().split("\n")

samp_inps = [
    ]

main()

