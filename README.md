# advent-of-code-python
My solutions to the [Advent of Code](https://adventofcode.com) puzzles. They use the `aocd` library to automatically fetch puzzle inputs. Some solutions are command line scripts (the scripts fodler), some are **JupyterLab** notebooks (the notebooks folder). Some are in both formats.



# Setup Instructions

1\. Clone the Repository


```
git clone https://github.com/cdbassett/advent-of-code-python.git
```


2\. Install Dependencies

It is recommended to use a virtual environment. 


```
# Change to the root folder of the project
cd advent-of-code-python

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install the required packages and make the utilties modules available
pip install -e . 
```

If you also want to use the notebooks, you will need to install JupyterLab and Jupytext:

```
pip install jupyterlab jupytext
```

Standard Jupyter Notebooks (`.ipynb`) contain heavy JSON metadata and output data, making Git diffs messy. To solve this, this repository uses **Jupytext** to pair every notebook with a standard Python script (`.py`).

*   **Coding:** Open and edit the `.ipynb` files interactively in JupyterLab. If there is no `.ipynb`, open the `.py` file instead.
*   **Saving:** JupyterLab automatically saves a mirrored `.py` file alongside it.
*   **Version Control:** Only the clean, human-readable `.py` files are tracked in Git. 


3\. Configure Your Session Token

The `aocd` package needs your Advent of Code session cookie to download your personalized inputs. 

- Open your browser and log into [Advent of Code](https://adventofcode.com).

- From the terminal, use this utlity which is part of the aocd package:

```
$ aocd-token > ~/.config/aocd/token
```

For further instructions and alternative methods to set up the session token, see:

[Advent of Code Data](https://github.com/wimglenn/advent-of-code-data#quickstart)

