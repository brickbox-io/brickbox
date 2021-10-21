#!/bin/bash

# ---------------------------------------------------------------------------- #
#                                Update Packages                               #
# ---------------------------------------------------------------------------- #

# Django
python3 -m pip install -U Django

# Install or Update Required Packages
pip install -r requirements.txt

# Pulls the latest code from GitHub, performs the required steps then deploys.

git pull --no-edit
python3 /opt/brickbox/manage.py collectstatic --noinput --clear
python3 /opt/brickbox/manage.py migrate


# ---------------------------------------------------------------------------- #
#                               Restart Services                               #
# ---------------------------------------------------------------------------- #
systemctl restart celery.service
systemctl restart gunicorn
