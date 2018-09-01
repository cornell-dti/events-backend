# views.py
# Jessica Zhao, Adit Gupta, Arnav Ghosh
# 21st June 2018

from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.utils import timezone
from django.contrib.auth.models import User

from rest_framework.renderers import JSONRenderer
from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import permissions

from .models import Org, Event, Location, Tag
from .permissions import IsOwnerOrReadOnly
from .serializers import EventSerializer, LocationSerializer, OrgSerializer, TagSerializer, UpdatedEventsSerializer, UpdatedOrgSerializer
from .forms import OrgForm, TagForm, EventForm, LocationForm


import dateutil.parser

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
        serializer = TagSerializer(tags, many=True)
    else:
        serialzer = TagSerializer(tags.filter(pk = tag_id), many=False)

    return serializer

def post_detail_org(request, pk):
    post = get_object_or_404(Org, pk=pk)
    return render(request, 'post_detail_org.html', {'post': post})

def post_detail_tag(request, pk):
    post = get_object_or_404(Tag, pk=pk)
    return render(request, 'post_detail_tag.html', {'post': post})

def post_detail_event(request, pk):
    post = get_object_or_404(Event, pk=pk)
    return render(request, 'post_detail_event.html', {'post': post})

def post_detail_location(request, pk):
    post = get_object_or_404(Location, pk=pk)
    return render(request, 'post_detail_location.html', {'post': post})

def post_org(request):
    if request.method == "POST":
        form = OrgForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('post_detail_org', pk=post.pk)
    else:
        form = OrgForm()
    return render(request, 'post_edit.html', {'form': form})

def post_tag(request):
    if request.method == "POST":
        form = TagForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('post_detail_tag', pk=post.pk)
    else:
        form = TagForm()
    return render(request, 'post_edit.html', {'form': form})

def post_event(request):
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('post_detail_event', pk=post.pk)
    else:
        form = EventForm()
    return render(request, 'post_edit.html', {'form': form})

def post_location(request):
    if request.method == "POST":
        form = LocationForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('post_detail_location', pk=post.pk)
    else:
        form = LocationForm()
    return render(request, 'post_edit.html', {'form': form})

def post_edit_org(request, pk):
    post = get_object_or_404(Org, pk=pk)
    if request.method == "POST":
        form = OrgForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('post_detail_org', pk=post.pk)
    else:
        form = OrgForm(instance=post)
    return render(request, 'post_edit.html', {'form': form})

def post_event_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class Authentication(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(owner = self.request.user)


