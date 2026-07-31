import io
import runpy
import sys
from pathlib import Path

from icecream import ic


def aoc_plugin(year, day, data):
#    print("running plugin")
    here = Path(__file__).parent
#    ic(here)

    files = list(here.glob(f"aoc_{year}_{day:02d}*.py")) + list(here.glob(f"notebooks\\{year}\\aoc_{year}_{day:02d}*.py"))
#    ic(files)

    mod_name = files[0].stem

        # if this is a notebook
    if "notebooks" in files[0].parts:
            # make module name reflect path
        mod_name = f"notebooks.{year}." + mod_name
            # put the year directory in sys.path so that imports for the year can be found
        year_dir = str(here / "notebooks" / str(year))
        if year_dir not in sys.path: sys.path.append(year_dir) # make modules in ut directory available


#    ic(mod_name)
    sys.modules.pop(mod_name, None)
    old_stdout = sys.stdout
    sys.stdout = out = io.StringIO()
    try:
        import aoc_utils
        aoc_utils.aoc_runner_data = data
        runpy.run_module(mod_name, run_name="__main__")
    finally:
        sys.stdout = old_stdout
        del aoc_utils.aoc_runner_data

    lines = [x for x in out.getvalue().splitlines() if x]
    answer_a = answer_b = None

    for line in lines:
        if line.startswith("Part 1"):
            if len(line.split()) > 2:
                answer_a = line.split()[-1]
            else:
                answer_a = ""
        elif line.startswith("Part 2"):
            if len(line.split()) > 2:
                answer_b = line.split()[-1]
            else:
                answer_b = ""

    if answer_a is not None and answer_b is not None:
        return answer_a, answer_b

    if not lines:
        return None, None

    if 0:
        if len(lines) == 1:
            answer_a = lines[0].split()[-1]
        else:
            if answer_a is None:
                answer_a = lines[-2].split()[-1]

            if answer_b is None:
                answer_b = lines[-1].split()[-1]

    return answer_a, answer_b
    return answer_a if answer_a is not None else 0, answer_b
