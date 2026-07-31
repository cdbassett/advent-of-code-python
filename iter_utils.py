import math
import itertools
import operator
from itertools import *
import collections

from icecream import ic


import iteration_utilities as it_ut # https://pypi.org/project/iteration-utilities/

from iteration_utilities import first, second, third, last, nth, minmax
"""
iteration_utilities.first(iterable[, default, pred, truthy, retpred, retidx])
    This callable is equivalent to nth(0).
iteration_utilities.second(iterable[, default, pred, truthy, retpred, retidx])
    This callable is equivalent to nth(1).
iteration_utilities.third(iterable[, default, pred, truthy, retpred, retidx])
    This callable is equivalent to nth(2).
iteration_utilities.last(iterable[, default, pred, truthy, retpred, retidx])
    This callable is equivalent to nth(-1).


class iteration_utilities.nth(x)
    Class that returns the n-th found value.

Parameters:
    nint
        The index of the wanted item. If negative the last item is searched.
        Note This is the only parameter for __init__. The following parameters have to be specified when calling the instance.
    iterable: iterable
        The iterable for which to determine the nth value.
    default: any type, optional
            If no nth value is found and default is given the default is returned.
    pred: callable, optional
        If given return the nth item for which pred(item) is True.
        Note pred=None is equivalent to pred=bool.
    truthy: bool, optional
        If False search for the nth item for which pred(item) is False. Default is True.
        Note Parameter is ignored if pred is not given.
    retpred: bool, optional
        If given return pred(item) instead of item. Default is False.
        Note Parameter is ignored if pred is not given.
    retidx: bool, optional
        If given return the index of the n-th element instead of the value. Default is False.
Returns:
    nth: any type
    The last value or the nth value for which pred is True. If there is no such value then default is returned.
Raises:
    TypeError If there is no nth element and no default is given.

iteration_utilities.minmax(iterable, /, key=None, default=None)
    Computes the minimum and maximum values in one-pass using only 1.5*len(iterable) comparisons
"""


# convert a new sequence to the same type as the old sequence if possible
def as_type(seq, old_seq):
    try:
        len(old_seq)
    except:
        return it
    else:
        return type(old_seq)(seq)

# for seq can use grouped
# batched is very similar
def chunks_of_n(iterable, n):
    iterable = iter(iterable)
    return iter(lambda: tuple(itertools.islice(iterable, n)), ())


def n_chunks(iterable, n):
    if not isinstance(iterable, (list, tuple, set)):
        iterable = list(iterable)

    length = len(iterable)
    chunk_size = length // n
    return chunks_of_n(iterable, chunk_size)

def count_iter(iterable):
    return sum(1 for _ in iterable)

    # this one handles the last chunk being partial
def grouper(n, iterable, padvalue=None):
    "grouper(3, 'abcdefg', 'x') --> ('a','b','c'), ('d','e','f'), ('g','x','x')"
    return itertools.zip_longest(*[iter(iterable)]*n, fillvalue=padvalue)

# like map, but pass multiple functions, each element of each tuple will use corresponding function
def multimap(it, *functions, fillvalue=it_ut.return_identity):
#    ic(functions)
    return (tuple(f(t) for t, f in itertools.zip_longest(tup, functions, fillvalue=fillvalue)) for tup in it)

def multimap_tuple(it, *functions, fillvalue=it_ut.return_identity):
    return tuple(multimap(it, *functions, fillvalue=fillvalue))

def multimaptuple(it, *functions, fillvalue=it_ut.return_identity):
    return tuple(multimap(it, *functions, fillvalue=fillvalue))

def map_list(func, it):
    return list(map(func, it))

def maplist(func, it):
    return list(map(func, it))


def map_tuple(func, it):
    return tuple(map(func, it))

def maptuple(func, it):
    return tuple(map(func, it))

def starmap_list(func, it):
    return list(starmap(func, it))

def starmaplist(func, it):
    return list(starmap(func, it))

def starmap_tuple(func, it):
    return tuple(starmap(func, it))

def starmaptuple(func, it):
    return tuple(starmap(func, it))

# performs map on each element of it
# untested!
def mapmap(func, it):
    return map(map(func, el) for el in it)


def foreach(func, it):
    """
    Executes func on each element of the sequence.

    >>> l = []
    >>> seq([1, 2, 3, 4]).for_each(l.append)
    >>> l
    [1, 2, 3, 4]

    :param func: function to execute
    """
    for e in it:
        func(e)

def starforeach(func, it):
    """
    Executes func on each element of the sequence.

    >>> l = []
    >>> seq([1, 2, 3, 4]).for_each(l.append)
    >>> l
    [1, 2, 3, 4]

    :param func: function to execute
    """
    for e in it:
        func(*e)



    # like map but preserves type if it's a sequence
def map_type(func, seq):
    it = map(func, seq)

    try:
        len(seq)
    except:
        return it
    else:
        return type(seq)(it)


def all_set_operation(sets, method):
    try:
        len(sets)
    except:
        sets = list(sets)

    if not sets:
        return set()

    return method(*([set(sets[0])] + list(sets[1:])))
#    return method(*(set(sets[0]).union(sets[1:]))

    # return set of items unique to every entry in seq
def sets_intersection(seq):
    return all_set_operation(seq, set.intersection)

    # return set of items that contains every entry in every sequence in seq
def sets_union(seq):
    return all_set_operation(seq, set.union)

    # similar to splitting a string
def split_iterable(i, split_val=""):
    return (list(c) for match, c in itertools.groupby(i, lambda p: p == split_val) if not match)


def flatten(iterables):
    return (elem for iterable in iterables for elem in iterable)


# handles nested, fast http://rightfootin.blogspot.com/2006/09/more-on-python-flatten.html
def flatten_full(l, ltypes=(list, tuple)):
    ltype = type(l)
    l = list(l)
    i = 0

    while i < len(l):
        while isinstance(l[i], ltypes):
            if not l[i]:
                l.pop(i)
                i -= 1
                break
            else:
                l[i:i + 1] = l[i]

        i += 1

    return ltype(l)

   # returns list with duplicate entries removed
   # order preserving
   # if idFun is passed will use that to determine what value of item is unique
def uniqued_list(seq, idFun=None):
    if idFun is None:
        def idFun(x): return x

    seen = set()
    result = []

    for item in seq:
        marker = idFun(item)

        if marker in seen:
            continue

        seen.add(marker)
        result.append(item)

    return result

def uniqued_list(seq, idFun=None):
        # Python 3.6+ maintains order in dictionaries
    if idFun:
        result = list(dict.fromkeys(map(idFun, seq)))
    else:
        result = list(dict.fromkeys(seq))
    return result

# returns True if any elements in iterable occur more than once
def repeats(iterable):
    values = set()

    for value in iterable:
        if value in values:
            return True

        values.add(value)

    return False

def find_loop(iterable):
    values = set()

    for value in iterable:
        if value in values:
            return values

        values.add(value)

    return None


def previous_current_next(iterable):
    """Make an iterator that yields an (previous, current, next) tuple per element.

    Returns None if the value does not make sense (i.e. previous before
    first and next after last).
    """
    iterable=iter(iterable)
    prv = None
    cur = iterable.next()

    try:
        while True:
            nxt = iterable.next()
            yield (prv,cur,nxt)
            prv = cur
            cur = nxt
    except StopIteration:
        yield (prv,cur,None)




    # return first "True" element from iterable
    # taken from https://github.com/hynek/first/
def first_true(iterable, default=None, key=None):
    if key is None:
        for el in iterable:
            if el:
                return el
    else:
        for el in iterable:
            if key(el):
                return el

    return default

    # same as first, but returns index of found element rather than the element
    # note: if calling this repeatedly with the same list, it would probably result in better performance to construct a dict with the indices instead
def first_index(iterable, default=None, key=None):
    if key is None:
        for n, el in enumerate(iterable):
            if el:
                return n
    else:
        for n, el in enumerate(iterable):
            if key(el):
                return n

    return default

    # return first element from iterable
def first_element(iterable, default=None):
    for el in iterable:
        return el

    return default

    # return last element from iterable
def last_element(iterable, default=None):
    for el in iterable:
        pass

    return el

    # return tuple with one element replaced
def new_tuple(t, index, val):
    return t[0:index] + (val,) + t[index+1:]


# given a tuple or list, yield removed element and tuple/list with that element removed
def tuples_without(t):
    for i in range(len(t)):
        yield t[i], t[:i]+t[i+1:]

    # return tuple or list with one element removed
    # returns same type as that passed
def del_index(t, index=-1):
    if index < 0:
        index += len(t) # handle negative number

    return t[0:index] + t[index+1:]


    # return list with one element replaced
def new_list(l, index, val):
    l = list(l)
    l[index] = val
    return l


def dict_with_entry(dct, k, v):
    return {**dct, k: v}

def dict_with(dct, d2):
    return dct | d2
    #raise Exception("use d1 | d2 syntax to achieve this")


# dct: dictionary to remove values if present from
# d2: dictionary or iterable (preferably set for performance) that contains values we want removed
def dict_without(dct, d2):
    return dict((k, v) for k, v in dct if k not in d2)
    #raise Exception("use d1 | d2 syntax to achieve this")

def dict_without_key(dct, key):
    return dict((k, v) for k, v in dct if k != key)


def pairs_diff(p1, p2):
    s1 = set(p1)
    s2 = set(p2)
    return tuple(sorted(s1-s2)), tuple(sorted(s2-s1))

def dict_diff(d1, d2):
    return pairs_diff(d1.items(), d2.items())

def set_without(s, *i):
    return s.difference(i)

def set_without_seq(s, l):
    return s.difference(l)


# Return the longest prefix of all list elements.
def commonprefix(m):
    "Given a list of strings, returns the longest common leading component"
    if not m: return ''

    s1 = min(m)
    s2 = max(m)

    for i, c in enumerate(s1):
        if c != s2[i]:
            return s1[:i]

    return s1

# Return the longest suffix of all list elements.
def commonsuffix(m):
    "Given a list of strings, returns the longest common trailing component"
        # we just reverse each string and use common prefix, then reverse that
    return commonprefix([s[::-1] for s in m])[::-1]

# internally a nested list, allows index by tuple of indexes
# taken from google ai seasrch result for "python subclass list index by tuple"
class TupleIndexedList(list):
    """
    # Example usage:
    my_list = TupleIndexedList([
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ])

    print(my_list[1, 2])
    my_list[0, 1] = 10    # Set element at (0, 1) to 10
    print(my_list[0, 1])
    """

    def __getitem__(self, key):
        if isinstance(key, tuple):
            result = self
            for k in key:
                result = result[k]
            return result
        else:
            return super().__getitem__(key)

    def __setitem__(self, key, value):
        if isinstance(key, tuple):
            result = self
            for k in key[:-1]:
                result = result[k]
            result[key[-1]] = value
        else:
            super().__setitem__(key, value)

# internally a nested list, allows index by complex number, imaginary part is y
# this works but:
# for 130x130 grid, dict of points was faster than ComplexIndexedList (23s -> 13s)
# checking bounds via real and imag went from 23s -> 28s
# dict of tuples was noticeably slower than dict of complex 26s vs. 13s, possibly due to add_tuple vs. complex add and multiply
class ComplexIndexedList(list):
    """
    # Example usage:
    my_list = ComplexIndexedList([
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ])

    print(my_list[2+j])
    my_list[j] = 10    # Set element at (0, 1) to 10
    print(my_list[0, 1])
    """

    def __getitem__(self, key):
        if isinstance(key, complex):
            #print(key)
            if key.imag <0 or key.real < 0:
                raise IndexError("blah!")
            return self[int(key.imag)][int(key.real)]
        else:
            return super().__getitem__(key)

    def __setitem__(self, key, value):
        if isinstance(key, complex):
            if key.imag <0 or key.real < 0:
                raise IndexError("blah!")
            self[int(key.imag)][int(key.real)] = value
        else:
            super().__setitem__(key, value)


# inputs just need to be iterable, output is tuple
def add_tuple(*iterables):
#    ic(list(iterables))
    return tuple(sum(p) for p in zip(*iterables))


def add_scalar(a, b):
    return tuple(aa + b for aa in a)

def subtract_tuple(a, b):
#    return tuple(aa - bb for aa, bb in zip(a, b))
    return tuple(starmap(operator.sub, zip(a, b)))

products = math.prod

#def multiply_tuple(a, b):
#    return tuple(aa * bb for (aa, bb) in zip(a, b))

def multiply(*iterables):
    return (products(p) for p in zip(*iterables))


# this version should allow multiplying elements of more than 2 iterables
def multiply_tuple(*iterables):
    return tuple(products(p) for p in zip(*iterables))


def multiply_scalar_tuple(a, b):
    return tuple(aa * b for aa in a)

def divide_scalar_tuple(a, b):
    return tuple(aa / b for aa in a)

def true_divide_scalar_tuple(a, b):
    return tuple(aa // b for aa in a)


    # let's you perform operations on all elements of a tuple
    # e.g. materials + robots * wait - robot_cost
    # other sequence of same length or scalar
    # could also handle and, or, xor, not, inversion, ordering, negation, modulo, shifting, exponent, round, floor, ceil,
    # could do another class based on array that also allows +=, -=, etc.
class arithtuple(tuple):
    def __add__(self, other):
        try:
            return arithtuple(map(operator.add, self, other))
        except TypeError as e:
            # handle case of operation on scalar
            return arithtuple(map(operator.add, self, (other,) * len(self)))

    def __sub__(self, other):
        try:
            return arithtuple(map(operator.sub, self, other))
        except TypeError as e:
            # handle case of operation on scalar
            return arithtuple(map(operator.sub, self, (other,) * len(self)))

    def __mul__(self, other):
        try:
            return arithtuple(map(operator.mul, self, other))
        except TypeError as e:
                # handle case of operation on scalar
            try:
                return arithtuple(map(operator.mul, self, (other,) * len(self)))
            except TypeError as e:
                ic(other)
                raise
    def __truediv__(self, other):
        try:
            return arithtuple(map(operator.truediv, self, other))
        except TypeError as e:
                # handle case of operation on scalar
            return arithtuple(map(operator.truediv, self, (other,) * len(self)))

    def __floordiv__(self, other):
        try:
            return arithtuple(map(operator.floordiv, self, other))
        except TypeError as e:
                # handle case of operation on scalar
            try:
                return arithtuple(map(operator.floordiv, self, (other,) * len(self)))
            except TypeError as e:
                ic(other)
                raise

    def __mod__(self, other):
        try:
            return arithtuple(map(operator.mod, self, other))
        except TypeError as e:
                # handle case of operation on scalar
            return arithtuple(map(operator.mod, self, (other,) * len(self)))

    def _replace(self, index, val):
        return arithtuple(self[0:index] + (val,) + self[index+1:])


def build_arithmetic_namedtuple(_class):
    class arithmetic_namedtuple(_class):
        def __add__(self, other):
            try:
                return self.__class__(*map(operator.add, self, other))
            except TypeError as e:
                # handle case of operation on scalar
                return self.__class__(*map(operator.add, self, (other,) * len(self)))

        def __sub__(self, other):
            try:
                return self.__class__(*map(operator.sub, self, other))
            except TypeError as e:
                # handle case of operation on scalar
                return self.__class__(*map(operator.sub, self, (other,) * len(self)))


        def __mul__(self, other):
            try:
                return self.__class__(*map(operator.mul, self, other))
            except TypeError as e:
                    # handle case of operation on scalar
                return self.__class__(*map(operator.mul, self, (other,) * len(self)))

        def __truediv__(self, other):
            try:
                return self.__class__(*map(operator.truediv, self, other))
            except TypeError as e:
                    # handle case of operation on scalar
                return self.__class__(*map(operator.truediv, self, (other,) * len(self)))

        def __floordiv__(self, other):
            try:
                return self.__class__(*map(operator.floordiv, self, other))
            except TypeError as e:
                    # handle case of operation on scalar
                return self.__class__(*map(operator.floordiv, self, (other,) * len(self)))

        def __mod__(self, other):
            try:
                return self.__class__(*map(operator.mod, self, other))
            except TypeError as e:
#                print("other", other)
                    # handle case of operation on scalar
                return self.__class__(*map(operator.mod, self, (other,) * len(self)))
#                return self.__class__(*(x % other for x in self))

        def _replace(self, index, val):
            return self.__class__(*(self[0:index] + (val,) + self[index+1:]))

    return arithmetic_namedtuple

    # return sequence of max values of each sub-sequence
def seq_max(seq):
    return (max(subseq[n] for subseq in seq) for n in range(len(seq[0])))

# can use int.bit_count() to count number of bits
def iterate_set_bits(n):
    """
    Iterates through the positions of set bits in an integer.
    Yields the position (0-indexed) of each set bit.
    """
    position = 0

    while n > 0:
        if n & 1:  # Check if the least significant bit is set
            yield position
        n >>= 1  # Right shift the number by 1 to check the next bit
        position += 1


# =======================
# from itertools recipes
# =======================
__FROM_ITERTOOLS_RECIPES__ = ""

def take(n, iterable):
    "Return first n items of the iterable as a list"
    return list(islice(iterable, n))

def prepend(value, iterator):
    "Prepend a single value in front of an iterator"
    # prepend(1, [2, 3, 4]) --> 1 2 3 4
    return chain([value], iterator)

# itertools recipes has tabulate, but that has name collision with very useful library
def iter_tabulate(function, start=0):
    "Return function(0), function(1), ..."
    return map(function, count(start))

def successive(function, start=0):
    "Return function(0), function(1), ..."
    return map(function, count(start))

def tail(n, iterable):
    "Return an iterator over the last n items"
    # tail(3, 'ABCDEFG') --> E F G
    return iter(collections.deque(iterable, maxlen=n))

def consume(iterator, n=None):
    "Advance the iterator n-steps ahead. If n is None, consume entirely."
    # Use functions that consume iterators at C speed.
    if n is None:
        # feed the entire iterator into a zero-length deque
        collections.deque(iterator, maxlen=0)
    else:
        # advance to the empty slice starting at position n
        next(islice(iterator, n, n), None)

def nth(iterable, n, default=None):
    "Returns the nth item or a default value"
    return next(islice(iterable, n, None), default)

def quantify(iterable, pred=bool):
    "Given a predicate that returns True or False, count the True results."
    return sum(map(pred, iterable))

def all_equal(iterable):
    "Returns True if all the elements are equal to each other"
    g = groupby(iterable)
    return next(g, True) and not next(g, False)

def iter_index(iterable, value, start=0):
    "Return indices where a value occurs in a sequence or iterable."
    # iter_index('AABCADEAF', 'A') --> 0 1 4 7
    try:
        seq_index = iterable.index
    except AttributeError:
        # Slow path for general iterables
        it = islice(iterable, start, None)
        for i, element in enumerate(it, start):
            if element is value or element == value:
                yield i
    else:
        # Fast path for sequences
        i = start - 1
        try:
            while True:
                yield (i := seq_index(value, i+1))
        except ValueError:
            pass

def sliding_window(iterable, n):
    "Collect data into overlapping fixed-length chunks or blocks."
    # sliding_window('ABCDEFG', 4) --> ABCD BCDE CDEF DEFG
    it = iter(iterable)
    window = collections.deque(islice(it, n-1), maxlen=n)
    for x in it:
        window.append(x)
        yield tuple(window)

def roundrobin(*iterables):
    "roundrobin('ABC', 'D', 'EF') --> A D E B F C"
    # Recipe credited to George Sakkis
    num_active = len(iterables)
    nexts = cycle(iter(it).__next__ for it in iterables)
    while num_active:
        try:
            for next in nexts:
                yield next()
        except StopIteration:
            # Remove the iterator we just exhausted from the cycle.
            num_active -= 1
            nexts = cycle(islice(nexts, num_active))

def partition(pred, iterable):
    """Partition entries into false entries and true entries.

    If *pred* is slow, consider wrapping it with functools.lru_cache().
    """
    # partition(is_odd, range(10)) --> 0 2 4 6 8   and  1 3 5 7 9
    t1, t2 = tee(iterable)
    return filterfalse(pred, t1), filter(pred, t2)


def batched(iterable, n):
    "Batch data into tuples of length n. The last batch may be shorter."
    # batched('ABCDEFG', 3) --> ABC DEF G
    if n < 1:
        raise ValueError('n must be at least one')

    it = iter(iterable)

    while (batch := tuple(islice(it, n))):
        yield batch

if 0: # already have a grouper function above with different params
    def grouper(iterable, n, *, incomplete='fill', fillvalue=None):
        "Collect data into non-overlapping fixed-length chunks or blocks"
        # grouper('ABCDEFG', 3, fillvalue='x') --> ABC DEF Gxx
        # grouper('ABCDEFG', 3, incomplete='strict') --> ABC DEF ValueError
        # grouper('ABCDEFG', 3, incomplete='ignore') --> ABC DEF
        args = [iter(iterable)] * n

        if incomplete == 'fill':
            return zip_longest(*args, fillvalue=fillvalue)

        if incomplete == 'strict':
            return zip(*args, strict=True)

        if incomplete == 'ignore':
            return zip(*args)
        else:
            raise ValueError('Expected fill, strict, or ignore')

def sumprodtuples(tuples):
    "Compute a sum of products."
    return sum(map(math.prod, tuples))

def sumprod(vec1, vec2):
    "Compute a sum of products."
    return sum(starmap(operator.mul, zip(vec1, vec2, strict=True)))


def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)  # allows duplicate elements
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

def sum_of_squares(it):
    "Add up the squares of the input values."
    # sum_of_squares([10, 20, 30]) -> 1400
    return sumprod(*tee(it))

def transpose(it):
    "Swap the rows and columns of the input."
    # transpose([(1, 2, 3), (11, 22, 33)]) --> (1, 11) (2, 22) (3, 33)
    return zip(*it, strict=True)

def matmul(m1, m2):
    "Multiply two matrices."
    # matmul([(7, 5), (3, 5)], [[2, 5], [7, 9]]) --> (49, 80), (41, 60)
    n = len(m2[0])
    return batched(starmap(sumprod, product(m1, transpose(m2))), n)

def convolve(signal, kernel):
    # See:  https://betterexplained.com/articles/intuitive-convolution/
    # convolve(data, [0.25, 0.25, 0.25, 0.25]) --> Moving average (blur)
    # convolve(data, [1, -1]) --> 1st finite difference (1st derivative)
    # convolve(data, [1, -2, 1]) --> 2nd finite difference (2nd derivative)
    kernel = tuple(kernel)[::-1]
    n = len(kernel)
    window = collections.deque([0], maxlen=n) * n

    for x in chain(signal, repeat(0, n-1)):
        window.append(x)
        yield sumprod(kernel, window)


def triplewise(iterable):
    "Return overlapping triplets from an iterable"
    # triplewise('ABCDEFG') --> ABC BCD CDE DEF EFG
    for (a, _), (b, c) in pairwise(pairwise(iterable)):
        yield a, b, c


