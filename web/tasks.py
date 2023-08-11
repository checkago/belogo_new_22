from celery import shared_task
from datetime import datetime
from .models import Week, WeekCDSCH, WeekBER, WeekF2, WeekF3, WeekF4, CinemaWeek


@shared_task
def update_cinema_week_active():
    today = datetime.now().date()
    cinema_weeks = CinemaWeek.objects.all()
    for cinema_week in cinema_weeks:
        if cinema_week.start_date <= today <= cinema_week.end_date:
            cinema_week.active = True
        else:
            cinema_week.active = False
        cinema_week.save()
