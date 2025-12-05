#!/bin/bash

# Run tests.
python3 -m coverage run -m unittest discover tst
python3 -m coverage report -m

# todo Start the program.
