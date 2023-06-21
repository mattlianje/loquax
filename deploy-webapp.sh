#!/bin/bash

# The directory of your Flask app on your local machine
local_app_dir=/path/to/your/app

# The directory where you want to deploy your app on the server
remote_app_dir=/path/to/deployment/dir

ssh root@nargothrond.xyz << 'ENDSSH'
  sudo apt-get update
  sudo apt-get upgrade -y

  # Check if Python 3.10 is installed, if not install it
  if ! command -v python3.10 &> /dev/null; then
    sudo apt-get install python3.10 python3.10-venv -y
  fi

  mkdir -p $remote_app_dir
  cd $remote_app_dir

  # Create and activate virtual environment
  python3.10 -m venv venv
  source venv/bin/activate

  # Install Flask and loquax in the virtual environment
  pip install Flask loquax
ENDSSH

# Copy the Flask app to the server
rsync -avz $local_app_dir/ root@nargothrond.xyz:$remote_app_dir/

ssh $user@$host << 'ENDSSH'
  cd $remote_app_dir

  # Start the Flask app
  # TODO restart the systemd service for loquax
  source venv/bin/activate
  export FLASK_APP=app.py
  flask run --host=0.0.0.0 --port=8080 &
ENDSSH