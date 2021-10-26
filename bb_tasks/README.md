# brickbox.io Task Management & Scheduler App

The bb_tasks app contains the core functionality of the Celery framework. The tasks can be called by any other app and set to run at specific intervals.

## Setup/Installation Requirements

```bash
apt-get install rabbitmq-server
```

A single config file is used to provide the settings for both of the celery related service files.

### Config Files

```/etc/conf.d/celery```

### Service Files

Celery service file is located at ```/etc/systemd/system/celery.service```
Celery beat service file is located at ```/etc/systemd/system/celerybeat.service```

## Result Monitoring

https://github.com/celery/django-celery-results
