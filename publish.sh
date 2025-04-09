#!/bin/bash

# Exit on error
set -e

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
twine upload dist/*

echo "✅ Successfully published to PyPI!"
