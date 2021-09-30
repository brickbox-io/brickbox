#!/bin/bash

# Pulls the latest code from GitHub, performs the required steps then deploys.

git reset --hard origin/release
python3 /opt/brickbox/manage.py collectstatic --noinput --clear
python3 /opt/brickbox/manage.py migrate
systemctl restart gunicorn
