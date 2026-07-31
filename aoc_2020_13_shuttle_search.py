from functools import *
from collections import *
#from sympy import *
from itertools import *
from math import *
from statistics import *
from builtins import pow
import operator
from timer_utils import timefunction

from functional import seq # https://github.com/EntilZha/PyFunctional
import iteration_utilities as it_ut # https://pypi.org/project/iteration-utilities/
from icecream import ic

from aoc_utils import * # this includes adding c:\ut to sys.path
from Utilities import *
import seq_extensions # these extend PyFunctional seq objects, don't need to directly use anything in it
#from fz import _1
from quicklambda import _1


@timefunction
def run(inp, is_real):
    insert_sample_functions(is_real, globals())

    lines = inp.strip().split('\n')
#    lines = inp.strip("\n").split('\n')
    ic(len(lines))
#    w = width(lines)
#    h = height(lines)
#    ic(w, h)
#    ics(inp)


    @timefunction
    def part1():
        timestamp = int(lines[0])
        bus_ids = seq(lines[1].split(",")).filter(_1 != "x").map(int)
        ics(bus_ids)
#        ics(bus_ids.combinations(2).starmap(math.gcd))
        next_departures = bus_ids.map(lambda n: timestamp + (n - timestamp % n))
        stop_timestamp, bus_id = next_departures.zip(bus_ids).min()
        ics(stop_timestamp, bus_id)
#        ics(bus_ids.zip(next_departures))
        result = (stop_timestamp - timestamp) * bus_id
        print_result(result)


    """
    https://en.wikipedia.org/wiki/Chinese_remainder_theorem
    In mathematics, the Chinese remainder theorem states that if one knows the remainders of the Euclidean division of an integer n by several integers, then one can determine uniquely the remainder of the division of n by the product of these integers, under the condition that the divisors are pairwise coprime (no two divisors share a common factor other than 1).

    For example, if we know that the remainder of n divided by 3 is 2, the remainder of n divided by 5 is 3, and the remainder of n divided by 7 is 2, then without knowing the value of n, we can determine that the remainder of n divided by 105 (the product of 3, 5, and 7) is 23. Importantly, this tells us that if n is a natural number less than 105, then 23 is the only possible value of n.
    https://www.geeksforgeeks.org/implementation-of-chinese-remainder-theorem-inverse-modulo-based-implementation/

    We need to find minimum positive number x such that:

         x % num[0]    =  rem[0],
         x % num[1]    =  rem[1],
         .......................
         x % num[k-1]  =  rem[k-1]

    x =  ( ∑ (rem[i]*pp[i]*inv[i]) ) % prod
       Where 0 <= i <= n-1

    rem[i] is given array of remainders

    prod is product of all given numbers
    prod = num[0] * num[1] * ... * num[k-1]

    pp[i] is product of all divided by num[i]
    pp[i] = prod / num[i]

    inv[i] = Modular Multiplicative Inverse of
             pp[i] with respect to num[i]

    """
    # Returns modulo inverse of a with
    # respect to m using extended
    # Euclid Algorithm. Refer below
    # post for details:
    # https://www.geeksforgeeks.org/
    # multiplicative-inverse-under-modulo-m/
    def inv(a, m) :
        m0 = m
        x0 = 0
        x1 = 1

        if (m == 1) :
            return 0

            # Apply extended Euclid Algorithm
        while (a > 1):
            # q is quotient
            q = a // m
            t = m

            # m is remainder now, process
            # same as euclid's algo
            m = a % m
            a = t
            t = x0
            x0 = x1 - q * x0
            x1 = t

            # Make x1 positive
        if x1 < 0:
            x1 += m0

        return x1

    # k is size of num[] and rem[].
    # Returns the smallest
    # number x such that:
    # x % num[0] = rem[0],
    # x % num[1] = rem[1],
    # ..................
    # x % num[k-2] = rem[k-1]
    # Assumption: Numbers in num[]
    # are pairwise coprime
    # (gcd for every pair is 1)
    def findMinX(num, rem) :
        assert len(num) == len(rem)
        # Compute product of all numbers
        prod = products(num)

        # Initialize result
        result = 0

        # Apply above formula
        for i in range(0,len(num)):
            pp = prod // num[i]
            result += rem[i] * inv(pp, num[i]) * pp


        return result % prod


    @timefunction
    def part2():
        bus_ids = seq(lines[1].replace("x", "-1").split(",")).map(int)
        assert bus_ids.combinations(2).starmap(math.gcd).distinct().to_list() == [1] #necessary condition for chinese remainder theorem to work, all values must have no common factors (relatively prime)
        bus_ids_and_indices = bus_ids.zip_with_index().filter(lambda x: x[0] != -1)
        bus_ids = bus_ids.clamp(0)
        ic(bus_ids_and_indices)
#        bus_ids, modulos = zip(*bus_ids_and_indices)
        modulos = bus_ids_and_indices.starmap(operator.sub)
        result = findMinX(bus_ids.to_list(), modulos.to_list())

        ic(seq(bus_ids).map(lambda num: result % num))
        print_result(result)

    part1()
    part2()

def main():
    if 1:
        for samp_inp in samp_inps:
            print("Sample:")
            run(samp_inp, False)

    if 1:
        print("Actual:")
        real_inp = get_aocd_data()
        run(real_inp, True)
#        aocd.submit(my_answer)




samp_inp = r"""
939
7,13,x,x,59,x,31,19
"""


short_samp = """
"""


samp_inps = [
#    short_samp,
    samp_inp,
"""
939
67,7,59,61
""",
"""
939
67,x,7,59,61
""",
"""
939
67,7,x,59,61
""",
"""
939
1789,37,47,1889
""",
    ]


main()

