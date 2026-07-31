import marimo

__generated_with = "0.13.13"
app = marimo.App(width="full")


@app.cell
def _(mo):
    mo.md(r"""We want to determine which files have script version only and notebook version only""")
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
    return glob, mo, os, seq


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
def _(get_base_key, glob, seq, strip_ext):
    python_files = glob.glob(r"**\aoc_*.py", recursive=True)
    notebook_files = glob.glob(r"**\aoc_*.ipynb", recursive=True)
    notebook_set = seq(notebook_files).map(strip_ext).set()
    python_files = [f for f in python_files if strip_ext(f) not in notebook_set]

    # we don't want to count script files that were saved by jupytext
    python_only = sorted(seq(python_files).map(get_base_key).set() - seq(notebook_files).map(get_base_key).set())
    notebook_only = sorted(seq(notebook_files).map(get_base_key).set() - seq(python_files).map(get_base_key).set())
    return notebook_only, python_only


@app.cell
def _(python_only):
    python_only
    return


@app.cell
def _(notebook_only):
    notebook_only
    return


if __name__ == "__main__":
    app.run()
