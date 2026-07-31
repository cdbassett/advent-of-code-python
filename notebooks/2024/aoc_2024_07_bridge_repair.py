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
import os
import sys
from collections import *
from math import log10

from icecream import ic

# %autoreload explicit
# import and reload these automatically
# %aimport aoc_utils, Utilities, iter_utils, seq_extensions, func_utils
from aoc_utils import * # this includes adding c:\ut to sys.path
from Utilities import *
from iter_utils import *
import seq_extensions # when running standalone, apparently need this import explicitly in main module

# %% [markdown]
# # Sample Data

# %%
if "example" not in dir() or not example:
    example = get_aocd_example()

# %%
sample_data1s = split_example(example)
sample_data1 = sample_data1s[0]
sample_data2 = sample_data1


# %% [markdown]
# # Parse

# %%
def parse_data(inp):
    return string_to_integers_list(inp)


# %% [markdown]
# # Process

# %%
# this reduced runtime from 1:30 to 30
@cache
def build_ops(operators, cnt):
    return tuple(product(*repeat(operators, cnt - 1)))
    
def possible(operators, line):
    #ics(list(product(*repeat(operators, len(line) - 1))))
    total, first, second, *rest = line
    #assert all(n > 0 for n in line) # verified that all numbers are positive

    for ops in build_ops(operators, len(line) - 1):
        first_op = ops[0]
        chk = first_op(first, second)
        #last_op = ops[-1]

        for val, op in zip(rest, ops[1:]):
            if chk > total: # this seems to improve time but marginally
                break
                
            chk = op(chk, val)

        if chk == total:
            return total
    
    return 0

def process(parsed):
    ics(parsed)
    operators = (int.__add__, int.__mul__)
    return seq(parsed).map(partial(possible, operators)).sum()


# %%
# rewrote based on my understanding of anohter solution, time went down to 150ms for both together
def is_possible(total, values, include_concat=False):
    *rest, last = values
    #ics(total, values, rest, last)

    if not rest:
        return last == total
        
    quot, rem = divmod(total, last)

    if rem == 0:
        if is_possible(quot, rest, include_concat):
            return True

    if include_concat:
        assert total >= 0
        last_digits = count_integer_digits(last)
        #digits = count_integer_digits(total)
        str_total = str(total)
        #ics(str_total, last, last, str_total.endswith(str(last)), int(str_total[:-last_digits]))
        
        if str_total.endswith(str(last)):
            preceding = str_total[:-last_digits]
            
            if preceding and is_possible(int(preceding), rest, True):
                return True
        
        #a * 10**num_digits + b
    
    return total > last and is_possible(total-last, rest, include_concat)

def process(parsed):
    ics(parsed)
    #ics(is_possible(parsed[0][0], parsed[0][1:]))
    #ics(sum(total for total, *values in parsed))
    combined_total = sum(total for total, *values in parsed if is_possible(total, values))
    return combined_total


# %%
def part1(inp):
    parsed = parse_data(inp)
    result = process(parsed)
    print_result(result)


# %% [markdown]
# # Process2

# %%
def concatenation(a, b):
    #num_digits = int(math.log10(b)) + 1
    #ics(a, b, num_digits, 10**num_digits, a * 10**num_digits + b, int(str(a) + str(b)))
    #return a * 10**num_digits + b
    return int(str(a) + str(b))

def process2(parsed):
    #operators = (int.__add__, int.__mul__, concatenation)
    #return seq(parsed).map(partial(possible, operators)).sum()
    combined_total = sum(total for total, *values in parsed if is_possible(total, values, True))
    return combined_total


# %%
def part2(inp):
    parsed = parse_data(inp)
    result = process2(parsed)
    print_result(result)


# %% [markdown]
# # Sample data processing

# %%
insert_sample_functions(False, globals())

for sample_data1 in sample_data1s:
    part1(sample_data1)

part2(sample_data2)

# %% [markdown]
# # Actual data

# %% editable=true slideshow={"slide_type": ""}
real_inp = get_aocd_data()
insert_sample_functions(True, globals())
part1(real_inp)
part2(real_inp) # 91377448644679


# %% [markdown]
# # Others' solutions

# %%
# these are not because I had problems, purely for performanece improvements - and there are some doozies here

# %%
# https://old.reddit.com/r/adventofcode/comments/1h8l3z5/2024_day_7_solutions/m0tw1bf/
def aoc07():
    L = [x.split(": ") for x in get_aocd_data().split("\n")]
    M = [(int(s), [int(x) for x in e.split()]) for (s,e) in L]
    find = lambda t, L, ops: L[0] == t if len(L) == 1 else any(find(t, [f(L[0], L[1])] + L[2:], ops) for f in ops)
    print(sum(t for (t,L) in M if find(t, L, ops := [int.__add__, int.__mul__])))
    print(sum(t for (t,L) in M if find(t, L, ops + [lambda x, y: int(str(x)+str(y))])))

aoc07()

# %%
# https://old.reddit.com/r/adventofcode/comments/1h8l3z5/2024_day_7_solutions/m0tv6di/
# this one is less than a 10th ofa second compared to my 30 seconds
"""
The key realization is to work through the list of numbers in reverse, and checking whether each operator can possibly yield the test value with the last number in the list, n and some unknown precursor value. For instance, a concatenation can only return test_value if the last digits of the test value are equal to n, and multiplication can only return test_value if it is divisible by n. There are no restrictions on addition, so that ends up being a fallback case.
If an operation can return the test value, we recursively do the same check, swapping out test_value for the precursor value, and removing n from the list of numbers.
"""
from math import log10

def concat(a, b):
    return int(f"{a}{b}")

def digits(n):
    return int(log10(n)) + 1

def endswith(a, b):
    return (a - b) % 10 ** digits(b) == 0

def is_tractable(test_value, numbers, check_concat=True):
    *head, n = numbers
    
    if not head:
        return n == test_value
        
    q, r = divmod(test_value, n)
    
    if r == 0 and is_tractable(q, head, check_concat):
        return True
        
    if check_concat and endswith(test_value, n) and is_tractable(test_value // (10 ** digits(n)), head, check_concat):
        return True
        
    return is_tractable(test_value - n, head, check_concat)

def solve(data):
    ans1 = ans2 = 0
    
    for line in data:
        test_value, *numbers = line
        
        if is_tractable(test_value, numbers, False):
            ans1 += test_value
            ans2 += test_value
        elif is_tractable(test_value, numbers):
            ans2 += test_value
            
    return ans1, ans2

solve(parse_data(get_aocd_data()))

# %%
# https://github.com/James-Ansley/adventofcode/blob/main/2024/day07.py
import re
from operator import add, mul

def run(equations, ops):
    result = 0
    for target, first, *rest in equations:
        queue = [first]
        for value in rest:
            queue = [
                op(total, value)
                for total in queue
                for op in ops
                if total <= target
            ]
        if target in queue:
            result += target
    return result


data = [re.findall(r"(\d+)", line) for line in get_aocd_data().splitlines()]
data = [[int(e) for e in line] for line in data]

concat = lambda e1, e2: int(str(e1) + str(e2))

print(run(data, (add, mul)))
print(run(data, (add, mul, concat)))


# %%
# https://old.reddit.com/r/adventofcode/comments/1h8l3z5/2024_day_7_solutions/m0tv0y2/
def operate(nums, part2 = True):
    if len(nums) == 1:
        yield nums[0]
        return
    for result in operate(nums[:-1]):
        yield result + nums[-1]
        yield result * nums[-1]
        if part2:
            yield int(str(result)+str(nums[-1]))

total = 0

for x, *nums in parse_data(get_aocd_data()):
    for result in operate(nums):
        if x == result:
            total += x
            break

print(total)
