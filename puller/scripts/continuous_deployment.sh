#!/bin/bash

# Pulls the latest code from GitHub, performs the required steps then deploys.

git pull
python3 /opt/brickbox/manage.py collectstatic --noinput
python3 /opt/brickbox/manage.py migrate
systemctl restart gunicorn
