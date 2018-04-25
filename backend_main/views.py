from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader


from .models import Org, Event

#from rest_framework import status

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

def outdatedEvents(timestamp, start_time, end_time):
    history_set = Event.history.filter(history_date__gte = timestamp)

def changesInOrgs(timestamp, start_time, end_time):
    outdated_orgs = outdatedOrgs(timestamp)
    
def outdatedOrgs(timestamp, start_time,end_time):
    org_updates = Org.history.filter(timestamp__gte = timestamp);
    org_updates = org_updates.distinct('id');
    
    org_list = org_updates.values_list('id');
    changed_orgs = Org.objects.filter(pk__in=org_list, start_date__gte=start_time,end_date__gte=end_time);
                                               
    
    
    # version_set = Version.objects.get_for_model(models.Event, model_db=None)
    # changes = set()
    # for obj in version_set:
    #     revised_obj = Revision.get(pk = obj.reversion)
    #     if revised_obj.date_created >= timestamp:
    #         change.add(int(obj.object_id))
    # return list(changes)
