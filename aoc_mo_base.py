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


@app.function
def setup(parsed):
    return parsed


@app.cell
def _(parse_data, print_result):
    def process(parsed):
        values = setup(parsed)
        return None

    def part1(inp):
        parsed = parse_data(inp)
        result = process(parsed)
        print_result(result)
    return (part1,)


@app.cell
def _(parse_data, print_result):
    def process2(parsed):
        values = setup(parsed)
        return None
        return None

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
