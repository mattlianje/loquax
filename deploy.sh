#!/bin/bash

get_current_version() {
    python3 setup.py --version
}

ask_version_bump_part() {
    read -p "Which part to bump (major/minor/patch)? " part
    echo $part
}

validate_input() {
    if ! [[ "$1" =~ ^(major|minor|patch)$ ]]; then
        echo -e "Invalid input. Please enter 'major', 'minor', or 'patch'."
        exit 1
    fi
}

install_bumpversion() {
    if ! command -v bumpversion &> /dev/null; then
        echo "Installing bumpversion..."
        pip3 install --upgrade bumpversion
    fi
}

bump_version() {
    bumpversion --current-version $1 $2 setup.py
}

install_twine() {
    if ! command -v twine &> /dev/null; then
        echo "Installing twine..."
        pip3 install --upgrade twine
    fi
}

build_package() {
    echo "Cleaning up the dist directory..."
    rm -rf dist/*
    echo "Building the package..."
    python3 setup.py sdist bdist_wheel
}

upload_package() {
    echo "Uploading the package to PyPI..."
    twine upload dist/*
}

main() {
    echo -e "\n Package Version Bumper and Uploader \n"

    local current_version=$(get_current_version)
    echo "Current version: $current_version"

    local part=$(ask_version_bump_part)
    validate_input $part

    install_bumpversion
    bump_version $current_version $part

    local new_version=$(get_current_version)
    echo "New version: $new_version"

    install_twine
    build_package
    upload_package

    echo -e "\n Package uploaded successfully! \n"
}

main