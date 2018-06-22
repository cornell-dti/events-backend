# views.py
# Jessica Zhao, Adit Gupta, Arnav Ghosh
# 21st June 2018

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.template import loader
from django.utils import timezone

from rest_framework.renderers import JSONRenderer
from rest_framework import status

from .models import Org, Event
from .serializers import EventSerializer, LocationSerializer, OrgSerializer,
                        UpdatedEventsSerializer, UpdatedOrgSerializer

import dateutil.parser

def eventDetail(request,event_id):
    event_set = Event.objects.get(pk=event_id)
    serializer = EventSerialize(event_set,many=False)
    return JsonResponse(serializer.data,status=status.HTTP_200_OK,safe=False)

def locationDetail(request,location_id):
    location_set = Location.objects.get(pk=location_id)
    serializer = EventSerialize(location_set,many=False)
    return JsonResponse(serializer.data,status=status.HTTP_200_OK,safe=False)

def orgDetail(request,org_id):
    org_set = Location.objects.get(pk=org_id)
    serializer = EventSerializer(org_set,many=False)
    return JsonResponse(serializer.data,status=status.HTTP_200_OK,safe=False)

def changesInOrgs(timestamp):
    old_timestamp = dateutil.parser.parse(timestamp)
    outdated_orgs, all_deleted = outdatedOrgs(old_timestamp)
    json_orgs = JSONRenderer().render(OrgSerializer(outdated_orgs, many = True).data)
    serializer = UpdatedOrgSerializer(updated = json_orgs, deleted = all_deleted, timestamp = timezone.now())
    return JsonResponse(serializer.data,status=status.HTTP_200_OK,safe=False)

def outdatedOrgs(timestamp):
    org_updates = Org.history.filter(timestamp__gte = timestamp)
    org_updates = org_updates.distinct('id')

    org_list = org_updates.values_list('id')
    #TODO: What if not in list
    changed_orgs = Org.objects.filter(pk__in=org_list)
    present_pks = Org.objects.filter(pk__in = org_list).value_list('pk', flat = True)
    all_deleted_pks = list(set(org_list).difference(set(present_pks)))
    return changed_orgs, all_deleted_pks
                                               
def changesInEvents(timestamp, start_time, end_time):
    old_timestamp = dateutil.parser.parse(timestamp)
    start_time = dateutil.parser.parse(start_time)
    end_time = dateutil.parser.parse(end_time)
    outdated_events, all_deleted = outdatedEvents(old_timestamp, start_time, end_time)
    json_events = JSONRenderer().render(EventSerializer(outdated_events, many = True).data)
    serializer = UpdatedEventsSerializer(updated = json_events, deleted = all_deleted, timestamp = timezone.now())
    return JsonResponse(serializer.data,status=status.HTTP_200_OK,safe=False)

def outdatedEvents(timestamp, start_time, end_time):
    history_set = Event.history.filter(history_date__gte = timestamp)
    unique_set  = history_set.distinct('id')

    pks = unique_set.values_list('id', flat=True).order_by('id')
    #TODO: What if not in list
    changed_events = Event.objects.filter(pk__in = pks, start_date__gte = start_time, end_date__lte =  end_time)
    present_pks = Event.objects.filter(pk__in = pks).value_list('pk', flat = True)
    all_deleted_pks = list(set(pks).difference(set(present_pks)))
    return changed_events, all_deleted_pks