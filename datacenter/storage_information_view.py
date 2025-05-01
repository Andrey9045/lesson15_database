from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render
from datacenter.models import get_duration
from datacenter.models import format_duration
from django.utils import timezone
import datetime

def storage_information_view(request):
    # Программируем здесь
    visits = Visit.objects.filter(leaved_at=None) 
    non_closed_visits = [
        {
            'who_entered': str(visit.passcard),
            'entered_at': visit.entered_at.strftime('%d %B %Y г. %H:%M'),
            'duration': format_duration(get_duration(visit), seconds_in_minute=60, seconds_in_hour=3600),
        }
    for visit in visits]
    context = {
        'non_closed_visits': non_closed_visits,  # не закрытые посещения
    }
    return render(request, 'storage_information.html', context)
