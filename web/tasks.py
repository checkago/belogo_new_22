from celery import shared_task
from django.utils import timezone
from .models import Week

@shared_task
def update_active_field():
    today = timezone.now().date()
    weeks = Week.objects.filter(start_date__lte=today, end_date__gte=today)
    weeks.update(active=True)
    weeks.exclude(active=True).update(active=False)