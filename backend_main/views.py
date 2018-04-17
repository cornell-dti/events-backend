from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from reversion.models import Version, Revision


from .models import Org

from rest_framework import status

# Create your views here.

def eventDetail(request,event_id):
    event_set = Event.objects.get(pk=event_id)
    serializer = EventSerialize(event_set,many=False)
    return JsonResponse(serializer.data,status=status.HTTP_200_OK,safe=False)

def locationDetail(request,location_id):
    location_set = Location.objects.get(pk=location_id)
    serializer = EventSerialize(event_set,many=False)
    return JsonResponse(serializer.data,status=status.HTTP_200_OK,safe=False)

def changesInEvents(timestamp, start_time, end_time):
    outdated_events = outdatedEvents(timestamp)


def outdatedEvents(timestamp):
    version_set = Version.objects.get_for_model(models.Event, model_db=None)
    changes = set()
    for obj in version_set:
        revised_obj = Revision.get(pk = obj.reversion)
        if revised_obj.date_created >= timestamp:
            change.add(int(obj.object_id))
    return list(changes)
