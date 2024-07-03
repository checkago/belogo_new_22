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


@shared_task
def update_weekb5_status():
    from .models import WeekB5
    current_date = timezone.now().date()
    weeksb5 = WeekB5.objects.all()

    for weekb5 in weeksb5:
        if weekb5.start_date <= current_date <= weekb5.end_date:
            weekb5.active = True
        else:
            weekb5.active = False
        weekb5.save()


@shared_task
def update_weekcgbt_status():
    from .models import WeekCGBT
    current_date = timezone.now().date()
    weekscgbt = WeekCGBT.objects.all()

    for weekcgbt in weekscgbt:
        if weekcgbt.start_date <= current_date <= weekcgbt.end_date:
            weekcgbt.active = True
        else:
            weekcgbt.active = False
        weekcgbt.save()


@shared_task
def update_weekbcj_status():
    from .models import WeekBCJ
    current_date = timezone.now().date()
    weeksbcj = WeekBCJ.objects.all()

    for weekbcj in weeksbcj:
        if weekbcj.start_date <= current_date <= weekbcj.end_date:
            weekbcj.active = True
        else:
            weekbcj.active = False
        weekbcj.save()


@shared_task
def update_weekbscd_status():
    from .models import WeekBSCD
    current_date = timezone.now().date()
    weeksbscd = WeekBSCD.objects.all()

    for weekbscd in weeksbscd:
        if weekbscd.start_date <= current_date <= weekbscd.end_date:
            weekbscd.active = True
        else:
            weekbscd.active = False
        weekbscd.save()


@shared_task
def update_weekyb_status():
    from .models import WeekYB
    current_date = timezone.now().date()
    weeksyb = WeekYB.objects.all()

    for weekyb in weeksyb:
        if weekyb.start_date <= current_date <= weekyb.end_date:
            weekyb.active = True
        else:
            weekyb.active = False
        weekyb.save()


@shared_task
def update_weekdb_status():
    from .models import WeekDB
    current_date = timezone.now().date()
    weeksdb = WeekDB.objects.all()

    for weekdb in weeksdb:
        if weekdb.start_date <= current_date <= weekdb.end_date:
            weekdb.active = True
        else:
            weekdb.active = False
        weekdb.save()


@shared_task
def update_weeknmb_status():
    from .models import WeekNMB
    current_date = timezone.now().date()
    weeksnmb = WeekNMB.objects.all()

    for weeknmb in weeksnmb:
        if weeknmb.start_date <= current_date <= weeknmb.end_date:
            weeknmb.active = True
        else:
            weeknmb.active = False
        weeknmb.save()


@shared_task
def update_weekcsb_status():
    from .models import WeekCSB
    current_date = timezone.now().date()
    weekscsb = WeekCSB.objects.all()

    for weekcsb in weekscsb:
        if weekcsb.start_date <= current_date <= weekcsb.end_date:
            weekcsb.active = True
        else:
            weekcsb.active = False
        weekcsb.save()


@shared_task
def update_weekssb_status():
    from .models import WeekSSB
    current_date = timezone.now().date()
    weeksssb = WeekSSB.objects.all()

    for weekssb in weeksssb:
        if weekssb.start_date <= current_date <= weekssb.end_date:
            weekssb.active = True
        else:
            weekssb.active = False
        weekssb.save()


@shared_task
def update_weekfsb_status():
    from .models import WeekFSB
    current_date = timezone.now().date()
    weeksfsb = WeekFSB.objects.all()

    for weekfsb in weeksfsb:
        if weekfsb.start_date <= current_date <= weekfsb.end_date:
            weekfsb.active = True
        else:
            weekfsb.active = False
        weekfsb.save()


@shared_task
def update_weekppb_status():
    from .models import WeekPPB
    current_date = timezone.now().date()
    weeksppb = WeekPPB.objects.all()

    for weekppb in weeksppb:
        if weekppb.start_date <= current_date <= weekppb.end_date:
            weekppb.active = True
        else:
            weekppb.active = False
        weekppb.save()


@shared_task
def update_weekdbt_status():
    from .models import WeekDBT
    current_date = timezone.now().date()
    weeksdbt = WeekDBT.objects.all()

    for weekdbt in weeksdbt:
        if weekdbt.start_date <= current_date <= weekdbt.end_date:
            weekdbt.active = True
        else:
            weekdbt.active = False
        weekdbt.save()


@shared_task
def update_weeknab_status():
    from .models import WeekNAB
    current_date = timezone.now().date()
    weeksnab = WeekNAB.objects.all()

    for weeknab in weeksnab:
        if weeknab.start_date <= current_date <= weeknab.end_date:
            weeknab.active = True
        else:
            weeknab.active = False
        weeknab.save()


@shared_task
def update_weeknb_status():
    from .models import WeekNB
    current_date = timezone.now().date()
    weeksnb = WeekNB.objects.all()

    for weeknb in weeksnb:
        if weeknb.start_date <= current_date <= weeknb.end_date:
            weeknb.active = True
        else:
            weeknb.active = False
        weeknb.save()


