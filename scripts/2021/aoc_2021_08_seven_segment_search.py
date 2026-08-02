from functools import *
from collections import *
from itertools import *
from math import *
from statistics import *
from builtins import pow
import pyperclip
from icecream import ic
import iteration_utilities as it_ut

from utils.aoc_utils import * # this includes adding c:\ut to sys.path
from utils.utilities import *
import utils.seq_extensions # these extend PyFunctional seq objects, don't need to directly use anything in it


# https://adventofcode.com/2021/day/8


segments = "abcdefg"

lcd_number_segments = [
    "abcefg", # 0
    "cf", # 1
    "acdeg", # 2
    "acdfg", # 3
    "bcdf", # 4
    "abdfg", # 5
    "abdefg", # 6
    "acf", # 7
    "abcdefg", # 8
    "abcdfg", # 9
    ]

lcd_lengths = list(map(len, lcd_number_segments))

lengths_to_number = defaultdict(list) # length of lcd_number_segments -> list of numbers with that length number
segment_to_number = defaultdict(list) # letter of segment -> list of numbers with that segment
real_patterns_to_number = dict()

for n, lcd_number_segment in enumerate(lcd_number_segments):
    real_patterns_to_number[lcd_number_segment] = n
    lengths_to_number[len(lcd_number_segment)].append(n)

    for letter in lcd_number_segment:
        segment_to_number[letter].append(n)


def sorted_pattern(pat):
    return "".join(sorted(pat))

def run(inp, is_real):
    ics = nothing if is_real else ic
    print_result = partial(print_result_aoc, is_real)

    inp = inp.strip().split('\n')
    entries = list(line.split("|") for line in inp)
#    print_sample_list("entries", entries)
#    print_sample_list("zip(*entries)", list(zip(*entries)))
    patterns, outputs = zip(*entries)
    outputs = [output.split() for output in outputs]
    patterns = [pattern.split() for pattern in patterns]
#    print_sample_list("patterns", patterns)
#    print_sample_list("outputs", outputs)
#    ics(lcd_number_segments)
#    ics(lengths_to_number)
#    ics(segment_to_number)
#    sorted_segment_to_number = sorted(segment_to_number.items(), key=lambda x: len(x[1]))
#    ics(sorted_segment_to_number)

    def part1():
        output_lengths = Counter(map(len, it_ut.flatten(outputs)))
        checked_counts = [output_lengths.get(n) for n in (2, 3, 4, 7)] # 1, 7, 4, 8
        checked_counts = filter(None, checked_counts)
        result = sum(checked_counts)
        print_result(result)

    def part2():
        def mapping_diff():
            pass

        def set_found(scrambled_letter, actual):
#            ics(scrambled_letter, actual)
            actual_to_scrambled_segments[actual] = scrambled_letter
            found_segments[scrambled_letter] = actual
            possibles[scrambled_letter] = { actual }

            for letter, possible_set in possibles.items():
                if letter != scrambled_letter:
                    possible_set.discard(actual)

        def set_found_by_number_length(letter, length):
            found_scrambled_letter = first(letter for letter, numbers in scrambled_letter_mapping.items() if len(numbers) == length)
            set_found(found_scrambled_letter, letter)

        def set_found_by_pattern_length(number, length):
            assert len(length_mapping[length]) == 1
            scrambled_pattern = length_mapping[length][0]
            found_patterns["".join(sorted(scrambled_pattern))] = number

        output_values = []

        for line_patterns, line_outputs in zip(patterns, outputs):
#            ics(line_patterns)
            length_mapping = defaultdict(list) # length of scrambled pattern -> list of sets of scrambled patterns with that length
            scrambled_letter_mapping = defaultdict(list) # scrambled letter -> list of scrambled patterns with that letter
            found_segments = {} # scrambled letter -> actual letter
            found_patterns = {} # scrambled pattern -> correct number segment
            actual_to_scrambled_segments = {}
                # remaining possible choices for each segment
            possibles = dict((letter, set(segments)) for letter in segments)  # scrambled letter -> set of possible actual letter choices for each segment
#            orig_possibles = copy.deepcopy(possibles)

            for n, pattern in enumerate(line_patterns):
                length_mapping[len(pattern)].append(set(pattern))

                for letter in pattern:
                    scrambled_letter_mapping[letter].append(n)

            set_found_by_pattern_length(1, 2) # 1, cf
            set_found_by_pattern_length(7, 3) # 7, acf
            set_found_by_pattern_length(8, 7) # 8, abcdefg
            set_found_by_pattern_length(4, 4) # 4, bcdf

#            ics(scrambled_letter_mapping)
#            ics(it_ut.first(letter for letter, numbers in scrambled_letter_mapping.items() if len(numbers) == 4))

#            ics(length_mapping)
#            print_sample_list("7", length_mapping[3])
#            print_sample_list("1", length_mapping[2])
#            print_sample_list("7-1", length_mapping[3][0] - length_mapping[2][0])

                # 7 has a, 1 does not
            found_a = first(length_mapping[3][0] - length_mapping[2][0])
            set_found(found_a, "a")
                # f is in every number but 2
                # should be able to find srmabnled letter for f and which is 2?
#            found_f =

                # e is the only segment used in exactly 4 numbers
            set_found_by_number_length("e", 4)

                # f is the only segment used in exactly 9 numbers
            set_found_by_number_length("f", 9)

                # b is the only segment used in exactly 6 numbers
            set_found_by_number_length("b", 6)

                # 1 has cf, and we know f
#            found_c = it_ut.first(length_mapping[2][0] - { "f" })
            found_c = first(length_mapping[2][0] - set(actual_to_scrambled_segments["f"]))
            set_found(found_c, "c")

                # 4 has bcdf, we know all but d
            found_d = first(length_mapping[4][0] - set(actual_to_scrambled_segments[l] for l in "bcf"))
            set_found(found_d, "d")

#            ics(possibles)
#            ics(found_patterns)
#            ics(actual_to_scrambled_segments)

            found_segments = dict((letter, first(possible)) for letter, possible in possibles.items())
#            ics(found_segments)

#            found_patterns = dict((it_ut.first(possible)) for letter, possible in possibles.items())
            found_patterns = {}

            for pattern in line_patterns:
#                ics(pattern)
                real_pattern = sorted_pattern(found_segments[l] for l in pattern)
#                ics(real_pattern)
                pat_num = real_patterns_to_number[real_pattern]
                found_patterns[sorted_pattern(pattern)] = pat_num

#            ics(found_patterns)

            output_value = 0

            for output in line_outputs:
#                ics(output)
                cur_val = found_patterns[sorted_pattern(output)]
                output_value = output_value * 10 + cur_val


            output_values.append(output_value)


#        while any(len(possible_set)>1 for possible_set in possibles.values()):



        result = sum(output_values)
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
