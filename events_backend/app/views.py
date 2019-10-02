# views.py
# Arnav Ghosh, Jessica Zhao, Jill Wu, Adit Gupta
# 17th Sept. 2018

from boto.s3.connection import S3Connection

import dateutil.parser
import boto3

from datetime import datetime as dt

from django.conf import settings
from django.contrib.auth import login, authenticate, get_user_model
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ObjectDoesNotExist

from .permissions import IsOwnerOrReadOnly
from .forms import TagForm, EventForm, LocationForm, OrgForm, CustomUserCreationForm

from google.oauth2 import id_token
from google.auth.transport import requests

from rest_framework import permissions, status, generics
from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.views import APIView

from .models import (
    Org,
    Mobile_User,
    Event,
    Event_Org,
    Location,
    Tag,
    Media,
    Attendance,
    Event_Media,
    Event_Tags,
    Verified_Emails,
)
from .serializers import (
    EventSerializer,
    LocationSerializer,
    OrgSerializer,
    TagSerializer,
    UpdatedEventsSerializer,
    UpdatedOrgSerializer,
    UserSerializer,
)

from django.core.mail import send_mail
import os
import re

from math import ceil;

User = get_user_model()
EVENTS_PER_PAGE = 15

# =============================================================
#                    LOGIN/SIGNUP
# =============================================================


class SignUp(APIView):
    permission_classes = (permissions.AllowAny,)

    # @csrf_exempt
    def post(self, request):
        org_name = request.data["name"]
        user_data = {
            "username": request.data["email"],
            "password1": request.data["password1"],
            "password2": request.data["password2"],
        }
        form = CustomUserCreationForm(user_data)

        if form.is_valid():
            verified = Verified_Emails.objects.values_list("email", flat=True)
            username = form.cleaned_data.get("username")
            if username not in verified:
                return JsonResponse(
                    {
                        "messages": [
                            "Your organization email has not been verified. Please contact cue@cornelldti.org to sign up."
                        ]
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            else:
                user = form.save()
                Org.objects.create(name=org_name, owner=user, email=username)
                raw_password = form.cleaned_data.get("password1")
                user = authenticate(username=username, password=raw_password)
                login(request, user)
                return JsonResponse({"messages": []}, status=status.HTTP_200_OK)
        else:
            errorList = []
            errors = dict(form.errors.items())
            for key, value in errors.items():
                errorList += value
            return JsonResponse(
                {"messages": errorList}, status=status.HTTP_400_BAD_REQUEST
            )


class Login(APIView):
    permission_classes = (permissions.AllowAny,)

    # @csrf_exempt
    def post(self, request):
        user_data = {
            "username": request.data["email"],
            "password": request.data["password"],
        }

        user = authenticate(
            username=user_data["username"], password=user_data["password"]
        )
        if user is None:
            return JsonResponse(
                {
                    "messages": [
                        "Your email or password is incorrect. Please try again."
                    ]
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )
        login(request, user)
        return JsonResponse({"messages": []}, status=status.HTTP_200_OK)


# =============================================================
#                ORGANIZATION INFORMATION
# =============================================================


class UserProfile(APIView):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        org_id = request.user.id
        org_set = get_object_or_404(Org, pk=org_id)
        serializer = OrgSerializer(
            org_set, many=False, context={"email": request.user.username}
        )
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        orgData = request.data
        org_id = request.user.id
        org_set = get_object_or_404(Org, pk=org_id)

        org_set.name = orgData["name"]
        org_set.website = orgData["website"]
        org_set.bio = orgData["bio"]

        org_set.save()

        serializer = OrgSerializer(
            org_set, many=False, context={"email": request.user.username}
        )
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)


class ChangeOrgEmail(APIView):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        org_email = request.data

        if not validate_email(org_email["new_email"]):
            return JsonResponse(
                {"messages": ["Please enter a valid email address."]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            User.objects.get(username=org_email["new_email"])
            return JsonResponse(
                {
                    "messages": [
                        "Organization email is taken. Please try another email."
                    ]
                },
                status=status.HTTP_409_CONFLICT,
            )

        except ObjectDoesNotExist:
            user_id = request.user.id
            user_set = get_object_or_404(User, pk=user_id)
            user_set.username = org_email["new_email"]
            user_set.save()

            return JsonResponse({"messages": []}, status=status.HTTP_200_OK)


class ChangePassword(APIView):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        old_password = request.data["old_password"]
        new_password = request.data["new_password"]
        user = request.user

        if not user.check_password(old_password):
            return JsonResponse(
                {"messages": ["Your password is incorrect. Please try again."]},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        user.set_password(new_password)
        user.save()
        return JsonResponse({"messages": []}, status=status.HTTP_200_OK)


class OrgDetail(APIView):
    # TODO: alter classes to token and admin?
    authentication_classes = ()  # (TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, org_id, format=None):
        org_set = Org.objects.get(pk=org_id)
        serializer = OrgSerializer(org_set, many=False)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)


class OrgEvents(APIView):
    # TODO: alter classes to token and admin?
    authentication_classes = ()  # (TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, organizer_id, format=None):
        org = Org.objects.get(pk=int(organizer_id))
        org_events_pks = Event_Org.objects.filter(org_id=org).values_list(
            "event_id", flat=True
        )
        event_set = Event.objects.filter(pk__in=org_events_pks)
        serializer = EventSerializer(event_set, many=True)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)


# =============================================================
#                   EVENT INFORMATION
# =============================================================


class AddOrEditEvent(APIView):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        eventData = request.data

        org = request.user.org
        loc = Location.objects.get_or_create(
            room=eventData["location"]["room"],
            building=eventData["location"]["building"],
            place_id=eventData["location"]["place_id"],
        )

        # edit
        try:
            event = Event.objects.get(pk=eventData["pk"])
            event.name = eventData["name"]
            event.location = loc[0]
            event.start_date = dt.strptime(eventData["start_date"], "%m/%d/%Y").date()
            event.end_date = dt.strptime(eventData["end_date"], "%m/%d/%Y").date()
            event.start_time = dt.strptime(eventData["start_time"], "%H:%M:%S %p").time()
            event.end_time = dt.strptime(eventData["end_time"], "%H:%M:%S %p").time()
            event.description = eventData["description"]
            event.organizer = org

            # IMPROVE THIS! RN JUST DELETE ALL THE RELATED TAGS AND PUTTING IT IN
            Event_Tags.objects.filter(event_id=event).delete()

            for t in eventData["tags"]:
                tag = Tag.objects.get(name=t["label"])
                event_tag = Event_Tags.objects.create(event_id=event, tags_id=tag)
            event.save()
            serializer = EventSerializer(event, many=False)

        # add
        except KeyError:
            event = Event.objects.create(
                name=eventData["name"],
                location=loc[0],
                start_date=dt.strptime(eventData["start_date"], "%m/%d/%Y").date(),
                end_date=dt.strptime(eventData["end_date"], "%m/%d/%Y").date(),
                start_time=dt.strptime(eventData["start_time"], "%H:%M:%S %p").time(),
                end_time=dt.strptime(eventData["end_time"], "%H:%M:%S %p").time(),
                description=eventData["description"],
                organizer=org,
            )
            Event_Org.objects.create(event=event, org=org)
            
            for t in eventData["tags"]:
                tag = Tag.objects.get(name=t["label"])
                event_tag = Event_Tags(event_id=event, tags_id=tag)
                event_tag.save()

            serializer = EventSerializer(event, many=False)

        if eventData["imageUrl"] != "":
            media = Media.objects.create(link=eventData["imageUrl"], uploaded_by=org)
            event_media = Event_Media(event=event, media=media)
            event_media.save()

        return JsonResponse(serializer.data, status=status.HTTP_200_OK)


class DeleteEvents(APIView):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    # TODO: DELETE TAGS
    def post(self, request, event_id, format=None):
        org = request.user.org
        event_set = get_object_or_404(Event, pk=event_id)

        if event_set.organizer == org:
            event_set.delete()
            return HttpResponse(status=status.HTTP_204_NO_CONTENT)
        else:
            return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)


# edit tags doesnt workd
class GetEvents(APIView):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, page, format=None):
        org = request.user.org
        event_count = Event.objects.count()
        event_set = Event.objects.filter(organizer=org)[(int(page)-1)*EVENTS_PER_PAGE:int(page)*EVENTS_PER_PAGE]
        serializer = EventSerializer(event_set, many=True)
        last_page= ceil(event_count / EVENTS_PER_PAGE)
        return JsonResponse({"last_page": last_page, "events":serializer.data}, safe=False, status=status.HTTP_200_OK)


class GetAllTags(APIView):
    # TODO: alter classes to token and admin?
    authentication_classes = (SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)


# =============================================================
#                   EVENT INFORMATION
# =============================================================


class EmailDetail(APIView):
    def get(self, request, org_email, org_name, name, net_id, link, format=None):
        send_mail(
            "New Application",
            "Organization Email: "
            + org_email
            + "\n"
            + "Organization Name: "
            + org_name
            + "\n"
            + "Creator Name: "
            + name
            + "\n"
            + "NetID: "
            + net_id
            + "\n"
            + "Organization Link: "
            + link,
            "noreply@cornell.dti.org",
            ["sz329@cornell.edu"],
        )
        return HttpResponse(status=204)


class EventDetail(APIView):
    # TODO: alter classes to token and admin?
    authentication_classes = ()  # (TokenAuthentication, )
    permission_classes = ()  # (permissions.IsAuthenticated, )

    def get(self, request, event_id, format=None):
        event_set = Event.objects.get(pk=event_id)
        serializer = EventSerializer(event_set, many=False)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)


class IncrementAttendance(APIView):
    authentication_classes = ()  # (TokenAuthentication,)
    permission_classes = ()  # (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        event = Event.objects.filter(pk=request.data["event"])[0]
        user = Token.objects.filter(
            pk=extractToken(request.META.get("HTTP_AUTHORIZATION"))
        )[0].user
        attendingSet = Attendance.objects.filter(user_id=user, event_id=event)

        if not attendingSet.exists():
            attendance = Attendance(user_id=user, event_id=event)
            attendance.save()
            event.num_attendees += 1
            event.save()

        return HttpResponse(status=status.HTTP_200_OK)
        # TODO: if exists then response


# =============================================================
#                   LOCATION INFORMATION
# =============================================================


class SingleLocationDetail(APIView):

    # TODO: alter classes to token and admin?
    authentication_classes = ()  # (TokenAuthentication, )
    permission_classes = ()  # (permissions.IsAuthenticated, )

    def get(self, request, location_id, format=None):
        location_set = Location.objects.get(pk=location_id)
        serializer = LocationSerializer(location_set, many=False)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)


class AllLocationDetail(APIView):
    # TODO: alter classes to token and admin?
    authentication_classes = ()  # (TokenAuthentication, )
    permission_classes = ()  # (permissions.IsAuthenticated, )

    def get(self, request, format=None):
        location_set = Location.objects.all()
        serializer = LocationSerializer(location_set, many=True)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)


# =============================================================
#                    TAG INFORMATION
# =============================================================


class SingleTagDetail(APIView):
    # TODO: alter classes to token and admin?
    authentication_classes = ()  # (TokenAuthentication, )
    permission_classes = ()  # (permissions.IsAuthenticated, )

    def get(self, request, tag_id, format=None):
        tag = Tag.objects.get(id=tag_id)
        serializer = TagSerializer(tag, many=False)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)


class AllTagDetail(APIView):
    # TODO: alter classes to token and admin?
    authentication_classes = ()  # (TokenAuthentication, )
    permission_classes = ()  # (permissions.IsAuthenticated, )

    def get(self, request, format=None):
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)


# =============================================================
#                           FEEDS
# =============================================================


class OrgFeed(APIView):
    # TODO: alter classes to token and admin?
    authentication_classes = ()  # (TokenAuthentication, )
    permission_classes = ()  # (permissions.IsAuthenticated, )

    def get(self, request, in_timestamp, format=None):
        old_timestamp = dateutil.parser.parse(in_timestamp)
        outdated_orgs, all_deleted = outdatedOrgs(old_timestamp)
        # json_orgs = JSONRenderer().render(OrgSerializer(outdated_orgs, many = True).data)

        json_orgs = OrgSerializer(outdated_orgs, many=True).data
        serializer = UpdatedOrgSerializer(
            {"orgs": json_orgs, "timestamp": timezone.now()}
        )
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)


def outdatedOrgs(in_timestamp):
    # org_updates = Org.history.filter(history_date__gte = in_timestamp)
    # org_updates = org_updates.distinct('id').order_by('id')

    # org_list = org_updates.values_list('id', flat = True).order_by('id')
    # TODO: What if not in list
    changed_orgs = Org.objects  # .filter(pk__in=org_list)
    # present_pks = Org.objects.filter(pk__in = org_list).values_list('pk', flat = True)
    all_deleted_pks = list()  # set(org_list).difference(set(present_pks)))
    return changed_orgs, all_deleted_pks


class EventFeed(APIView):
    # TODO: token authentication not working...?
    authentication_classes = ()  # (TokenAuthentication, )
    permission_classes = ()  # (permissions.IsAuthenticated, )

    # get event feed, parse timestamp and return events
    def get(self, request, format=None):
        in_timestamp = request.GET.get("timestamp")
        start_time = request.GET.get("start")
        end_time = request.GET.get("end")
        old_timestamp = dateutil.parser.parse(in_timestamp)
        start_time = dateutil.parser.parse(start_time)
        end_time = dateutil.parser.parse(end_time)
        outdated_events, all_deleted = outdatedEvents(
            old_timestamp, start_time, end_time
        )
        json_events = EventSerializer(outdated_events, many=True).data
        serializer = UpdatedEventsSerializer(
            {"events": json_events, "timestamp": timezone.now()}
        )
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)


def outdatedEvents(in_timestamp, start_time, end_time):
    # history_set = Event.history.filter(history_date__gte = in_timestamp)
    # unique_set  = history_set.values_list('id', flat=True).distinct().order_by('id')
    # pks = unique_set.values_list('id', flat=True).order_by('id')
    # #TODO: What if not in list
    changed_events = Event.objects.filter(
        start_date__gte=start_time, end_date__lte=end_time
    ).order_by("id")
    # present_pks = Event.objects.filter(pk__in = pks).values_list('pk', flat = True)
    all_deleted_pks = list()  # set(pks).difference(set(present_pks)))
    return changed_events, all_deleted_pks


# =============================================================
#                          MEDIA
# =============================================================


class GetSignedRequest(APIView):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        S3_BUCKET = settings.AWS_STORAGE_BUCKET_NAME
        timeString = dt.now().strftime("%Y%m%d_%H%M%S")
        file_name = (
            "user_media/"
            + str(request.user.id)
            + "/"
            + timeString
            + "_"
            + request.GET.get("file_name")
        )
        file_type = request.GET.get("file_type")

        s3 = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
       )

        presigned_post = s3.generate_presigned_post(
            Bucket=S3_BUCKET,
            Key=file_name,
            Fields={"acl": "public-read", "Content-Type": file_type},
            Conditions=[{"acl": "public-read"}, {"Content-Type": file_type}],
            ExpiresIn=3600,
        )

        return JsonResponse(
            {
                "data": presigned_post,
                "url": "https://%s.s3.amazonaws.com/%s" % (S3_BUCKET, file_name),
            },
            status=status.HTTP_200_OK,
        )


def tagDetail(tag_id=0, all=False):
    tags = Tag.objects.all()
    if all:
        serializer = TagSerializer(tags, many=True)
    else:
        serializer = TagSerializer(tags.filter(pk=tag_id), many=False)

    return serializer


class ImageDetail(APIView):
    # TODO: alter classes to token and admin?
    authentication_classes = ()  # (TokenAuthentication, )
    permission_classes = ()  # (permissions.IsAuthenticated, )

    def get(self, request, img_id, format=None):
        media = Media.objects.filter(pk=img_id)[0].file.name
        name, extension = os.path.splitext(media)
        s3 = S3Connection(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
        s3bucket = s3.get_bucket(settings.AWS_STORAGE_BUCKET_NAME)
        s3key = s3bucket.get_key(media)
        response = HttpResponse(
            s3key.read(), status=status.HTTP_200_OK, content_type="image/" + extension
        )  # what if its not jpg
        response["Content-Disposition"] = "inline; filename=" + media
        return response


# =============================================================
#                        TOKENS
# =============================================================

# TODO: Different table for firebaseIDs, better practices?
class ObtainToken(APIView):
    # TODO: alter classes to token and admin?
    permission_classes = (permissions.AllowAny,)

    def get(self, request, mobile_id, format=None):
        mobile_user_set = Mobile_User.objects.filter(mobile_id=mobile_id)
        if mobile_user_set.exists():
            return HttpResponseBadRequest("Token Already Assigned to User")
        else:
            validated, valid_info = validate_firebase(mobile_id)
            if not validated:
                return HttpResponseBadRequest("Invalid Firebase ID")

            # generate username
            username = generateUserName()
            user = User.objects.create_user(username=username, password="")
            user.set_unusable_password()
            user.save()

            new_mobile_user = Mobile_User(user=user, mobile_id=mobile_id)
            new_mobile_user.save()

            # generate token
            token = Token.objects.create(user=user)
            return JsonResponse({"token": token.key}, status=status.HTTP_200_OK)


class ResetToken(APIView):
    # TODO: alter classes to token and admin?
    permission_classes = (permissions.AllowAny,)

    def get(self, request, mobile_id, format=None):
        mobile_user_set = Mobile_User.objects.filter(token=mobile_id)
        if mobile_user_set.exists():
            user = mobile_user_set[0]
            token = Token.objects.get(user=user)
            return JsonResponse({"token": token.key}, status=status.HTTP_200_OK)
        else:
            return HttpResponse("Reset Token Error")


# =============================================================
#                        FORMS
# =============================================================


class TagFormView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        form = TagForm()
        return render(request, "post_edit.html", {"form": form})

    def post(self, request):
        form = TagForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect("post_detail_tag", pk=post.pk)


class EventFormView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        form = EventForm()
        return render(request, "post_edit.html", {"form": form})

    def post(self, request):
        form = EventForm(request.POST)

        if form.is_valid():
            e = Event()
            e.name = form.cleaned_data["name"]
            e.description = form.cleaned_data["description"]
            e.start_date = form.cleaned_data["start_date"]
            e.end_date = form.cleaned_data["end_date"]
            e.start_time = form.cleaned_data["start_time"]
            e.end_time = form.cleaned_data["end_time"]
            e.is_public = form.cleaned_data["is_public"]
            e.organizer = form.cleaned_data["organizer"]

            l = Location()
            if form.cleaned_data["existing_location"]:
                l = form.cleaned_data["existing_location"]
                e.location = l
            elif form.cleaned_data["new_location_building"]:
                l.building = form.cleaned_data["new_location_building"]
                l.place_id = form.cleaned_data["new_location_placeid"]
                l.save()
                e.location = l
            else:
                return redirect("post_detail_event_error.html")

            e.save()
            return redirect("post_detail_event", pk=e.pk)


class LocationFormView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        form = LocationForm()
        return render(request, "post_edit.html", {"form": form})

    def post(self, request):
        form = LocationForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect("post_detail_location", pk=post.pk)


class OrgFormView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        form = OrgForm()
        return render(request, "post_edit.html", {"form": form})

    def post(self, request):
        form = OrgForm(request.POST)
        if form.is_valid():
            o = Org()
            o.name = form.cleaned_data["name"]
            o.description = form.cleaned_data["description"]
            o.verified = form.cleaned_data["verified"]
            o.website = form.cleaned_data["website"]
            o.photo = form.cleaned_data["photo"]

            o.owner = request.user

            o.save()
            return redirect("post_detail_org", pk=o.pk)


# =============================================================
#                        HELPERS
# =============================================================
def check_login_status(request):
    return JsonResponse({"status": request.user.is_authenticated})


def extractToken(header):
    return header[header.find(" ") + 1 :]


def generateUserName():
    # HANDLE user.obects.latest is null case
    # Safe: pk < 2147483647 and max(len(username)) == 150 [16/9/2018]
    return "user{0}".format(User.objects.latest("pk").pk + 1)


def post_detail_org(request, pk):
    post = get_object_or_404(Org, pk=pk)
    return render(request, "post_detail_org.html", {"post": post})


def post_detail_tag(request, pk):
    post = get_object_or_404(Tag, pk=pk)
    return render(request, "post_detail_tag.html", {"post": post})


def post_detail_event(request, pk):
    post = get_object_or_404(Event, pk=pk)
    return render(request, "post_detail_event.html", {"post": post})


def post_detail_location(request, pk):
    post = get_object_or_404(Location, pk=pk)
    return render(request, "post_detail_location.html", {"post": post})


def post_detail_user(request, pk):
    post = get_object_or_404(User, pk=pk)
    return render(request, "post_detail_user.html", {"post": post})


def post_edit_org(request, pk):
    post = get_object_or_404(Org, pk=pk)
    if request.method == "POST":
        form = OrgForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect("post_detail_org", pk=post.pk)
    else:
        form = OrgForm(instance=post)
    return render(request, "post_edit.html", {"form": form})


def post_event_edit(request, pk):
    post = get_object_or_404(Event, pk=pk)
    if request.method == "POST":
        form = EventForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect("post_detail", pk=post.pk)
    else:
        form = EventForm(instance=post)
    return render(request, "blog/post_edit.html", {"form": form})


def validate_email(email):
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email)


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
        serializer.save(owner=self.request.user)


# =============================================

