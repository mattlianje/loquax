#!/bin/bash

# Gets the directory of this script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

LOCAL_PATH="$DIR/webapp"
REMOTE_PATH="/var/www/loquax"
VENV_PATH="${REMOTE_PATH}/venv"
REMOTE_HOST="root@nargothrond.xyz"

create_remote_directory() {
    echo "Creating remote directory..."
    ssh "$REMOTE_HOST" "mkdir -p $REMOTE_PATH"
}

copy_project_to_remote() {
    echo "Copying project to remote server..."
    scp -r "$LOCAL_PATH"/* "$REMOTE_HOST":"$REMOTE_PATH"
}

setup_python_environment() {
    echo "Setting up Python environment on remote server..."
    ssh "$REMOTE_HOST" "
        cd ${REMOTE_PATH} ;
        if [ ! -d \"${VENV_PATH}\" ]; then
            python3.10 -m venv ${VENV_PATH} || { echo 'Failed to create virtual environment'; exit 1; } ;
        else
            echo 'Virtual environment already exists' ;
        fi ;
        source ${VENV_PATH}/bin/activate ;
        pip install --upgrade pip ;
        pip install -r requirements.txt ;
    "
}

deploy_project() {
    create_remote_directory
    copy_project_to_remote
    setup_python_environment
    echo "Deployment complete."
}

deploy_project
