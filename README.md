<div align="center">

<h1>brickbox.io</h1>

[![Code Quality](https://github.com/brickbox-io/brickbox/actions/workflows/pylint.yml/badge.svg)](https://github.com/brickbox-io/brickbox/actions/workflows/pylint.yml) &nbsp;
[![Script Check](https://github.com/brickbox-io/brickbox/actions/workflows/shellcheck.yml/badge.svg)](https://github.com/brickbox-io/brickbox/actions/workflows/shellcheck.yml) &nbsp;
[![Django CI](https://github.com/brickbox-io/brickbox/actions/workflows/Dajango.yml/badge.svg)](https://github.com/brickbox-io/brickbox/actions/workflows/Dajango.yml)

</div>

## Table of Contents

- [Table of Contents](#table-of-contents)
- [What is brickbox.io?](#what-is-brickbox.io)
- [Getting Started](#getting-Started)
- [Continuous Integration (CI)](#continuous-integration)
- [Continuous Deployment (CD)](#continuous-deployment)
- [Directory Structure](#directory-structure)
- [Definitions](#definitions)

## What is brickbox.io?

[brickbox.io](brickbox.io) is an artificial intelligence (AI) infrastructure provider and management platform. The goal of brickbox.io is to connection individuals working on the latest in cutting edge technology with the hardware they need to rain AI models.

The web interface is built on the [Django](https://www.djangoproject.com/) framework.

## Getting Started

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install software-properties-common -y
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.10 -y
sudo apt install nginx -y

sudo apt-get install python3.10-venv -y
python3.10 -m venv env

source env/bin/activate
python -m pip install -r requirements.txt
```

To update requirements.txt after a new package is installed

```bash
python3 -m pip freeze -l > requirements.txt
```

### Deploy

[Uvicorn](https://www.uvicorn.org/) is used as the ASGI server to provide async capabilities. When changes are made use ```systemctl restart gunicorn``` to update the service.

### Static Files

Files including images and .js are servered from the location specified in Nginx. Rull the command ```python3 manage.py collectstatic``` to automaticly copy static files from the project directory to the location specified in the settings folder.

## Dashboard Framework

https://www.creative-tim.com/live/black-dashboard-django

https://appseed.us/admin-dashboards/django-dashboard-black <br>

https://docs.appseed.us/products/django-dashboards/black-dashboard
<br>
https://demos.creative-tim.com/black-dashboard-django/docs/1.0/getting-started/getting-started-django.html

## Continuous Integration

To facilitate the rapid integration of new code the brickbox.io DevOps process includes a set of continuous integration tools. These tools are a combination of both best practices and enforced code policies with the aid of GitHub Actions.

## Admin & Monitoring

### Service Status

To quickly see that services are operational the app [django-health-check](https://github.com/KristianOellegaard/django-health-check) has been added.

## Directory Structure

```default
.
├── .github             # CI/CD using GitHub Actions and other functions.
├── bb_accounts         # User account creation and management.
├── bb_api              # API framework and endpoints.
├── bb_dashboard        # Main user interfaces.
├── bb_data             # Contains the database model definitions.
├── bb_public           # Any publicly accessible landing/info pages.
├── bb_tasks            # Task management framework, celery.
├── bb_vm               # Virtual machine component.
├── brickbox            # Django project settings and configuration.
├── django_dash_black   # Main website dashboard.
└── puller              # Internal CI/CD tools.
```

## Definitions

**Colocation Client** <br>
Represents an idividual or entity that owns one or more servers located within brickbox. A client can be controlled by one or more users. A "client" is singular while their servers/units can be plural.

**Colocation Owner** <br>
The user that owns the colocation client.
