from functools import *
from collections import *
from itertools import *
from math import *
from statistics import *
from builtins import pow
from utils.timer_utils import timefunction


from colorama import Fore, Style
from functional import seq # https://github.com/EntilZha/PyFunctional
import iteration_utilities as it_ut # https://pypi.org/project/iteration-utilities/
import pyperclip
from icecream import ic
from utils.aoc_2019_intcode import process_intcodes, parse_intcodes

from utils.aoc_utils import * # this includes adding c:\ut to sys.path
from utils.utilities import *
import utils.seq_extensions # these extend PyFunctional seq objects, don't need to directly use anything in it
from utils.quicklambda import _1, _2

# doesn't seem to work with generators because each call to send returns the next yield value,
# and we need to send two values (phase and input) before outputting anything
# got it working by queueing inputs that we receive when outputting


@timefunction
def run(inp1, inp2, is_real):
    insert_sample_functions(is_real, globals())

    def data_parse(inp):
        return parse_intcodes(inp)

    def mem_repr(memory):
#        ics(memory.keys())
        min_key = min(memory.keys())
        max_key = max(memory.keys())
        return [memory[n] for n in range(min_key,max_key+1)]


    def process1(parsed, phases):
        best_signal = 0

        for combo in permutations(phases):
#            ics(combo)
#            input = 0

            if 1:
#                generators = [process_intcodes(parsed) for _ in combo]
                generators = []

                for n, phase in enumerate(combo):
                    generator = process_intcodes(parsed, n)
                    generators.append(generator)
                    generator.send(None) # start it
                    generator.send(phase)

                value = 0

                try:
                    for step in count():
#                        ics(step)

                            # taking value from one coroutine and sending it to the next in line, due to outer loop will also send last to first
                        for id, g in enumerate(generators):
                            got_value = None

                                # getting None indicates generator was requesting input rather than sending output
                            while got_value is None:
                                got_value = g.send(value)

                            value = got_value
                except StopIteration:
#                    ics("stopped", combo, step)
                    pass
                except GeneratorExit:
#                    ics("exited", combo, step)
                    pass

            else:
                iterator = [0]

                for n in combo:
                    iterator = process_intcodes(parsed, prepend(n, iterator))
#                value = next(process_intcodes(parsed, (n, value)))

                input = next(iterator)

#            ics(combo, value)
            best_signal = max(best_signal, value)
#            break

        return best_signal

    @timefunction
    def part1(inp):
        parsed = data_parse(inp)
#        ics(parsed)
        result = process1(parsed, range(5))
        print_result(result)

    process2 = process1

    @timefunction
    def part2(inp):
        parsed = data_parse(inp)
#        ics(parsed)
        result = process2(parsed, range(5, 10))
        print_result(result)


    part1(inp1)
    part2(inp2)

def main():
    example = get_aocd_example()
    samp_inps = split_example(example)

    for n, samp_inp in enumerate(samp_inps, 1):
        print(f"{Fore.BLUE}{Style.BRIGHT}Sample {n}:{Style.RESET_ALL}")
        run(samp_inp, samp_inp, False)

    if 1:
        print(f"{Fore.BLUE}{Style.BRIGHT}Actual:{Style.RESET_ALL}")
        # needs env var AOC_SESSION
        real_inp = get_aocd_data()
        run(real_inp, real_inp, True)
#        aocd.submit(my_answer)


main()


