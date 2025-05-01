import datetime
from django.utils import timezone


def get_duration(visit):
    local_time = timezone.localtime(visit.entered_at)
    if visit.leaved_at:
        local_time_leaved = timezone.localtime(visit.leaved_at).replace(microsecond=0)
        duration = local_time_leaved-local_time
    else:
        now = timezone.now().replace(microsecond=0)
        duration = now-local_time     
    return duration


def format_duration(duration, seconds_in_minute=60, seconds_in_hour=3600):
    total_seconds = int(duration.total_seconds())
    hours, remainder = divmod(total_seconds, seconds_in_hour)
    minutes, seconds = divmod(remainder, seconds_in_minute)
    format_duration = f"{hours:02}:{minutes:02}:{seconds:02}"

    return format_duration


def is_visit_long(visit, minutes=60):
    return get_duration(visit) > datetime.timedelta(minutes=minutes)
