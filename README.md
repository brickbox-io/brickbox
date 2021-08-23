# brickbox.io Web & Dashboard

[![Django CI](https://github.com/brickbox-io/brickbox/actions/workflows/Dajango.yml/badge.svg)](https://github.com/brickbox-io/brickbox/actions/workflows/Dajango.yml)
[![Code Quality](https://github.com/brickbox-io/brickbox/actions/workflows/pylint.yml/badge.svg)](https://github.com/brickbox-io/brickbox/actions/workflows/pylint.yml)
[![Script Check](https://github.com/brickbox-io/brickbox/actions/workflows/shellcheck.yml/badge.svg)](https://github.com/brickbox-io/brickbox/actions/workflows/shellcheck.yml)
Framework: Django

## Getting Started

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

## Deploy

[Uvicorn](https://www.uvicorn.org/) is used as the ASGI server to provide async capabilities. When changes are made use ```systemctl restart gunicorn``` to update the service.

### Static Files

Files including images and .js are servered from the location specified in Nginx. Rull the command ```python3 manage.py collectstatic``` to automaticly copy static files from the project directory to the location specified in the settings folder.

## Dashboard Framework

https://www.creative-tim.com/live/black-dashboard-django

https://appseed.us/admin-dashboards/django-dashboard-black <br>

https://docs.appseed.us/products/django-dashboards/black-dashboard
<br>
https://demos.creative-tim.com/black-dashboard-django/docs/1.0/getting-started/getting-started-django.html

## Definitions

**Colocation Client** <br>
Represents an idividual or entity that owns one or more servers located within brickbox. A client can be controlled by one or more users. A "client" is singular while their servers/units can be plural.

**Colocation Owner** <br>
The user that owns the colocation client.

## Apps

| App               | Description                                 |
|-------------------|---------------------------------------------|
| bb_accounts       | User account creation and management.       |
| bb_api            | API framework and endpoints.                |
| bb_dashboard      |                                             |
| bb_public         | Any publicly accessible landing/info pages. |
| bb_tasks          | Task management framework, celery.          |
| bb_vm             | Virtual machine component.                  |
| django_dash_black | Main website dashboard.                     |
