from functools import *
from collections import *
from sympy import *
from itertools import *
from math import *
from statistics import *
from builtins import pow
import pyperclip
from icecream import ic
import copy
from timer_utils import timefunction

from aoc_utils import * # this includes adding c:\ut to sys.path
from Utilities import *
import seq_extensions # these extend PyFunctional seq objects, don't need to directly use anything in it


Point = Point2D

def run(inp, is_real):
    ics = nothing if is_real else ic
    print_result = partial(print_result_aoc, is_real)

#    inp = inp.strip().split('\n')
    inp = inp.strip("\n").split('\n')
#    ic(inp[:5])
#    ic(list(line[:60] for line in inp[:5]))
    ic(len(inp))
    the_map, instructions = split_iterable(inp, "")
    instructions = "".join(instructions)
    ic(len(instructions))
#    ics(instructions)
    instructions = list(int("".join(g)) if isdigit else "".join(g) for isdigit, g in groupby(instructions, key=lambda x: x.isdigit()))
#    instructions = list(chunks_of_n(instructions, 2))
    instructions = list(grouper(2, instructions, " "))

    left_positions = [line.find(line.strip()[0]) for line in the_map]
#    ics(left_positions)
    right_positions = [len(line) - 1 for line in the_map]
#    ics(right_positions)

    full_width = max(len(line) for line in the_map)
    ic(full_width)
    full_height = height(the_map)
    ic(full_height)
    the_map = [line.ljust(full_width) for line in the_map]
    transposed_map = list("".join(line) for line in zip(*the_map))

    top_positions = [line.find(line.strip()[0]) for line in transposed_map]
    ics(top_positions)
    bottom_positions = [len(line.rstrip()) - 1 for line in transposed_map]
    ics(bottom_positions)

#    instructions = list((k,list(g)) for k, g in groupby(instructions[0], key=lambda x: x in ("R", "L")))
    ics(the_map)
#    ic(the_map[:5])
    ics(instructions)
#    Facing is 0 for right (>), 1 for down (v), 2 for left (<), and 3 for up (^)

    movements = [
        arithtuple((1, 0)), # right, 0
        arithtuple((0, 1)), #down, 1
        arithtuple((-1, 0)), # left, 2
        arithtuple((0, -1)), #up, 3
        ]

    move_right, move_down, move_left, move_up = movements

    rotation_chars = {
        "R" : 1,
        "L" : -1,
        " " : 0,
        }

    right, down, left, up, face = range(5)
    dir_text = ("right", "down", "left", "up", "face")

#    ups = [[n - 1] * full_width for n in range(full_height)]
#    downs = [[n + 1] * full_width for n in range(full_height)]
#    lefts = [[n - 1 for n in range(full_width)]] * full_height
##    lefts = [n - 1 for n in range(full_width)]
#    rights = [[n + 1 for n in range(full_width)]] * full_height
##    rights = [n + 1 for n in range(full_width)]
#    ics(lefts, rights, ups, downs)

#    links = list(list(zip(rights, downs, lefts, ups)])
#    ics(list(range(full_width)))
#    ics(list(range(full_height)))


    def build_basic_links():
        links = [[None] * full_width  for n in range(full_height)]

        for x, y in product(range(full_width), range(full_height)):
            if left_positions[y] <= x <= right_positions[y] and top_positions[x] <= y <= bottom_positions[x]:
                x_left = x - 1
                x_right = x + 1
                y_up = y - 1
                y_down = y + 1

                links[y][x] = [
                    (x_right, y),
                    (x, y_down),
                    (x_left, y),
                    (x, y_up),
                    0
                    ]

        return links

    def fixup_links_for_walls(links):
        org_links = copy.deepcopy(links)

        if 0:
            for x, y in product(range(full_width), range(full_height)):
                if the_map[y][x] == "#":
                    link = org_links[y][x]
                    change_x, change_y = link[up]
                    links[change_y][change_x][down] = (change_x, change_y)

                    change_x, change_y = link[down]
                    links[change_y][change_x][up] = (change_x, change_y)

                    change_x, change_y = link[left]
                    links[change_y][change_x][right] = (change_x, change_y)

                    change_x, change_y = link[right]
                    links[change_y][change_x][left] = (change_x, change_y)

        for p in product(range(full_width), range(full_height)):
            x, y = p
            link = org_links[y][x]

            if link:
                for dir in range(4):
                    change_x, change_y = link[dir]
#                    ic(x, y, dir, change_x, change_y)

                    if the_map[change_y][change_x] == "#":
                        links[y][x][dir] = None

        for x, y in product(range(full_width), range(full_height)):
            if the_map[y][x] == "#":
                links[y][x] = None


    arrows = ">v<^"
    faces = [[None] * full_width for _ in the_map]

    def get_vis_link_map(links, direction):
        link_map = [list(line) for line in the_map]

        for p in product(range(full_width), range(full_height)):
            x, y = p
            link = links[y][x]

            if not link:
                link_map[y][x] = " "
                continue

            if direction == face:
                link_map[y][x] = str(faces[y][x]) if link else " "
                continue



            check_link = link[direction]

#            if direction == rotation:
#                link_map[y][x] = r"%\o/%"[check_link + 2]
#                continue



            right_link, down_link, left_link, up_link, rot = link
            movement = movements[direction]
            arrow = arrows[direction]

#            link_map_el =
            axes = (0, 1, 0, 1)
            axis = axes[direction]
            edge_markers = "|-"
            axis = axes[direction]


            if not check_link:
                link_map[y][x] = "$"
#            elif check_link == (x, y):
#                link_map[y][x] = "$"
            elif check_link == movement + (x, y):
                link_map[y][x] = arrow
            elif check_link[axis] != p[axis]:
                link_map[y][x] = edge_markers[axis]

        return "\n".join(repr_m(link_map))
#        return link_map

    def print_vis_link_map(links, direction):
        print(dir_text[direction])
        print(get_vis_link_map(links, direction))


#    ics(left_arrows)

    @timefunction
    def part1():
        links = build_basic_links()
#        ics(get_vis_link_map(links))
#        print("\n".join(repr_m(link_map)),"\n")
#        print("\n".join(repr_m(get_vis_link_map(links, left))),"\n")
        print(get_vis_link_map(links, left),"\n")

        for x in range(full_width):
            top_y = top_positions[x]
            bot_y = bottom_positions[x]
            links[top_y][x][up] = (x, bot_y)
            links[bot_y][x][down] = (x, top_y)

        for y in range(full_height):
            left_x = left_positions[y]
            right_x = right_positions[y]
            links[y][left_x][left] = (right_x, y)
            links[y][right_x][right] = (left_x, y)


        fixup_links_for_walls(links)
        facing = 0
        adjust = movements[facing]
#        ics(top_positions)
#        ics(left_positions[0])
#        ics(top_positions[left_positions[0]])
        start = left_positions[0], top_positions[left_positions[0]]
        x, y = start
        ic(start)
        movement_map = [list(line) for line in the_map]
        points = set()
#        print("\n".join(repr_m(movement_map[:60])),"\n")

        for n, (cnt, direction) in enumerate(instructions):
            adjust = movements[facing]

            if n < 10:
                ic(n, cnt, direction, facing, x, y)

            for _ in range(cnt):
                points.add(Point(x, y))
#                position += adjust
                link = links[y][x]
                assert link, ic.format(_, x, y, facing)
                movement_map[y][x] = arrows[facing]
                new_p = link[facing]

                if new_p:
                    x, y = link[facing]


            movement_map[y][x] = arrows[facing]
            facing = (facing + rotation_chars[direction]) % 4
#            ics(n, facing, position)

#            if n < 10:
#                print("\n".join(repr_m(movement_map)),"\n")

#        print("\n".join(the_map))
#        print("\n".join(repr_m(movement_map)))
#        print("\n".join(get_vis_map(points)))
#        ics(facing, position)
#        print("\n".join(repr_m(movement_map[:60])),"\n")
        result = (y + 1) * 1000 + (x + 1) * 4 + facing
        print_result(result)



    @timefunction
    def part2():
        nonlocal the_map, instructions
        cube_width = full_width / 3 if is_real else full_width / 4
        cube_height = full_height / 4 if is_real else full_height / 3
        assert cube_height == int(cube_height)
        assert cube_width == int(cube_width)
        cube_height = int(cube_height)
        cube_width = int(cube_width)
        assert cube_width == cube_height
        cube_x_count = full_width // cube_width
        cube_y_count = full_height // cube_height
        ic(cube_height)
        cube_range = tuple(range(cube_height))
        cube_half = cube_height // 2

        links = build_basic_links()
#        rotations = [[[0] * 4] * full_width] * full_height
        rotations = [[[0] * 4 for _ in line] for line in the_map]

#        ic(rotations[:2])
#        print("left")
#        print(get_vis_link_map(links, left))
#        print("right")
#        print(get_vis_link_map(links, right))

#        stitch_adj = [
#            arithtuple((-1, 0)), # right, 0
#            arithtuple((0, -1)), #down, 1
#            arithtuple((0, 0)), # left, 2
#            arithtuple((0, 0)), #up, 3
#            ]
#        print_vis_link_map(links, left)


        def set_face(p1, p2, face):
            for x, y in product(range(p1[0], p2[0]), range(p1[1], p2[1])):
                faces[y][x] = face


        def stitch(p1, side1, prog_dir1, p2, side2, prog_dir2, rot = 0):
#            ic("stitch", p1, p2)
            p1_adjust = movements[prog_dir1]
            p2_adjust = movements[prog_dir2]
#            p1 = p1 + stitch_adj[side1]
#            p2 = p2 + stitch_adj[side2]
            ics(p1, side1, p1_adjust)
            ics(p2, side2, p2_adjust)

            for n in cube_range:
#                if n == cube_height - 1:
#                    ic(n, p1, p2)

                ics(n, p1, p2)
                link1 = links[p1[1]][p1[0]]
                rotation1 = rotations[p1[1]][p1[0]]
                assert link1, ic.format(n, p1, link)
                link1[side1] = p2
                rotation1[side1] = rot

                link2 = links[p2[1]][p2[0]]
                rotation2 = rotations[p2[1]][p2[0]]
                assert link2, ic.format(n, p2, link)
                link2[side2] = p1
                rotation2[side2] = rot * -1

                p1 = p1_adjust + p1
                p2 = p2_adjust + p2

#                if n ==0 or n == cube_height - 1:
#                    ic(n, p1, p2, link1, link2)

        def make_corner(x_mult, y_mult):
            return arithtuple((cube_width * x_mult, cube_height * y_mult))


        corner_0_1 = make_corner(0, 1)
        corner_0_2 = make_corner(0, 2)
        corner_0_3 = make_corner(0, 3)
        corner_0_4 = make_corner(0, 4)
        corner_1_0 = make_corner(1, 0)
        corner_1_1 = make_corner(1, 1)
        corner_1_2 = make_corner(1, 2)
        corner_1_3 = make_corner(1, 3)
        corner_1_4 = make_corner(1, 4)
        corner_2_1 = make_corner(2, 1)
        corner_2_2 = make_corner(2, 2)
        corner_2_3 = make_corner(2, 3)
        corner_2_0 = make_corner(2, 0)
        corner_3_0 = make_corner(3, 0)
        corner_3_1 = make_corner(3, 1)
        corner_3_2 = make_corner(3, 2)
        corner_3_3 = make_corner(3, 3)
        corner_4_3 = make_corner(4, 3)

        if is_real:
            set_face(corner_1_0, corner_2_1, 0)
            set_face(corner_2_0, corner_3_1, 1)

            set_face(corner_1_1, corner_2_2, 2)

            set_face(corner_0_2, corner_1_3, 3)
            set_face(corner_1_2, corner_2_3, 4)

            set_face(corner_0_3, corner_1_4, 5)

            # 2 <-> 1
            stitch(corner_2_1 + move_left, right, down, corner_2_1 + move_up, down, right, -1)
            # 5 <-> 4
            stitch(corner_1_3 + move_left, right, down, corner_1_3 + move_up, down, right, -1)
            # 3 <-> 2
            stitch(corner_0_2, up, right, corner_1_1, left, down, 1)
            # 1 <-> 4
            stitch(corner_3_0 + move_left, right, down, corner_2_3 + move_left + move_up, right, up, 2)
            # 0 <-> 5
            stitch(corner_1_0, up, right, corner_0_3, left, down, 1)
            # 1 <-> 5
            stitch(corner_2_0, up, right, corner_0_4 + move_up, down, right, 0)
            # 0 <-> 3
            stitch(corner_1_0, left, down, corner_0_3 + move_up, left, up, 2)

        else:
            set_face(corner_2_0, corner_3_1, 0)
            set_face(corner_0_1, corner_1_2, 1)
            set_face(corner_1_1, corner_2_2, 2)
            set_face(corner_2_1, corner_3_2, 3)
            set_face(corner_2_2, corner_3_3, 4)
            set_face(corner_3_2, corner_4_3, 5)

            stitch(corner_2_0, left, down, corner_1_1, up, right, -1)
            stitch(corner_3_2, up, right, corner_3_2 + move_left + move_up, right, up, -1)
            stitch(corner_2_2, left, down, corner_2_2 + move_left + move_up, down, left, 1)
            stitch(corner_0_1, left, down, corner_3_3 + move_up, down, right, -1)
            stitch(corner_0_1, up, right, corner_3_0 + move_left, up, left, 2)
            stitch(corner_0_2 + move_up, down, right, corner_3_3 + move_left + move_up, down, left, 2)
            stitch(corner_3_0 + move_left, right, down, corner_4_3 + move_left + move_up, right, up, 2)


        if 0:
            the_map = [line.replace("#", ".") for line in the_map]
            cube_34 = (cube_height * 3) // 4
                # 5 center, go around right
            instructions = [(cube_half+1, "L"), (cube_half+1, "R"), (cube_height * 3 + cube_34, "L")]
                # 5 center, go around left
            instructions = [(cube_half+1, "L"), (cube_half+1, "L"), (cube_height * 3 + cube_34, "L")]
                # 0 center, go around left
            instructions = [(cube_half+1, "R"), (cube_half+1, "R"), (cube_height * 3 + cube_34, "L")]
                # 0 center, go around right
            instructions = [(cube_half+1, "R"), (cube_half+1, "L"), (cube_height * 3 + cube_34, "L")]
                # 0 top center, go around right
            instructions = [(cube_half+1, "R"), (cube_height * 3 + cube_34, "L")]
                # 0 top center, go around left
            instructions = [(cube_half+1, "L"), (cube_height * 3 + cube_34, "L")]
                # 1 top center, go around left
            instructions = [(cube_height + cube_half+1, "L"), (cube_height * 3 + cube_34, "L")]
                # 1 top center, go around right
            instructions = [(cube_height + cube_half+1, "R"), (cube_height * 3 + cube_34, "L")]
        else:
            fixup_links_for_walls(links)


        if 0:
            print_vis_link_map(links, left)
            print_vis_link_map(links, right)
            print_vis_link_map(links, up)
            print_vis_link_map(links, down)
#            print_vis_link_map(links, rotation)
            print_vis_link_map(links, face)
        facing = 0
        adjust = movements[facing]
#        ics(top_positions)
#        ics(left_positions[0])
#        ics(top_positions[left_positions[0]])
        start = left_positions[0], top_positions[left_positions[0]]
        x, y = start
        ic(start)

        movement_map = [list(line) for line in the_map]
        points = set()
#        print("\n".join(repr_m(movement_map[:60])),"\n")

        for n, (cnt, direction) in enumerate(instructions):
            adjust = movements[facing]

            if n < 10:
                ic(n, cnt, direction, facing, x, y)

            for s in range(cnt):
                points.add(Point(x, y))
#                position += adjust
                link = links[y][x]
                rotation = rotations[y][x]
                assert link, ic.format(s, x, y, facing)
                old_face = faces[y][x]
                movement_map[y][x] = arrows[facing]
#                new_x, new_y = link[facing]

#                if link[rotation] and old_face != faces[new_y][new_x]:
#                    ics(x, y, link[facing], link[rotation])

#                if n < 2 and s < 5:
#                    ic(s, x, y, facing, new_x, new_y, rotation, rotation[facing])

                new_p = link[facing]

                if new_p:
                    x, y = link[facing]
                    facing = (facing + rotation[facing]) % 4

                new_face = faces[y][x]


#                if new_face != old_face:
#                    facing = (facing + link[rotation]) % 4


            movement_map[y][x] = arrows[facing]
            facing = (facing + rotation_chars[direction]) % 4
#            ics(n, facing, position)

#            if n < 10:
#                print("\n".join(repr_m(movement_map)),"\n")

#        print("\n".join(the_map))
        print("\n".join(repr_m(movement_map)))
#        print("\n".join(get_vis_map(points)))
        ics(x, y, facing)
#        print("\n".join(repr_m(movement_map[:60])),"\n")
        result = (y + 1) * 1000 + (x + 1) * 4 + facing
            # 181067 is too high
            # 131384 is too high
            # 49549 is too high
            # 39k something is too low
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
