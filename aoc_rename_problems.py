import marimo

__generated_with = "0.13.13"
app = marimo.App(width="full")


@app.cell
def _(mo):
    mo.md(r"""We want to rename advent of code problem files that have no problem description in their filename.""")
    return


@app.cell
def _():
    import os
    import glob
    import re
    import functools

    import marimo as mo
    from functional import seq # https://github.com/EntilZha/PyFunctional
    from icecream import ic

    import seq_extensions
    from aoc_utils import get_aocd_example # this includes adding c:\ut to sys.path
    return functools, get_aocd_example, glob, mo, os, re, seq


@app.cell
def _(os):
    def get_base_key(f):
        return os.path.splitext(os.path.basename(f))[0]
    return (get_base_key,)


@app.cell
def _(os):
    def strip_ext(f):
        return os.path.splitext(f)[0]
    return (strip_ext,)


@app.cell
def _(re):
    re_parse_fn = re.compile(r"aoc_(\d+)_(\d+)(.*)")
    return (re_parse_fn,)


@app.cell
def _(re_parse_fn, strip_ext):
    def match(s):
        return (m := re_parse_fn.match(strip_ext(s))) and m.groups((1,2,3))
    return (match,)


@app.cell
def _(get_base_key, glob, seq, strip_ext):
    python_files = glob.glob(r"**\aoc_*.py", recursive=True)
    notebook_files = glob.glob(r"**\aoc_*.ipynb", recursive=True)
    notebook_set = seq(notebook_files).map(strip_ext).set()
    python_files = [f for f in python_files if strip_ext(f) not in notebook_set]

    # we don't want to count script files that were saved by jupytext
    python_only = sorted(seq(python_files).map(get_base_key).set() - seq(notebook_files).map(get_base_key).set())
    notebook_only = sorted(seq(notebook_files).map(get_base_key).set() - seq(python_files).map(get_base_key).set())
    return notebook_only, notebook_set, python_only


@app.cell
def _(match, python_only, seq):
    list(zip(python_only,seq(python_only).map(match)))
    return


@app.cell
def _(notebook_only):
    notebook_only
    return


@app.cell
def _(functools, get_aocd_example, match, re):
    re_parse_desc = re.compile(r"Day \d+: (.+)")

    def cleanup_desc(s):
        return s.lower().replace(" ", "_").replace("-", "_")

    def get_problem_desc(day, year):
        ex = get_aocd_example(day, year)
        return (m := re_parse_desc.match(ex[0].strip(" -"))) and cleanup_desc(m.group(1))
        #return ex[0]
    
    @functools.cache
    def get_problem_desc_from_filename(fn):
        return (m := match(fn)) and get_problem_desc(*m[0:2])
    return (get_problem_desc_from_filename,)


@app.cell
def _(get_base_key, get_problem_desc_from_filename, match, notebook_set, os):
    problems_missing_title = [f for f in notebook_set if (m := match(get_base_key(f))) and not m[2]]
    notebook_rename_paths = list(zip(problems_missing_title, ["_".join((f, get_problem_desc_from_filename(get_base_key(f)))) for f in notebook_rename_paths]))
    #notebook_rename_paths

    for org_fn, new_fn in notebook_rename_paths:
        os.rename(org_fn+".py", new_fn+".py")
        os.rename(org_fn+".ipynb", new_fn+".ipynb")

    #list(zip(problems_missing_title,seq(problems_missing_title).map(get_problem_desc_from_filename)))
    return


if __name__ == "__main__":
    app.run()
