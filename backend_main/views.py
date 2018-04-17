from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from reversion.models import Version

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
    version_set = Version.objects.get_for_model(models.Event, model_db=None)
