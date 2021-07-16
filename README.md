[![Code Quality](https://github.com/brickbox-io/brickbox/actions/workflows/pylint.yml/badge.svg)](https://github.com/brickbox-io/brickbox/actions/workflows/pylint.yml)

Framework: Django

# Getting Started

```bash
apt-get install python3-venv -y
python3 -m venv brickbox-env

source brickbox-env/bin/activate
python3 -m pip install -r requirements.txt
```

To update requirements.txt after a new package is installed

```bash
python3 -m pip freeze -l >requirements.txt
```

# Deploy

[Uvicorn](https://www.uvicorn.org/) is used as the ASGI server to provide async capabilities.

## Static Files

Files including images and .js are servered from the location specified in Nginx. Rull the command ```python3 manage.py collectstatic``` to automaticly copy static files from the project directory to the location specified in the settings folder.

## Dashboard Framework

https://appseed.us/admin-dashboards/django-dashboard-black
https://docs.appseed.us/products/django-dashboards/black-dashboard
