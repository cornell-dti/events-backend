# views.py
# Jessica Zhao, Adit Gupta, Arnav Ghosh
# 21st June 2018

from boto.s3.connection import S3Connection
from boto.s3.key import Key

import dateutil.parser

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.template import loader
from django.utils import timezone
from django.conf import settings

from rest_framework.renderers import JSONRenderer
from rest_framework import status
from rest_framework.response import Response

from .models import Org, Event, Location, Tag, Media
from .serializers import EventSerializer, LocationSerializer, OrgSerializer, TagSerializer, UpdatedEventsSerializer, UpdatedOrgSerializer

import os

def eventDetail(request,event_id):
    event_set = Event.objects.get(pk=event_id)
    serializer = EventSerializer(event_set,many=False)
    return JsonResponse(serializer.data,status=status.HTTP_200_OK,safe=False)

def locationDetail(request,location_id):
    location_set = Location.objects.get(pk=location_id)
    serializer = LocationSerializer(location_set,many=False)
    return JsonResponse(serializer.data,status=status.HTTP_200_OK,safe=False)

def orgDetail(request,org_id):
    org_set = Org.objects.get(pk=org_id)
    serializer = OrgSerializer(org_set,many=False)
    return JsonResponse(serializer.data,status=status.HTTP_200_OK,safe=False)

def changesInOrgs(request, in_timestamp):
    old_timestamp = dateutil.parser.parse(in_timestamp)
    outdated_orgs, all_deleted = outdatedOrgs(old_timestamp)
    #json_orgs = JSONRenderer().render(OrgSerializer(outdated_orgs, many = True).data)
    json_orgs = OrgSerializer(outdated_orgs, many = True).data
    serializer = UpdatedOrgSerializer({"updated":json_orgs, "deleted":all_deleted, "timestamp":timezone.now()})
    return JsonResponse(serializer.data,status=status.HTTP_200_OK,safe=False)

def outdatedOrgs(in_timestamp):
    org_updates = Org.history.filter(history_date__gte = in_timestamp)
    org_updates = org_updates.distinct('id').order_by('id')

    org_list = org_updates.values_list('id', flat = True).order_by('id')
    #TODO: What if not in list
    changed_orgs = Org.objects.filter(pk__in=org_list)
    present_pks = Org.objects.filter(pk__in = org_list).values_list('pk', flat = True)
    all_deleted_pks = list(set(org_list).difference(set(present_pks)))
    return changed_orgs, all_deleted_pks
                                               
def changesInEvents(request, in_timestamp, start_time, end_time):
    old_timestamp = dateutil.parser.parse(in_timestamp)
    start_time = dateutil.parser.parse(start_time)
    end_time = dateutil.parser.parse(end_time)
    outdated_events, all_deleted = outdatedEvents(old_timestamp, start_time, end_time)
    json_events = EventSerializer(outdated_events, many = True).data
    serializer = UpdatedEventsSerializer({"updated":json_events, "deleted":all_deleted, "timestamp":timezone.now()})
    return JsonResponse(serializer.data,status=status.HTTP_200_OK,safe=False)

def outdatedEvents(in_timestamp, start_time, end_time):
    history_set = Event.history.filter(history_date__gte = in_timestamp)
    unique_set  = history_set.distinct('id').order_by('id')

    pks = unique_set.values_list('id', flat=True).order_by('id')
    #TODO: What if not in list
    changed_events = Event.objects.filter(pk__in = pks, start_date__gte = start_time, end_date__lte =  end_time)
    present_pks = Event.objects.filter(pk__in = pks).values_list('pk', flat = True)
    all_deleted_pks = list(set(pks).difference(set(present_pks)))
    return changed_events, all_deleted_pks

def singleTag(request, tag_id):
    return JsonResponse(tagDetail(tag_id).data,status=status.HTTP_200_OK,safe=False)

def allTags(request):
    return JsonResponse(tagDetail(tag_id, True).data,status=status.HTTP_200_OK,safe=False)

def tagDetail(tag_id, all=False):
    tags = Tag.objects.all()
    if all:
        serializer = TagsSerializer(tags, many=True)
    else:
        serialzer = TagsSerializer(tags.filter(pk = tag_id), many=False)

    return serializer

def imageDetail(request, img_id):
    media = Media.objects.filter(pk = img_id)[0].file.name 
    name, extension = os.path.splitext(media)
    s3 = S3Connection(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
    s3bucket = s3.get_bucket(settings.AWS_STORAGE_BUCKET_NAME)
    s3key = s3bucket.get_key(media)
    response = HttpResponse(s3key.read(), status=status.HTTP_200_OK, content_type="image/" + extension) #what if its not jpg
    response['Content-Disposition'] = 'inline; filename=' + media
    return response