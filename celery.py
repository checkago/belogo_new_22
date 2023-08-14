import os
from datetime import timedelta

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "belogo_new.settings")
app = Celery("belogo_new")
app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'update-cinema-week-active': {
        'task': 'myapp.tasks.update_cinema_week_active',
        'schedule': timedelta(hours=1),
    },
}
