#!/bin/bash

# Exit on error
set -e

echo "🐍 Setting up Python 3.11.11 for publishing..."
# First save current Python version
CURRENT_VERSION=$(pyenv version-name)
echo "Current Python version: $CURRENT_VERSION"

# Switch to Python 3.11.11
pyenv local 3.11.11
PY311_PATH=$(pyenv which python)
echo "Using Python binary: $PY311_PATH"

# Create and activate a virtual environment
rm -rf venv_publish
"$PY311_PATH" -m venv venv_publish
source venv_publish/bin/activate

# Verify Python version
python --version

echo "📦 Installing required tools..."
pip install --upgrade setuptools wheel twine

echo "🧹 Cleaning up previous builds..."
rm -rf dist/ build/ splore_sdk.egg-info/

# Check if there are any existing wheel files
echo "🔍 Checking for existing wheel files..."
if ls dist/*.whl 2>/dev/null; then
    echo "⚠️ Found existing wheel files. Cleaning up..."
    rm dist/*.whl
fi

# Check if there are any existing source distributions
if ls dist/*.tar.gz 2>/dev/null; then
    echo "⚠️ Found existing source distributions. Cleaning up..."
    rm dist/*.tar.gz
fi

echo "📦 Building distribution packages..."
python setup.py sdist bdist_wheel

echo "📦 Uploading to PyPI..."
python -m twine upload dist/*

# Deactivate the virtual environment
deactivate

# Clean up
rm -rf venv_publish

# Restore original Python version
pyenv local $CURRENT_VERSION

echo "✅ Successfully published to PyPI!"
