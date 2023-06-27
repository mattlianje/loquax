#!/bin/bash

# Get the directory of this script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# Define the local path to your Loquax project
LOCAL_PATH="$DIR/webapp"

# Define the remote path to the project
REMOTE_PATH="/var/www/loquax"
VENV_PATH="${REMOTE_PATH}/venv"

# Create the remote directory if it doesn't already exist
ssh root@nargothrond.xyz "mkdir -p $REMOTE_PATH"

# Copy your project to the remote server
scp -r $LOCAL_PATH/* root@nargothrond.xyz:$REMOTE_PATH

# SSH into nargothrond and setup the Python environment
ssh root@nargothrond.xyz "
    # Navigate to the project directory
    cd ${REMOTE_PATH} ;

    # Check if the venv exists, if not create it
    if [ ! -d \"${VENV_PATH}\" ]; then
        python3.11 -m venv ${VENV_PATH} || echo 'Failed to create virtual environment' ;
    else
        echo 'Virtual environment already exists' ;
    fi ;

    # Activate the virtual environment
    source ${VENV_PATH}/bin/activate ;

    # Refresh the requirements
    pip install --upgrade pip ;
    pip install -r requirements.txt ;
"