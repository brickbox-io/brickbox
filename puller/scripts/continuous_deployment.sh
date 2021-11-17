#!/bin/bash

# ---------------------------------------------------------------------------- #
#                            System Update/Updgrade                            #
# ---------------------------------------------------------------------------- #

sudo apt-get update -y && sudo apt-get upgrade -y &

# ---------------------------------------------------------------------------- #
#                                Update Packages                               #
# ---------------------------------------------------------------------------- #

# PIP
python3 -m pip install --upgrade pip

# Django
python3 -m pip install -U Django

# Install or Update Required Packages
pip3 install --force-reinstall --upgrade -r requirements.txt

# Pulls the latest code from GitHub, performs the required steps then deploys.

git pull --no-edit
python3 /opt/brickbox/manage.py collectstatic --noinput --clear
python3 /opt/brickbox/manage.py migrate


# ---------------------------------------------------------------------------- #
#                                Update Services                               #
# ---------------------------------------------------------------------------- #

python3 /opt/brickbox/manage.py update_services

# ---------------------------------------------------------------------------- #
#                               Restart Services                               #
# ---------------------------------------------------------------------------- #
systemctl restart gunicorn
