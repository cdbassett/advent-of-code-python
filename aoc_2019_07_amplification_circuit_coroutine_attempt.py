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
from aoc_2019_intcode import process_intcodes, parse_intcodes

from aoc_utils import * # this includes adding c:\ut to sys.path
from Utilities import *
import seq_extensions # these extend PyFunctional seq objects, don't need to directly use anything in it
from quicklambda import _1, _2

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
        real_inp = get_aocd_data()
        run(real_inp, real_inp, True)
#        aocd.submit(my_answer)




samp_inp1 = r"""
3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0
"""

samp_inp2 = """
3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5
"""



samp_inps = """
3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0
3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0
3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0
""".strip().split("\n")
samp_inps=[]



main()


