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
    'update-week-status': {
        'task': 'web.tasks.update_week_status',
        'schedule': crontab(minute=1, hour=0),
    },
    'update-weekcdsch-status': {
        'task': 'web.tasks.update_weekcdsch_status',
        'schedule': crontab(minute=1, hour=0),
    },
    'update-weekber-status': {
        'task': 'web.tasks.update_weekber_status',
        'schedule': crontab(minute=1, hour=0),
    },
    'update-weekf2-status': {
        'task': 'web.tasks.update_weekf2_status',
        'schedule': crontab(minute=1, hour=0),
    },
    'update-weekf3-status': {
        'task': 'web.tasks.update_weekf3_status',
        'schedule': crontab(minute=1, hour=0),
    },
    'update-weekf4-status': {
        'task': 'web.tasks.update_weekf4_status',
        'schedule': crontab(minute=1, hour=0),
    },
}
