import marimo

__generated_with = "0.13.13"
app = marimo.App(width="medium")


@app.cell
def _():
    from collections import defaultdict

    import marimo as mo
    from icecream import ic
    from functional import seq
    from colorama import Fore, Style

    import seq_extensions
    import aoc_utils
    from aoc_utils import get_aocd_example, split_example, insert_sample_functions, get_aocd_data
    import timer_utils
    return (
        defaultdict,
        get_aocd_data,
        get_aocd_example,
        insert_sample_functions,
        seq,
        split_example,
    )


@app.cell
def _(get_aocd_example):
    example = get_aocd_example()
    #example
    return (example,)


@app.cell
def _(example, split_example):
    sample_data1s = split_example(example)
    sample_data2s = sample_data1s
    return sample_data1s, sample_data2s


@app.cell
def _(seq):
    def parse_line(line):
        return line.split("-")

    def parse_data(inp):
        return seq(inp.strip().split("\n")).map(parse_line).list()
    return (parse_data,)


@app.cell
def _():
    def simple_nodes(connections):
        return [f"{node}: {','.join(conns)}" for node, conns in connections.items()]

    def get_path_desc(path):
        return ",".join(path)
    return


@app.cell
def _(defaultdict, islower):
    def setup(parsed):
        start_node = "start"
        end_node = "end"
        connections = defaultdict(set)

        # don't bother with connections back to start
        for a, b in parsed:
            # problem conditions state that can visit big caves unlimited times, so both upper would meean can get stuck
            assert b,islower() or a.islower() 
        
            if b != start_node:
                connections[a].add(b)
            
            if a != start_node:
                connections[b].add(a)
        #ics(simple_nodes(connections))
        return start_node, end_node, connections
    return (setup,)


@app.cell
def _(parse_data, print_result, setup):
    def traverse_path1(node, end_node, connections, paths, path, visited):
        if node.islower():
            if node in visited:
                return
            else:
                visited.add(node)

        path.append(node)

        if node == end_node:
    #            ics(get_path_desc(path))
            paths.append(path)
        else:
            for neighbor in connections[node]:
                traverse_path1(neighbor, end_node, connections, paths, path[:], set(visited))

    def process(parsed):
        start_node, end_node, connections = setup(parsed)
        paths = []
        traverse_path1(start_node, end_node, connections, paths, [], set())
    #    path_desc = [get_path_desc(path) for path in paths]
    #        ics(path_desc)
    #        ics(simple_nodes(paths[0]))
        return len(paths)

    def part1(inp):
        parsed = parse_data(inp)
        result = process(parsed)
        print_result(result)
    return (part1,)


@app.cell
def _(parse_data, print_result, setup):
    # one small cave may be visited twice
    def traverse_path2(node, end_node, connections, paths, path, visited, small_cave=None):
        if node.islower():
            if node in visited:
                if small_cave:
                    return
                else:
                    small_cave = node
            else:
                visited.add(node)

        path.append(node)

        if node == end_node:
    #            ics(get_path_desc(path))
            paths.append(path)
        else:
            for neighbor in connections[node]:
                traverse_path2(neighbor, end_node, connections, paths, path[:], set(visited), small_cave)

    def process2(parsed):
        start_node, end_node, connections = setup(parsed)
        paths = []
        traverse_path2(start_node, end_node, connections, paths, [], set())
    #    path_desc = [get_path_desc(path) for path in paths]
    #        ics(path_desc)
    #        ics(simple_nodes(paths[0]))
        return len(paths)

    def part2(inp):
        parsed = parse_data(inp)
        result = process2(parsed)
        print_result(result)
    return (part2,)


@app.cell
def _(
    insert_sample_functions,
    part1,
    part2,
    print_preface_notebook,
    sample_data1s,
    sample_data2s,
):
    insert_sample_functions(False, globals())
    print_preface_notebook()

    for sample_data1 in sample_data1s:
        part1(sample_data1)

    for sample_data2 in sample_data2s:
        part2(sample_data2)
    return


@app.cell
def _(
    get_aocd_data,
    insert_sample_functions,
    part1,
    part2,
    print_preface_notebook,
):
    real_inp = get_aocd_data()
    insert_sample_functions(True, globals())
    print_preface_notebook()
    part1(real_inp)
    part2(real_inp)
    return


if __name__ == "__main__":
    app.run()
