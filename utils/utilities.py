from __future__ import print_function
# -*- coding: utf-8 -*-
import sys
import os
import itertools
from icecream import ic

from utils.yaml_utils import *
from utils.string_utils import *
from utils.iter_utils import *

def get_integers_from_string(s):
    return (int("".join(c)) for match, c in itertools.groupby(s, lambda c: c.isdigit() or c =="-") if match)

def get_vis_map(dots, reversed = False, min_val=None, max_val=None):
    def get_dim(dims):
        dims = list(dims)
        negative_x = min(dims) if min_val is None else min_val
        positive_x = max(dims) + 1 if max_val is None else max_val
        return -negative_x, max(15, positive_x - negative_x)

    assert(dots)
    min_x, width = get_dim(p.x for p in dots)
    min_y, height = get_dim(p.y for p in dots)
    vis_map = [["."] * width for r in range(height)]

    for p in dots:
        try:
            if reversed:
                vis_map[height - (p.y + min_y) - 1][p.x + min_x] = "#"
            else:
                vis_map[p.y + min_y][p.x + min_x] = "#"
        except IndexError:
            ic(p.y, p.x)
            raise

    vis_map = [f"({-min_x},{-min_y})"] + ["".join(e) for e in vis_map]
    return vis_map

def walk(dir_,  excluded):
    """Traverse a directory tree in pre-order.

    branches specified in exclude are ignored. Symbolic links are followed.
    """

    try:
        subs = os.listdir(dir_)
    except OSError:
        return

    subs = [os.path.join(dir_, sub) for sub in subs]
    subs = [sub for sub in subs if os.path.isdir(sub) and sub not in excluded]

    yield dir_

    for sub in subs:
        for res in walk(sub, excluded):
            yield res

class PrintMaxTimes(object):
    def __init__(self, max_count, out_method = print):
        self.max_count = max_count
        self.printed_count = 0
        self.out_method = out_method

    def print(self, *msg):
        if self.printed_count < self.max_count:
            self.out_method(*msg)
            self.printed_count += 1

    def should_print_and_inc(self):
        result = self.printed_count < self.max_count
        self.printed_count += 1
        return result

    def should_print(self):
        return self.printed_count < self.max_count
