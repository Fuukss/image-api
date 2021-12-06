from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Default Django settings module for Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

app = Celery('app', broker='redis://redis:6379/0')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


