#!/bin/bash
# shellcheck disable=SC1091,SC2086


# ---------------------------------------------------------------------------- #
#                                 Pulls Updates                                #
# ---------------------------------------------------------------------------- #
git pull --no-edit


# ---------------------------------------------------------------------------- #
#                            System Update/Updgrade                            #
# ---------------------------------------------------------------------------- #

# sudo apt-get update -y && sudo apt-get upgrade -y


# ---------------------------------------------------------------------------- #
#                                Update Packages                               #
# ---------------------------------------------------------------------------- #
. /opt/brickbox/bbenv/bin/activate

# PIP
python -m pip install --upgrade pip

# Install or Update Required Packages
/opt/brickbox/bbenv/bin/python3.10 pip install --force-reinstall --upgrade -r requirements.txt


# ---------------------------------------------------------------------------- #
#                                    Deploy                                    #
# ---------------------------------------------------------------------------- #
python /opt/brickbox/manage.py collectstatic --noinput --clear
python /opt/brickbox/manage.py migrate


# ---------------------------------------------------------------------------- #
#                                Update Services                               #
# ---------------------------------------------------------------------------- #
python /opt/brickbox/manage.py update_services

# ---------------------------------------------------------------------------- #
#                               Restart Services                               #
# ---------------------------------------------------------------------------- #
systemctl restart gunicorn
