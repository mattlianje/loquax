i#!/bin/bash

# Get the latest version of the package
current_version=$(python3 setup.py --version)
echo "Current version: $current_version"

# Ask user for the part to bump
read -p "Which part to bump (major/minor/patch)? " part

# Check the input
if [[ "$part" != "major" && "$part" != "minor" && "$part" != "patch" ]]; then
    echo "Invalid part. Please enter 'major', 'minor' or 'patch'."
    exit 1
fi

# Install bumpversion if not installed
if ! command -v bumpversion &> /dev/null; then
    echo "bumpversion not found. Installing..."
    pip3 install --upgrade bumpversion
fi

# Bump the version
bumpversion --current-version $current_version $part setup.py

# Get the new version
new_version=$(python3 setup.py --version)
echo "New version: $new_version"

# Install twine if not installed
if ! command -v twine &> /dev/null; then
    echo "twine not found. Installing..."
    pip3 install --upgrade twine
fi

# Clean up the dist directory
echo "Cleaning up the dist directory..."
rm -rf dist/*

# Build the package
python3 setup.py sdist bdist_wheel

# Upload the package to PyPI
twine upload dist/*