# advent-of-code-python
My solutions to the [Advent of Code](https://adventofcode.com) puzzles. They use the `aocd` library to automatically fetch puzzle inputs. Some solutions are command line scripts, some are **JupyterLab** notebooks. Some are in both formats. 

Standard Jupyter Notebooks (`.ipynb`) contain heavy JSON metadata and output data, making Git diffs messy. To solve this, this repository uses **Jupytext** to pair every notebook with a standard Python script (`.py`).

*   **Coding:** Open and edit the `.ipynb` files interactively in JupyterLab. If there is no `.ipynb`, open the `.py` file instead.
*   **Saving:** JupyterLab automatically saves a mirrored `.py` file alongside it.
*   **Version Control:** Only the clean, human-readable `.py` files are tracked in Git. 


# Setup Instructions

1\. Clone the Repository

bash

```
git clone https://github.com/cdbassett/advent-of-code-python.git
cd advent-of-code-python
```


2\. Install Dependencies

It is recommended to use a virtual environment. 

bash

```
# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install the required packages
pip install -r requirements.txt
```

Use code with caution.

3\. Configure Your Session Token

The `aocd` package needs your Advent of Code session cookie to download your personalized inputs. 

- Open your browser and log into Advent of Code.

- Open the browser Developer Tools (F12) and go to the **Application** (Chrome) or **Storage** (Firefox) tab.

- Under **Cookies**, select `https://adventofcode.com`.

- Find the cookie named `session` and copy its long hex string value. 

On Linux / macOS: 

Add the token to your shell profile (e.g., `~/.bashrc` or `~/.zshrc`): 

bash

```
export AOC_SESSION="your_session_cookie_here"
```

Use code with caution.

On Windows (Command Prompt): 

cmd

```
setx AOC_SESSION "your_session_cookie_here"
```

Use code with caution.

Alternative (.env file): 

If you prefer using a `.env` file, create a file named `.env` in the root of this project: 

text

```
AOC_SESSION=your_session_cookie_here
```

Use code with caution.

_Note: Ensure your code loads this environment variable (e.g., using `python-dotenv`) before importing `aocd`._