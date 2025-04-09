#!/bin/bash

# Set Python 3.7.17 as the active version
pyenv local 3.7.17

# Install test dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/
