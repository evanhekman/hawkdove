# Hawk Dove

### Overview
For Complex Systems 511 (Theory of Complex Systems) at the University of Michigan final project. This repository contains 

### Setup
> Create a python virual environment and install the editable hawkdove module. Commands:
- `python -m venv venv` (this creates a virtual environment)
- `pip install requirements.txt` (this installs dependencies)
- `pip install -e .` (this installs the hawkdove module in editable mode)
- `python -m pytest tests/unit_tests.py` or just `python tests/unit_tests.py` to check everything.

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
