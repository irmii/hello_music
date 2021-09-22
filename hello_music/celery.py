from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from decouple import config

# set the default Django settings module for the 'celery' program.
dj_settings = config('DJANGO_SETTINGS_MODULE', default='hello_music.settings')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', dj_settings)

app = Celery('hello_music')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
