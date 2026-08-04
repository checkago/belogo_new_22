from datetime import date, timedelta

from django import template

register = template.Library()

DAY_ABBR = {
    'понедельник': 'ПН',
    'вторник': 'ВТ',
    'среда': 'СР',
    'четверг': 'ЧТ',
    'пятница': 'ПТ',
    'суббота': 'СБ',
    'воскресенье': 'ВС',
    'пн': 'ПН',
    'вт': 'ВТ',
    'ср': 'СР',
    'чт': 'ЧТ',
    'пт': 'ПТ',
    'сб': 'СБ',
    'вс': 'ВС',
}

WEEKDAY_ORDER = {
    'понедельник': 0,
    'вторник': 1,
    'среда': 2,
    'четверг': 3,
    'пятница': 4,
    'суббота': 5,
    'воскресенье': 6,
    'пн': 0,
    'вт': 1,
    'ср': 2,
    'чт': 3,
    'пт': 4,
    'сб': 5,
    'вс': 6,
}

MONTHS_GENITIVE = {
    1: 'января',
    2: 'февраля',
    3: 'марта',
    4: 'апреля',
    5: 'мая',
    6: 'июня',
    7: 'июля',
    8: 'августа',
    9: 'сентября',
    10: 'октября',
    11: 'ноября',
    12: 'декабря',
}


def _day_key(name):
    return (name or '').strip().lower()


def _day_abbr(name):
    key = _day_key(name)
    return DAY_ABBR.get(key, str(name)[:2].upper() if name else '')


def _weekday_index(day):
    key = _day_key(getattr(day, 'name', ''))
    if key in WEEKDAY_ORDER:
        return WEEKDAY_ORDER[key]
    day_date = getattr(day, 'date', None)
    if day_date:
        return day_date.weekday()
    return 99


def _resolve_date(day, week_start):
    """Дата из поля дня или вычисленная от начала недели + имени дня."""
    day_date = getattr(day, 'date', None)
    if day_date:
        return day_date
    if not week_start:
        return None
    idx = _weekday_index(day)
    if idx > 6:
        return None
    start_wd = week_start.weekday()
    return week_start + timedelta(days=(idx - start_wd) % 7)


def _format_day_title(day, week_start=None):
    abbr = _day_abbr(getattr(day, 'name', ''))
    day_date = _resolve_date(day, week_start)
    if day_date:
        return f"{abbr} {day_date.day}/{day_date.month:02d}"
    return abbr


def _format_date_range(start, end):
    if not start:
        return ''
    if isinstance(start, str) or isinstance(end, str):
        return f"{start} - {end}" if end else str(start)
    month = MONTHS_GENITIVE.get(end.month if end else start.month, '')
    if end and (start.month != end.month or start.year != end.year):
        start_month = MONTHS_GENITIVE.get(start.month, '')
        return f"{start.day} {start_month} - {end.day} {month}"
    if end and start.day != end.day:
        return f"{start.day}-{end.day} {month}"
    return f"{start.day} {month}"


def _events_list(weekday):
    return list(weekday.events.all().order_by('start_time'))


def _pad_row(days, week_start=None):
    prepared = []
    max_count = 0
    for day in days:
        events = _events_list(day)
        prepared.append({
            'day': day,
            'title': _format_day_title(day, week_start),
            'events': events,
        })
        max_count = max(max_count, len(events))
    if max_count == 0:
        max_count = 1
    for item in prepared:
        pad = max_count - len(item['events'])
        item['slots'] = item['events'] + [None] * pad
    return prepared


@register.simple_tag
def schedule_date_range(start_date, end_date):
    return _format_date_range(start_date, end_date)


@register.simple_tag
def schedule_day_title(weekday):
    return _format_day_title(weekday)


@register.simple_tag
def schedule_address_lines(address):
    from django.utils.html import escape
    from django.utils.safestring import mark_safe

    if not address:
        return ''
    text = str(address).strip()
    if ',' in text:
        head, tail = text.split(',', 1)
        html = f"{escape(head.strip())},<br>{escape(tail.strip())}"
    else:
        html = escape(text)
    return mark_safe(html)


@register.simple_tag
def schedule_layout_rows(weekdays, start_date=None):
    """
    Сетка брендбука: Пн–Сб (2×3) или Пн–Вс (3+4).
    Дни всегда в порядке Пн→Вс; пустые даты считаются от start_date.
    """
    days = list(weekdays)
    if not days:
        return []

    week_start = start_date if isinstance(start_date, date) else None
    days.sort(key=_weekday_index)

    def is_sunday(day):
        return _weekday_index(day) == 6

    def is_effectively_empty(day):
        events = _events_list(day)
        if not events:
            return True
        if len(events) == 1:
            name = (events[0].name or '').strip().lower()
            return 'выходн' in name
        return False

    use_seven = False
    if len(days) >= 7:
        sunday = next((d for d in days if is_sunday(d)), None)
        if sunday and not is_effectively_empty(sunday):
            use_seven = True
        elif not any(is_sunday(d) for d in days):
            use_seven = True

    if use_seven:
        ordered = days[:7]
        return [
            {'cols': 3, 'days': _pad_row(ordered[:3], week_start)},
            {'cols': 4, 'days': _pad_row(ordered[3:7], week_start)},
        ]

    ordered = [d for d in days if not (is_sunday(d) and is_effectively_empty(d))]
    ordered = ordered[:6]
    if len(ordered) <= 3:
        return [{'cols': len(ordered) or 1, 'days': _pad_row(ordered, week_start)}]
    return [
        {'cols': 3, 'days': _pad_row(ordered[:3], week_start)},
        {'cols': min(3, len(ordered) - 3), 'days': _pad_row(ordered[3:6], week_start)},
    ]
