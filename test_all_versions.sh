#!/bin/bash

# This script runs tests on all available Python versions
# It handles Python 3.7 separately using setuptools and Python 3.8+ using PDM
set -e  # Exit on any error

# Define Python versions to test based on what's installed on this machine
ALL_VERSIONS=("3.7.17" "3.8.20" "3.9.4" "3.10.16" "3.11.11" "3.12.0" "3.12.9" "3.13.2")
AVAILABLE_VERSIONS=()

# Check if pyenv is installed
if ! command -v pyenv &> /dev/null; then
    echo "Error: pyenv is not installed. Please install pyenv to manage Python versions."
    exit 1
fi

# Save current Python version
CURRENT_VERSION=$(pyenv version-name)
echo "Current Python version: $CURRENT_VERSION"

# Check which Python versions are installed
echo "Checking installed Python versions..."
for version in "${ALL_VERSIONS[@]}"; do
    if pyenv versions | grep -q "$version"; then
        echo "✓ Python $version is installed"
        AVAILABLE_VERSIONS+=("$version")
    else
        echo "✗ Python $version is not installed"
    fi
done

if [ ${#AVAILABLE_VERSIONS[@]} -eq 0 ]; then
    echo "Error: No required Python versions are installed."
    echo "Please install at least one Python version (3.7.17 through 3.13.2) using pyenv."
    exit 1
fi

echo "Testing with available Python versions: ${AVAILABLE_VERSIONS[*]}"

# Run Python 3.7 tests if available
if [[ " ${AVAILABLE_VERSIONS[*]} " =~ " 3.7.17 " ]]; then
    echo "Running Python 3.7 tests..."
    
    # Set Python 3.7.17 as the active version and get the full path to the binary
    pyenv local 3.7.17
    PY37_PATH=$(pyenv which python)
    echo "Using Python 3.7: $PY37_PATH"

    # Clean up any previous installations
    rm -rf build/ dist/ *.egg-info venv_py37

    # Create a clean virtual environment with explicit Python 3.7 binary
    "$PY37_PATH" -m venv venv_py37
    source venv_py37/bin/activate

    # Verify we're using Python 3.7
    python --version

    # Install older pip and setuptools versions that work with Python 3.7
    pip install --upgrade pip==20.3.4 setuptools==59.8.0 wheel==0.37.1

    # Install test dependencies
    pip install pytest==7.4.4 pytest-mock==3.11.1 pydantic==1.10.8 requests==2.31.0 markdown==3.4.4 tuspy==1.1.0

    # Set environment variable to prevent pip from checking dependency conflicts
    export PIP_DISABLE_PIP_VERSION_CHECK=1

    # Install the package in development mode
    pip install --no-dependencies -e .

    # Run tests
    echo "Running tests with Python 3.7..."
    python -m pytest tests/

    # Deactivate and clean up
    deactivate
    rm -rf venv_py37
    
    echo "Python 3.7 tests completed successfully!"
else
    echo "Skipping Python 3.7 tests as Python 3.7.17 is not installed."
fi

# Prepare tox environments for other Python versions
TOX_ENVS=""
for version in "${AVAILABLE_VERSIONS[@]}"; do
    if [[ "$version" != "3.7.17" ]]; then
        case "$version" in
            "3.8.20") TOX_ENVS="${TOX_ENVS},py38" ;;
            "3.9.4") TOX_ENVS="${TOX_ENVS},py39" ;;
            "3.10.16") TOX_ENVS="${TOX_ENVS},py310" ;;
            "3.11.11") TOX_ENVS="${TOX_ENVS},py311" ;;
            "3.12.0"|"3.12.9") 
                # Just use one of the Python 3.12 versions
                if [[ ! "$TOX_ENVS" =~ ",py312" ]]; then
                    TOX_ENVS="${TOX_ENVS},py312"
                fi
                ;;
            "3.13.2") TOX_ENVS="${TOX_ENVS},py313" ;;
        esac
    fi
done

# Remove leading comma if present
TOX_ENVS=${TOX_ENVS#,}

# Run other Python versions if any are available
if [ -n "$TOX_ENVS" ]; then
    echo "Running tests for Python 3.8+ with tox environments: $TOX_ENVS"
    
    # Check if Python 3.11 is available for running tox (more stable with plugins)
    if [[ " ${AVAILABLE_VERSIONS[*]} " =~ " 3.11.11 " ]]; then
        echo "Using Python 3.11.11 to run tox (avoiding plugin compatibility issues with Python 3.13)..."
        pyenv local 3.11.11
        
        # Create a tox venv to avoid plugin issues
        if [ ! -d "tox_venv" ]; then
            python -m venv tox_venv
            source tox_venv/bin/activate
            pip install tox
            deactivate
        fi
        
        # Use the tox from our venv
        source tox_venv/bin/activate
        
        # Set all Python versions for testing
        pyenv local 3.11.11 "${AVAILABLE_VERSIONS[@]}"
        
        # Disable tox-pyenv plugin to avoid conflicts
        export TOX_DISABLE_PLUGIN="tox_pyenv"
        
        # Run tox with our settings
        tox -e "$TOX_ENVS,lint" --skip-missing-interpreters true
        
        # Clean up
        deactivate
    else
        # Fall back to using whatever Python is available
        echo "Python 3.11.11 not available, using existing Python to run tox (may encounter plugin issues)"
        pyenv local "${AVAILABLE_VERSIONS[@]}"
        export TOX_DISABLE_PLUGIN="tox_pyenv"
        tox -e "$TOX_ENVS,lint" --skip-missing-interpreters true
    fi
else
    echo "No Python 3.8+ versions available to test."
fi

# Restore original Python version
pyenv local $CURRENT_VERSION

# Clean up
if [ -d "tox_venv" ]; then
    rm -rf tox_venv
fi

echo "All tests completed! Check the above output for results."
