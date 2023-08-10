from celery import shared_task
from django.utils import timezone
from .models import Week, WeekCDSCH, WeekBER, WeekF2, WeekF3, WeekF4, CinemaWeek


@shared_task
def update_active_field():
    today = timezone.now().date()
    models = [CinemaWeek, Week, WeekCDSCH, WeekBER, WeekF2, WeekF3, WeekF4]  # Список ваших моделей
    for model in models:
        weeks = model.objects.filter(start_date__lte=today, end_date__gte=today)
        weeks.update(active=True)
        weeks.exclude(active=True).update(active=False)
