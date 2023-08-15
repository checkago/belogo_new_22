from belogo_new.celery import shared_task
from django.utils import timezone
from .models import CinemaWeek


@shared_task
def update_cinema_week_status():
    current_date = timezone.now().date()
    cinema_weeks = CinemaWeek.objects.all()

    for cinema_week in cinema_weeks:
        if cinema_week.start_date <= current_date <= cinema_week.end_date:
            cinema_week.active = True
        else:
            cinema_week.active = False
        cinema_week.save()
