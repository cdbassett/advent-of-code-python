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
from icecream import ic

from utils.aoc_utils import * # this includes adding c:\ut to sys.path
from utils.utilities import *
import utils.seq_extensions # these extend PyFunctional seq objects, don't need to directly use anything in it
from utils.quicklambda import _1, _2


# https://adventofcode.com/2020/day/20


icf = ic.format


sea_monster = \
"""
..................#.
#....##....##....###
.#..#..#..#..#..#...
""".strip("\n").split("\n")


@timefunction
def run(inp1, inp2, is_real):
    insert_sample_functions(is_real, globals())

    def data_parse(inp):
        lines = inp.strip().split('\n')
#        lines = inp.strip("\n").split('\n')
        tile_parts = split_iterable(lines, "")
        tiles = seq(tile_parts).map(head_tail).multimap(compose(itemgetter(0), string_to_integers), identity).to_dict()
#        ics(tiles)
        return tiles

#    rev_str = compose(reversed, sjoin)

    def rev_str(s):
        return s[::-1]

    def transpose_tile(tile):
#        return seq(zip(*tile)).map(partial(map_tuple, sjoin)).to_tuple()
        return seq(zip(*tile)).map(sjoin).to_tuple()

    def flip_horiz(tile):
        return map_list(rev_str, tile)

    def flip_vert(tile):
        return tile[::-1]

        # AB -> CA
        # CD    DB
    def rotate_right(tile):
        return flip_horiz(transpose_tile(tile))

        # AB -> BD
        # CD    AC
    def rotate_left(tile):
        return flip_vert(transpose_tile(tile))

        # AB    ->  DC
        # CD        BA
    def rotate_180(tile):
        return flip_horiz(flip_vert(tile))


    TOP = 0
    BOT = 1
    LEFT = 2
    RIGHT = 3
    RTOP = 4
    RBOT = 5
    RLEFT = 6
    RRIGHT = 7

    border_descs = "top bottom left right rtop rbott rleft rright".split()

    def get_top_and_bottom(tile):
        top = tile[0]
        bot = rev_str(tile[-1]) # we want the same orientation for each side
#        return top, rev_str(top), bot, rev_str(bot)
        return top, bot

    def get_left_and_right(tile):
        rotated_tile = rotate_right(tile)
#        ics(rotated_tile)
        return get_top_and_bottom(rotated_tile)

    def get_borders(tile):
#        ics(tile)
        top_bot = get_top_and_bottom(tile)
        left_right = get_left_and_right(tile)
        reg_borders = top_bot + left_right
        return reg_borders + tuple(flip_horiz(reg_borders))
#        return get_top_and_bottom(tile) + get_top_and_bottom(transposed_tile)

    transformations = {
        (TOP, LEFT): rotate_left,
        (BOT, LEFT): rotate_right,
        (LEFT, LEFT): identity,
        (RIGHT, LEFT): rotate_180,
        (RTOP, LEFT): compose(rotate_left, flip_vert),
        (RBOT, LEFT): compose(rotate_right, flip_vert),
        (RLEFT, LEFT): flip_vert,
        (RRIGHT, LEFT): compose(rotate_180, flip_vert),

#        (TOP, RLEFT): rotate_left,
#        (BOT, RLEFT): rotate_right,
#        (LEFT, RLEFT): identity,
#        (RIGHT, RLEFT): rotate_180,
#        (RTOP, RLEFT): compose(rotate_left, flip_vert),
#        (RBOT, RLEFT): compose(rotate_right, flip_vert),
#        (RLEFT, RLEFT): flip_vert,
#        (RRIGHT, RLEFT): compose(rotate_180, flip_vert),

        (TOP, TOP): identity,
        (BOT, TOP): rotate_180,
        (LEFT, TOP): rotate_right,
        (RIGHT, TOP): rotate_left,
        (RTOP, TOP): flip_horiz,
        (RBOT, TOP): compose(rotate_180, flip_horiz),
        (RLEFT, TOP): compose(rotate_right, flip_horiz),
        (RRIGHT, TOP): compose(rotate_left, flip_horiz),
        }

    def transform_tile(tile, from_border_index, desired_border_index):
#        ics("transform_tile", border_descs[from_border_index], border_descs[desired_border_index])
#        ics(tile)

        return transformations[(from_border_index, desired_border_index)](tile)

        if 0:
            if from_border_index == desired_border_index:
                return tile

            normalized_index = from_border_index % 4 # what the side will be without considering reversing

            if normalized_index == desired_border_index:
#            return transpose_tile(tile)
#            return flip_horiz(tile) if normalized_index <= BOT else flip_vert(tile)
                return flip_vert(tile) if normalized_index <= BOT else flip_horiz(tile)

            is_reversed = from_border_index // 4
            is_rot = normalized_index // 2 != desired_border_index // 2 # one is top/bot, other is left/right
            ics(border_descs[from_border_index], border_descs[desired_border_index])
            ics(is_reversed, normalized_index, is_rot)

            raise NotImplementedError

    opposite_sides = [
        BOT,
        TOP,
        RIGHT,
        LEFT
        ]

        # the idnex on the other side
    def opposite_border_index(from_border_index):
        normalized_index = from_border_index % 4 # what the side will be without considering reversing
        is_reversed = from_border_index // 4
        new_index = opposite_sides[normalized_index]

        if is_reversed:
            new_index += 4 # convert back to reversed

        return new_index

    def join_tiles_horiz(tiles, between=""):
        return [between.join(lines) for lines in zip(*tiles)]

    def join_tiles_vert(tiles, between = None):
        if between is None:
            return list(chain(*tiles))

        return list(chain(*roundrobin(tiles, repeat(between, len(tiles)-1))))

    def join_tiles_grid(all_tiles, gaps = False):
        if gaps:
            return join_tiles_vert([join_tiles_horiz(row, " ") for row in all_tiles], [""])

        return join_tiles_vert([join_tiles_horiz(row) for row in all_tiles])





    def process1(tiles_dict):
        def match_tile_seq(left_id, left_border_index, override_matching_border = None):
            matched_tiles = []
            desired_border_index = opposite_border_index(left_border_index)

            for x in range(1, side_size):
#                ic(x, left_id, border_descs[left_border_index])
                matching_border = override_matching_border or rev_str(tile_borders[left_id][left_border_index]) # reversed because opposing sides
#                ic(matching_border, tiles_by_border[matching_border])
                right_id = seq(tiles_by_border[matching_border]).filter(_1 != left_id).one()
                right_tile = tiles_dict[right_id]
                right_border_index = tile_borders[right_id].index(matching_border)
                transformed_tile = transform_tile(right_tile, right_border_index, desired_border_index)
                matched_tiles.append((right_id, transformed_tile))
                left_id = right_id
                left_border_index = opposite_border_index(right_border_index)
#                ics(right_id, border_descs[left_border_index], border_descs[right_border_index])
#                ics(right_id)
#                ics(transformed_tile)
                override_matching_border = None

            return matched_tiles

        values = Counter()
#        tile_borders = {} # top, top_rev, bot, bot_rev, left, left_rev, right, right_rev
        tile_borders = {} # tile_id -> top, top_rev, bot, bot_rev, left, left_rev, right, right_rev
        tiles_by_border = defaultdict(list)

#        ics(get_borders(it_ut.first(tiles_dict.values())))

        for tile_id, tile in tiles_dict.items():
            borders = get_borders(tile)
            values.update(borders)
            tile_borders[tile_id] = borders

            for border in borders:
                tiles_by_border[border].append(tile_id)

#            tiles_by_border.update(zip(borders, repeat(tile_id)))

#        ics(values)
        side_size = sqrt(len(tiles_dict))
        assert round(side_size) == side_size
        side_size = round(side_size)
        ic(len(tiles_dict), len(values), side_size, len(values))
#        ic(seq(values.items()).filter(compose(itemgetter(1), partial(operator.eq, 1))).len())
        ic(seq(values.items()).starfilter(_2 == 1).len())
        ic(seq(values.items()).starfilter(_2 == 2).len())
#        ic(side_size, len(tiles_dict)*8 - side_size * 4)

#        ics(seq(tile_borders.items()).starmap(lambda id, borders: (id, seq(borders).filter(lambda border: values[border] == 1).len())))
#        ics(seq(tile_borders.items()).starmap(lambda id, borders: (id, seq(borders).filter(lambda border: values[border] == 2).len())))

            # corners have 4 unmatched sides bc of reversed
        tile_corners = seq(tile_borders.items()).starfilter(lambda id, borders: seq(borders).filter(lambda border: values[border] == 1).len() == 4).to_dict()
#        ic(len(tile_corners.keys()), tile_corners.keys())
            # corners have 2 unmatched sides bc of reversed
        tile_sides = seq(tile_borders.items()).starfilter(lambda id, borders: seq(borders).filter(lambda border: values[border] == 1).len() == 2).to_dict()
#        ic(len(tile_sides.keys()), tile_sides.keys())
        assert len(tile_corners) == 4
        assert len(tile_sides) == (side_size - 2) * 4
#        ic(products(tile_corners.keys()))

            # we know our data has 2 that match, either will work, sample data has exactly one, this way we dont' have to rotate starting tile and borders for it
        starting_corner_id = seq(tile_corners.keys()).filter(lambda tile_id: seq(tiles_by_border[tile_borders[tile_id][TOP]]).len() == 1 and seq(tiles_by_border[tile_borders[tile_id][LEFT]]).len() == 1).first()
        starting_corner_tile = tiles_dict[starting_corner_id]

#        if is_real:
#            ic(tile_borders[1283])
#            ic(tile_borders[2063])

        ic(width(starting_corner_tile),height(starting_corner_tile))
#        ics(starting_corner_id, starting_corner_tile)
#        ics(rotate_180(starting_corner_tile))
#        ic("top row")
            # build top row
        top_tiles = [(starting_corner_id, starting_corner_tile)] + match_tile_seq(starting_corner_id, RIGHT)
#        ics(join_tiles_horiz(t[1] for t in top_tiles))
#        ic("left col")
            # build left column
        left_tiles = match_tile_seq(starting_corner_id, BOT)
#        ics(join_tiles_vert([t[1] for t in [(starting_corner_id, starting_corner_tile)] + left_tiles]))
        all_tiles = [top_tiles]

            # fill rest of rows from left column
        for y, (left_id, left_tile) in zip(range(1, side_size), left_tiles):
#            ic("row", y, left_id)
            _, use_border = get_left_and_right(left_tile)
#            from_border_index = tile_borders[left_id].index(use_border)
#            row_tiles = match_tile_seq(left_id, from_border_index)
            row_tiles = match_tile_seq(left_id, RIGHT, rev_str(use_border))
            full_row = [(left_id, left_tile)] + row_tiles
#            ics(join_tiles_horiz(t[1] for t in full_row))
            all_tiles.append(full_row)

        all_tiles_only = [[t[1] for t in row] for row in all_tiles]
        all_tiles_stripped = [[[line[1:-1] for line in t][1:-1] for t in row] for row in all_tiles_only]

#        fp = join_tiles_grid(all_tiles_only)

#        print("\n".join(join_tiles_grid(all_tiles_only, True)))
#        print()
#        print("\n".join(join_tiles_grid(all_tiles_stripped)))
        ic(width(all_tiles_stripped), height(all_tiles_stripped))

#        ics(join_tiles_horiz((starting_corner_tile, transformed_tile)))

        return products(tile_corners.keys()), join_tiles_grid(all_tiles_stripped)



    @timefunction
    def part1(inp):
        tiles_dict = data_parse(inp)
        result,_ = process1(tiles_dict)
        print_result(result)


    def get_2D_rotations(lines):
        return [lines, rotate_right(lines), rotate_180(lines), rotate_left(lines)]

    def get_2D_variations(lines):
        base = get_2D_rotations(lines)
        base += get_2D_rotations(flip_vert(lines))
#        base += get_2D_rotations(flip_horiz(lines))
        return base

    def process2(full_pic):
#        rot_right_sea_monster = rotate_right(sea_monster)
#        ic(width(rot_right_sea_monster), width(rot_right_sea_monster))
#        ic(rot_right_sea_monster)
        ic(width(sea_monster), height(sea_monster))
#        ic(tuple(get_hash_coords(sea_monster)))
#        ic(sea_monster)

        sea_monster_variations = get_2D_variations(sea_monster)
        sea_monster_variation_tuple = map_tuple(compose(get_hash_coords, tuple), sea_monster_variations)
#        ics(len(sea_monster_variations))
#        sea_monster_variation_set = set(map("\n".join, sea_monster_variations))
#        sea_monster_variation_set = set(map(compose(get_hash_coords, tuple), sea_monster_variations))
#        ics(len(sea_monster_variation_set))

        if 0:
            for n, sea_monster_variations in enumerate(sea_monster_variations):
                ic(n)
                print("\n".join(sea_monster_variations))
                print("=" * 20)

#        ics(sea_monster_variation_set)
        ics(full_pic)
        pic_points = set(get_hash_coords(full_pic))
        ic(width(full_pic), height(full_pic), len(pic_points))
        found_count = 0
        w, h = width(full_pic), height(full_pic)
        ics(len(sea_monster_variation_tuple))
        found_at = defaultdict(list)


        for xy in product(range(w), range(h)):
            for v, sea_monster_variation in enumerate(sea_monster_variation_tuple):
                if pic_points.issuperset(map(partial(add_tuple, xy), sea_monster_variation)):
                    found_count += 1
                    found_at[v].append(xy)

#        ics(found_at)
        for v, coords in found_at.items():
            ic(v, len(coords))

        ic(found_count)
        return len(pic_points) - found_count * len(sea_monster_variation_tuple[0])

    @timefunction
    def part2(inp):
        tiles_dict = data_parse(inp)
        _, full_pic = process1(tiles_dict)
        result = process2(full_pic)
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

