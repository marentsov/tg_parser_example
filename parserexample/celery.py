import os
from celery import Celery

# where our settings.py is
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "parserexample.settings")
# creating Celery app
app = Celery("parserexample")
# startings Celery settings from settings.py with prefix CELERY
app.config_from_object("django.conf:settings", namespace="CELERY")
# searching for tasks in Django apps automatically
app.autodiscover_tasks()
