from django.db import models
from django.utils import timezone
import datetime
from .functions_for_the_database import get_duration, format_duration, is_visit_long 

class Passcard(models.Model):
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    passcode = models.CharField(max_length=200, unique=True)
    owner_name = models.CharField(max_length=255)

    def __str__(self):
        if self.is_active:
            return self.owner_name
        return f'{self.owner_name} (inactive)'


class Visit(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    passcard = models.ForeignKey(Passcard, on_delete=models.CASCADE)
    entered_at = models.DateTimeField()
    leaved_at = models.DateTimeField(null=True)

    def __str__(self):
        return '{user} entered at {entered} {leaved}'.format(
            user=self.passcard.owner_name,
            entered=self.entered_at,
            leaved=(
                f'leaved at {self.leaved_at}'
                if self.leaved_at else 'not leaved'
            )
        )

def get_duration(visit):
    local_time=timezone.localtime(visit.entered_at)
    if visit.leaved_at:
        local_time_leaved=timezone.localtime(visit.leaved_at).replace(microsecond=0)
        duration = local_time_leaved-local_time
    else:
        now = timezone.now().replace(microsecond=0)   
        duration = now-local_time
        
    return duration


def format_duration(duration):
    total_seconds = int(duration.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    format_duration = f"{hours:02}:{minutes:02}:{seconds:02}"

    return format_duration

def is_visit_long(visit, minutes=60):
    return get_duration(visit)>datetime.timedelta(minutes=60)


    