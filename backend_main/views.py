from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader

from .models import Org

from rest_framework import status

# Create your views here.

def eventDetail(request,event_id):
    event_set = Event.objects.get(pk=event_id)
    serializer = EventSerialize(event_set,many=False)
    return JsonResponse(serializer.data,status=status.HTTP_200_OK,safe=False)
