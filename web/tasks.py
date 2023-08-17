from celery import shared_task
from django.utils import timezone


@shared_task
def update_cinema_week_status():
    from .models import CinemaWeek
    current_date = timezone.now().date()
    cinema_weeks = CinemaWeek.objects.all()

    for cinema_week in cinema_weeks:
        if cinema_week.start_date <= current_date <= cinema_week.end_date:
            cinema_week.active = True
        else:
            cinema_week.active = False
        cinema_week.save()


@shared_task
def update_week_status():
    from .models import Week
    current_date = timezone.now().date()
    weeks = Week.objects.all()

    for week in weeks:
        if week.start_date <= current_date <= week.end_date:
            week.active = True
        else:
            week.active = False
        week.save()


@shared_task
def update_weekcdsch_status():
    from .models import WeekCDSCH
    current_date = timezone.now().date()
    weekscdsh = WeekCDSCH.objects.all()

    for weekcdsch in weekscdsh:
        if weekcdsch.start_date <= current_date <= weekcdsch.end_date:
            weekcdsch.active = True
        else:
            weekcdsch.active = False
        weekcdsch.save()


@shared_task
def update_weekber_status():
    from .models import WeekBER
    current_date = timezone.now().date()
    weeksber = WeekBER.objects.all()

    for weekber in weeksber:
        if weekber.start_date <= current_date <= weekber.end_date:
            weekber.active = True
        else:
            weekber.active = False
        weekber.save()


@shared_task
def update_weekf2_status():
    from .models import WeekF2
    current_date = timezone.now().date()
    weeksf2 = WeekF2.objects.all()

    for weekf2 in weeksf2:
        if weekf2.start_date <= current_date <= weekf2.end_date:
            weekf2.active = True
        else:
            weekf2.active = False
        weekf2.save()


@shared_task
def update_weekf3_status():
    from .models import WeekF3
    current_date = timezone.now().date()
    weeksf3 = WeekF3.objects.all()

    for weekf3 in weeksf3:
        if weekf3.start_date <= current_date <= weekf3.end_date:
            weekf3.active = True
        else:
            weekf3.active = False
        weekf3.save()


@shared_task
def update_weekf4_status():
    from .models import WeekF4
    current_date = timezone.now().date()
    weeksf4 = WeekF4.objects.all()

    for weekf4 in weeksf4:
        if weekf4.start_date <= current_date <= weekf4.end_date:
            weekf4.active = True
        else:
            weekf4.active = False
        weekf4.save()
