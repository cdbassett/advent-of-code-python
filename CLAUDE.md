# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

- **Run a solution script:** `python aoc_YYYY_DD_problem_name.py`
- **Dependencies:** Uses `advent-of-code-data` (`aocd`), `colorama`, `functional` (PyFunctional), `iteration-utilities`, `pyperclip`, `icecream`, `z3-solver`, `numpy`.

## High-Level Architecture

- **Problem Scripts & Jupytext:** Each puzzle solution is contained in an independent Python script named `aoc_YYYY_DD_description.py`. Since Jupytext is used, `.ipynb` files should be ignored; only the matching `.py` files should be considered in operations.
- **Utilities & Helpers:** 
  - `aoc_base.py`: Template base script used for running aoc puzzles, parsing input, and handling parts 1 and 2.
  - `aoc_utils.py`: Core utility functions, imports, setup for `aocd` (Advent of Code Data), and common helper bindings.
  - `aoc_gen_files.py`: Helper script for scaffolding new puzzle files.
- **Input Fetching:** Uses the `aocd` library (`advent-of-code-data`) to automatically fetch puzzle inputs. Requires an `AOC_SESSION` environment variable or session token configuration.
