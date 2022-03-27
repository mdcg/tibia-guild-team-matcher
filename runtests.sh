#!/bin/bash

export PYTHONPATH="${PWD}/core/"
python -m pytest tests/
