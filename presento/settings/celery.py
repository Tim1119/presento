import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'presento.base')

app = Celery('presento')
app.config_from_object('django.conf:base', namespace='CELERY')
app.autodiscover_tasks()
