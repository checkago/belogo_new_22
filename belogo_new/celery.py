import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'belogo_new.settings')

app = Celery('belogo_new')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.beat_schedule = {
    'update-cinema-week-status': {
        'task': 'web.tasks.update_cinema_week_status',
        'schedule': crontab(minute=1, hour=0),  # change to `crontab(minute=0, hour=0)` if you want it to run daily at midnight
    },
}
