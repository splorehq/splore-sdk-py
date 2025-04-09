#!/bin/bash

# Define Python versions to test
PYTHON_VERSIONS=("3.7.17" "3.8.0" "3.9.0" "3.10.0" "3.11.0" "3.12.0" "3.13.0")

# Save current Python version
CURRENT_VERSION=$(pyenv version-name)

# Function to run tests for a specific version
run_tests() {
    local version=$1
    echo "Testing with Python $version..."
    pyenv local $version
    python -m pip install -r requirements-dev.txt
    python -m pytest tests/ || exit 1
}

# Run tests for each version
for version in "${PYTHON_VERSIONS[@]}"; do
    run_tests $version
    echo "Passed tests for Python $version"
done

# Restore original Python version
pyenv local $CURRENT_VERSION
