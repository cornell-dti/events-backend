# views.py
# Arnav Ghosh, Jessica Zhao, Jill Wu, Adit Gupta
# 17th Sept. 2018

from boto.s3.connection import S3Connection
from boto.s3.key import Key

import dateutil.parser

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.utils import timezone
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.utils.decorators import method_decorator

from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.utils import timezone
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.template import loader


from rest_framework.renderers import JSONRenderer

from .permissions import IsOwnerOrReadOnly
from .forms import OrgForm, TagForm, EventForm, LocationForm

from google.oauth2 import id_token
from google.auth.transport import requests

from rest_framework.renderers import JSONRenderer
from rest_framework import permissions, status, generics
from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Org, Event, Event_Org, Location, Tag, Media, Attendance, UserID
from .serializers import (EventSerializer, LocationSerializer, OrgSerializer,
                            TagSerializer, UpdatedEventsSerializer, UpdatedOrgSerializer, UserSerializer)
from django.core.mail import send_mail
import logging
import os

#=============================================================
#                   EVENT INFORMATION
#=============================================================

class EmailDetail(APIView):
    def get(self, request, org_email, org_name, name, net_id, link, format=None):
        send_mail('New Application',
                  "Organization Email: " + org_email + "\n" +
                  "Organization Name: " + org_name + "\n" +
                  "Creator Name: " + name + "\n" +
                  "NetID: " + net_id + "\n" +
                  "Organization Link: " + link,
                  'noreply@cornell.dti.org', ['sz329@cornell.edu'])
        return HttpResponse(status=204)

class EventDetail(APIView):
    #TODO: alter classes to token and admin?
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request, event_id, format=None):
        event_set = Event.objects.get(pk=event_id)
        serializer = EventSerializer(event_set,many=False)
        return JsonResponse(serializer.data,status=status.HTTP_200_OK)

class IncrementAttendance(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        event = Event.objects.filter(pk=request.data["event"])[0]
        user = Token.objects.filter(pk=extractToken(request.META.get("HTTP_AUTHORIZATION")))[0].user
        attendingSet = Attendance.objects.filter(user_id = user, event_id = event)

        if not attendingSet.exists():
            attendance = Attendance(user_id = user, event_id = event)
            attendance.save()
            event.num_attendees += 1
            event.save()

        return HttpResponse(status=status.HTTP_200_OK)
        #TODO: if exists then response

#=============================================================
#                   LOCATION INFORMATION
#=============================================================

class SingleLocationDetail(APIView):

    #TODO: alter classes to token and admin?
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request, location_id, format=None):
        location_set = Location.objects.get(pk=location_id)
        serializer = LocationSerializer(location_set,many=False)
        return JsonResponse(serializer.data,status=status.HTTP_200_OK)

class AllLocationDetail(APIView):
    #TODO: alter classes to token and admin?
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request, format=None):
        location_set = Location.objects.all()
        serializer = LocationSerializer(location_set,many=True)
        return JsonResponse(serializer.data,status=status.HTTP_200_OK, safe=False)

#=============================================================
#                ORGANIZATION INFORMATION
#=============================================================

class OrgDetail(APIView):
    #TODO: alter classes to token and admin?
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request, org_id, format=None):
        org_set = Org.objects.get(pk=org_id)
        serializer = OrgSerializer(org_set,many=False)
        return JsonResponse(serializer.data,status=status.HTTP_200_OK)

class OrgEvents(APIView):
    #TODO: alter classes to token and admin?
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request, organizer_id, format=None):
        org = Org.objects.get(pk = int(organizer_id))
        org_events_pks = Event_Org.objects.filter(org_id = org).values_list('event_id', flat=True)
        event_set = Event.objects.filter(pk__in=org_events_pks)
        serializer = EventSerializer(event_set,many=True)
        return JsonResponse(serializer.data,status=status.HTTP_200_OK, safe = False)

#=============================================================
#                    TAG INFORMATION
#=============================================================

class SingleTagDetail(APIView):
    #TODO: alter classes to token and admin?
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request, tag_id, format=None):
        tag = Tag.objects.get(id = tag_id)
        serializer = TagSerializer(tag, many=False)
        return JsonResponse(serializer.data,status=status.HTTP_200_OK)

class AllTagDetail(APIView):
    #TODO: alter classes to token and admin?
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request, format=None):
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        return JsonResponse(serializer.data,status=status.HTTP_200_OK)

#=============================================================
#                           FEEDS
#=============================================================

class OrgFeed(APIView):
    #TODO: alter classes to token and admin?
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request, in_timestamp, format=None):
        old_timestamp = dateutil.parser.parse(in_timestamp)
        outdated_orgs, all_deleted = outdatedOrgs(old_timestamp)
        #json_orgs = JSONRenderer().render(OrgSerializer(outdated_orgs, many = True).data)
        json_orgs = OrgSerializer(outdated_orgs, many = True).data
        serializer = UpdatedOrgSerializer({"updated":json_orgs, "deleted":all_deleted, "timestamp":timezone.now()})
        return JsonResponse(serializer.data,status=status.HTTP_200_OK)

def outdatedOrgs(in_timestamp):
    org_updates = Org.history.filter(history_date__gte = in_timestamp)
    org_updates = org_updates.distinct('id').order_by('id')

    org_list = org_updates.values_list('id', flat = True).order_by('id')
    #TODO: What if not in list
    changed_orgs = Org.objects.filter(pk__in=org_list)
    present_pks = Org.objects.filter(pk__in = org_list).values_list('pk', flat = True)
    all_deleted_pks = list(set(org_list).difference(set(present_pks)))
    return changed_orgs, all_deleted_pks

class EventFeed(APIView):
    #TODO: token authentication not working...?
    # authentication_classes = (TokenAuthentication, )
    # permission_classes = (permissions.IsAuthenticated, )

    #get event feed, parse timestamp and return events
    def get(self, request, format=None):
        in_timestamp = request.GET.get('timestamp')
        start_time = request.GET.get('start')
        end_time = request.GET.get('end')
        old_timestamp = dateutil.parser.parse(in_timestamp)
        start_time = dateutil.parser.parse(start_time)
        end_time = dateutil.parser.parse(end_time)
        outdated_events, all_deleted = outdatedEvents(old_timestamp, start_time, end_time)
        json_events = EventSerializer(outdated_events, many = True).data
        serializer = UpdatedEventsSerializer({"updated":json_events, "deleted":all_deleted, "timestamp":timezone.now()})
        return JsonResponse(serializer.data,status=status.HTTP_200_OK)

#tbh i have no idea what this function does
def outdatedEvents(in_timestamp, start_time, end_time):
    history_set = Event.history.filter(history_date__gte = in_timestamp)
    unique_set  = history_set.values_list('id', flat=True).distinct().order_by('id')
    pks = unique_set.values_list('id', flat=True).order_by('id')
    # #TODO: What if not in list
    changed_events = Event.objects.filter(pk__in = pks, start_date__gte = start_time, end_date__lte =  end_time)
    present_pks = Event.objects.filter(pk__in = pks).values_list('pk', flat = True)
    all_deleted_pks = list(set(pks).difference(set(present_pks)))
    return changed_events, all_deleted_pks

#=============================================================
#                          MEDIA
#=============================================================

def tagDetail(tag_id=0, all=False):
    tags = Tag.objects.all()
    if all:
        serializer = TagSerializer(tags, many=True)
    else:
        serializer = TagSerializer(tags.filter(pk = tag_id), many=False)

    return serializer

class ImageDetail(APIView):
    #TODO: alter classes to token and admin?
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request, img_id, format=None):
        media = Media.objects.filter(pk = img_id)[0].file.name
        name, extension = os.path.splitext(media)
        s3 = S3Connection(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
        s3bucket = s3.get_bucket(settings.AWS_STORAGE_BUCKET_NAME)
        s3key = s3bucket.get_key(media)
        response = HttpResponse(s3key.read(), status=status.HTTP_200_OK, content_type="image/" + extension) #what if its not jpg
        response['Content-Disposition'] = 'inline; filename=' + media
        return response

#=============================================================
#                        TOKENS
#=============================================================

#TODO: Different table for firebaseIDs, better practices?
class ObtainToken(APIView):
    #TODO: alter classes to token and admin?
    permission_classes = (permissions.AllowAny, )

    def get(self, request, mobile_id, format=None):

        userIDSet = UserID.objects.filter(token=mobile_id)
        if userIDSet.exists():
                return HttpResponseBadRequest("Token Already Assigned to User")
        else:
            validated, valid_info = validate_firebase(mobile_id)
            if not validated:
                return HttpResponseBadRequest("Invalid Firebase ID")

            #generate username
            username = generateUserName()
            user = User.objects.create_user(username=username,
                                            password='')
            user.set_unusable_password()
            user.save()

            newUserID = UserID(user = user, token = mobile_id)
            newUserID.save()

            #generate token
            token = Token.objects.create(user=user)
            return JsonResponse({'token': token.key}, status=status.HTTP_200_OK)



class ResetToken(APIView):
    #TODO: alter classes to token and admin?
    permission_classes = (permissions.AllowAny, )

    def get(self, request, mobile_id, format=None):
        userIDSet = UserID.objects.filter(token=mobile_id)
        if userIDSet.exists():
            userID = userIDSet[0]
            token = Token.objects.get(user = userID.user)
            return JsonResponse({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return HttpResponse("Reset Token Error")

class TagFormView(APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request):
        form = TagForm()
        return render(request, 'post_edit.html', {'form': form})

    def post(self, request):
            form = TagForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.save()
                return redirect('post_detail_tag', pk=post.pk)

class EventFormView(APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request):
        form = EventForm()
        return render(request, 'post_edit.html', {'form': form})

    def post(self, request):
        form = EventForm(request.POST)

        if form.is_valid():            
            e = Event()
            e.name = form.cleaned_data['name']
            e.description = form.cleaned_data['description']
            e.start_date = form.cleaned_data['start_date']
            e.end_date = form.cleaned_data['end_date']
            e.start_time = form.cleaned_data['start_time']
            e.end_time = form.cleaned_data['end_time']
            e.is_public = form.cleaned_data['is_public']
            e.organizer = form.cleaned_data['organizer']

            l = Location() 
            if form.cleaned_data['existing_location']:
                l = form.cleaned_data['existing_location']
                e.location = l
            elif form.cleaned_data['new_location_building']:
                l.building = form.cleaned_data['new_location_building']
                l.place_id = form.cleaned_data['new_location_placeid']
                l.save()
                e.location = l
            else:
                return redirect('post_detail_event_error.html')
            
            e.save()
            print(e)
            return redirect('post_detail_event', pk=e.pk)
    

class LocationFormView(APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request):
        form = LocationForm()
        return render(request, 'post_edit.html', {'form': form})

    def post(self, request):
        form = LocationForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('post_detail_location', pk=post.pk)

#=============================================================
#                        HELPERS
#=============================================================
def extractToken(header):
    return header[header.find(" ") + 1:]

def generateUserName():
    #HANDLE user.obects.latest is null case
    #Safe: pk < 2147483647 and max(len(username)) == 150 [16/9/2018]
    return "user{0}".format(User.objects.latest('pk').pk + 1)

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
    post = get_object_or_404(Event, pk=pk)
    if request.method == "POST":
        form = EventForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = EventForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

def validate_firebase(mobile_id):
    try:
        idinfo = id_token.verify_oauth2_token(mobile_id, requests.Request())
        return True, ""
    except Exception as e:
        return False, mobile_id

class UserList(generics.ListAPIView):
    queryset = User.objects.filter(is_staff=False)
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.filter(is_staff=False)
    serializer_class = UserSerializer


class Authentication(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    def perform_create(self, serializer): 
        serializer.save(owner = self.request.user)

class OrgFormView(APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request):
        form = OrgForm()
        return render(request, 'post_edit.html', {'form': form})

    def post(self, request):
        form = OrgForm(request.POST)
        if form.is_valid():
            o = Org()
            o.name = form.cleaned_data['name']
            o.description = form.cleaned_data['description']
            o.verified = form.cleaned_data['verified']
            o.website = form.cleaned_data['website']
            o.photo = form.cleaned_data['photo']

            o.owner = request.user

            o.save()
            return redirect('post_detail_org', pk=o.pk)


#=============================================
@csrf_exempt
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return HttpResponse(status=status.HTTP_204_NO_CONTENT)
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})
