from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render
from datacenter.models import get_duration
from datacenter.models import format_duration
from datacenter.models import is_visit_long
from django.shortcuts import get_object_or_404

def passcard_info_view(request, passcode):
    obj = get_object_or_404(Passcard, passcode=passcode)
    visits = Visit.objects.filter(passcard=obj)
    # Программируем здесь

    this_passcard_visits = [
        {
            'entered_at': str(visit.entered_at),
            'duration': format_duration(get_duration(visit)),
            'is_strange': is_visit_long(visit, minutes=60)
        }
        for visit in visits
    ]
    context = {
        'passcard': obj,
        'this_passcard_visits': this_passcard_visits
    }
    return render(request, 'passcard_info.html', context)
