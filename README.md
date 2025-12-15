# Hawk Dove

### Overview
For Complex Systems 511 (Theory of Complex Systems) at the University of Michigan final project. This repository contains code to play around with and simulate the game of hawk-dove, informally described in terms of the four available strategies:
- Hawks: Always attack, fighting for maximal reward.
- Doves: Peacefully coexist, run away if attacked.
- Bullies: Attack at first, but retreat if challenged.
- Retaliators: Peacefully coexist, but fight back if attacked.

### Setup
> Create a python virual environment and install the editable hawkdove module. Commands:
- `python -m venv venv` (this creates a virtual environment)
- `pip install -r requirements.txt` (this installs dependencies)
- `pip install -e .` (this installs the hawkdove module in editable mode)
- `python -m pytest tests/unit_tests.py` or just `python tests/unit_tests.py` to check everything.
- `python hawkdove/simulation.py -h 0.75 -d 0.25 -b 0 -r 0 -i 5000 -t "Plot Title"` to run the code. Change command line arguments to generate different scenarios.

### Structure
- hawkdove/
  - This is a module with the core functionality of the hawkdove game. Anything fundamental to how the game works should live here.
- miscellaneous/
  - This is for random testing and exploration. Anything interesting can live here.
- tests/
  - This is for testing (currently just unit tests, potentially integration/sim tests later).
- pyproject.toml
  - This file defines the hawkdove module that we use.
- requirements.txt
  - This file makes all dependencies in the project explicit.
- .gitignore
  - This defines files that will not be tracked by git (add anything local/private to this file).
- .pytest_cache, hawkdove.egg_info, venv
  - Python utilities.
