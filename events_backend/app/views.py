# views.py
# Arnav Ghosh, Jessica Zhao, Jill Wu, Adit Gupta
# 17th Sept. 2018

from boto.s3.connection import S3Connection

import dateutil.parser
import boto3
import math

from datetime import datetime as dt, date

from django.conf import settings
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.staticfiles.storage import staticfiles_storage
from django.http.response import StreamingHttpResponse

from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist

from .permissions import IsOwnerOrReadOnly
from .forms import CustomUserCreationForm

from google.oauth2 import id_token
from google.auth.transport import requests

from rest_framework import status, generics
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet

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
    Org_Media,
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

from math import ceil

User = get_user_model()
EVENTS_PER_PAGE = 15


# =============================================================
#                    AASA
# =============================================================
class AppleAppSite(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        response = StreamingHttpResponse(staticfiles_storage.open(
            "apple-app-site-association"), content_type="application/json")
        return response


# =============================================================
#                        TOKENS
# =============================================================

# TODO: Different table for firebaseIDs, better practices?
class Tokens(ViewSet):
    # TODO: alter classes to token and admin?
    permission_classes = (AllowAny,)

    def get_token(self, request, mobile_id, format=None):
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

    def reset_token(self, request, mobile_id, format=None):
        mobile_user_set = Mobile_User.objects.filter(token=mobile_id)
        if mobile_user_set.exists():
            user = mobile_user_set[0]
            token = get_object_or_404(Token, user=user)
            return JsonResponse({"token": token.key}, status=status.HTTP_200_OK)
        else:
            return HttpResponse("Reset Token Error")


# =============================================================
#            LOGIN/SIGNUP/CHANGE LOGIN EMAIL/PASSWORD
# =============================================================

class SignUp(APIView):
    permission_classes = (AllowAny,)

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
                            "Your organization email has not been verified. \
                            Please contact cue@cornelldti.org to sign up."
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
            for _, value in errors.items():
                errorList += value

            return JsonResponse(
                {"messages": errorList}, status=status.HTTP_400_BAD_REQUEST
            )


class Login(APIView):
    permission_classes = (AllowAny,)

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


class ChangeLoginCredentials(ViewSet):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)

    def change_login_email(self, request):
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

    def change_password(self, request):
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


# =============================================================
#                  ORGANIZATION PROFILE
# =============================================================

class UserProfile(ViewSet):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_profile(self, request, org_id=None, format=None):
        if org_id is None:
            org_owner_id = request.user.id
            org_set = get_object_or_404(Org, owner=org_owner_id)
        else:
            org_set = get_object_or_404(Org, pk=org_id)
        serializer = OrgSerializer(org_set, many=False)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)

    def edit_profile(self, request, format=None):
        orgData = request.data
        org_owner_id = request.user.id
        org_set = get_object_or_404(Org, owner=org_owner_id)

        org_set.name = orgData["name"]
        org_set.website = orgData["website"]
        org_set.bio = orgData["bio"]

        if orgData["imageUrl"] != "":
            media = Media.objects.create(
                link=orgData["imageUrl"], uploaded_by=org_set)
            org_media = Org_Media(org=org_set, media=media)
            org_media.save()

        org_set.save()

        serializer = OrgSerializer(
            org_set, many=False, context={"email": request.user.username}
        )
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)

# =============================================================
#                     ORGANIZATION EVENTS
# =============================================================


class OrgEvents(ViewSet):
    # TODO: alter classes to token and admin?
    # (TokenAuthentication, )
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_event(self, request, event_id, format=None):
        event_set = get_object_or_404(Event, pk=event_id)
        serializer = EventSerializer(event_set, many=False)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)

    def get_events(self, request, org_id=None, format=None):
        if org_id is None:
            org_owner_id = request.user.id
            org = get_object_or_404(Org, owner=org_owner_id)
        else:
            org = get_object_or_404(Org, pk=org_id)

        event_set = Event.objects.filter(organizer=org)
        if request.GET.get("page") != None:
            page = request.GET.get("page")
            event_set = Event.objects.filter(organizer=org)[(
                int(page)-1)*EVENTS_PER_PAGE:int(page)*EVENTS_PER_PAGE]
            last_page = ceil(event_set.count()/EVENTS_PER_PAGE)
            serializer = EventSerializer(event_set, many=True)
            return JsonResponse({"last_page": last_page, "events":
                                 serializer.data}, status=status.HTTP_200_OK)

        else:
            serializer = EventSerializer(event_set, many=True)
            return JsonResponse({"events": serializer.data}, status=status.HTTP_200_OK)

    def add_event(self, request):
        org_owner_id = request.user.id
        org = get_object_or_404(Org, owner=org_owner_id)
        eventData = request.data
        loc = Location.objects.get_or_create(
            room=eventData["location"]["room"],
            building=eventData["location"]["building"],
            place_id=eventData["location"]["place_id"],
        )

        event = Event.objects.create(
            name=eventData["name"],
            location=loc[0],
            start_date=dt.strptime(eventData["start_date"], "%m/%d/%Y").date(),
            end_date=dt.strptime(eventData["end_date"], "%m/%d/%Y").date(),
            start_time=dt.strptime(
                eventData["start_time"], "%H:%M:%S %p").time(),
            end_time=dt.strptime(eventData["end_time"], "%H:%M:%S %p").time(),
            description=eventData["description"],
            organizer=org,
        )
        Event_Org.objects.create(event=event, org=org)

        for t in eventData["tags"]:
            tag = get_object_or_404(Tag, name=t["label"])
            Event_Tags.objects.get_or_create(event=event, tags=tag)

        if eventData["imageUrl"] != "":
            media = Media.objects.create(
                link=eventData["imageUrl"], uploaded_by=org)
            Event_Media.objects.get_or_create(event=event, media=media)

        serializer = EventSerializer(event, many=False)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)

    def edit_event(self, request):
        org_owner_id = request.user.id
        org = get_object_or_404(Org, owner=org_owner_id)

        eventData = request.data
        event = get_object_or_404(Event, pk=eventData["pk"])
        loc = Location.objects.get_or_create(
            room=eventData["location"]["room"],
            building=eventData["location"]["building"],
            place_id=eventData["location"]["place_id"],
        )
    
        event.name = eventData["name"]
        event.location = loc[0]
        event.start_date = dt.strptime(
            eventData["start_date"], "%m/%d/%Y").date()
        event.end_date = dt.strptime(eventData["end_date"], "%m/%d/%Y").date()
        event.start_time = dt.strptime(
            eventData["start_time"], "%H:%M:%S %p").time()
        event.end_time = dt.strptime(
            eventData["end_time"], "%H:%M:%S %p").time()
        event.description = eventData["description"]
        event.organizer = org
        event.save()
        
        for t in event.tags.all():
            Event_Tags.objects.filter(tags_id=t.id).delete()

        for t in eventData["tags"]:
            tag = get_object_or_404(Tag, name=t["label"])
            Event_Tags.objects.get_or_create(event=event, tags=tag)

        if eventData["imageUrl"] != "":
            media = Media.objects.create(
                link=eventData["imageUrl"], uploaded_by=org)
            Event_Media.objects.get_or_create(event=event, media=media)

        serializer = EventSerializer(event, many=False)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)

    def delete_event(self, request, event_id, format=None):
        org_owner_id = request.user.id
        org = get_object_or_404(Org, owner=org_owner_id)
        event = get_object_or_404(Event, pk=event_id)

        if event.organizer == org:
            event.delete()
            return HttpResponse(status=status.HTTP_204_NO_CONTENT)
        else:
            return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)

    # TODO: FIGURE OUT THE PERMISSIONS REQUIRED FOR ATTENDANCE FUNCTIONS
    def increment_attendence(self, request, event_id, format=None):
        event = get_object_or_404(Event, pk=event_id)
        event.num_attendees = event.num_attendees + 1
        event.save()
        return HttpResponse("Attendance incremented for event with ID: " + event_id, status=status.HTTP_200_OK)

    def decrement_attendance(self, request, event_id, format=None):
        event = get_object_or_404(Event, pk=event_id)
        event.num_attendees = event.num_attendees - 1
        event.save()
        return HttpResponse("Attendance decremented for event with ID: " + event_id, status=status.HTTP_200_OK)

# =============================================================
#                          TAGS
# =============================================================


class Tags(ViewSet):
    permission_classes = (AllowAny,)

    def get_all_tags(self, request, format=None):
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        return JsonResponse({"tags": serializer.data}, status=status.HTTP_200_OK)

    def get_tag(self, request, tag_id, format=None):
        tag = get_object_or_404(Tag, id=tag_id)
        serializer = TagSerializer(tag, many=False)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)

# =============================================================
#                        LOCATIONS
# =============================================================


class Locations(ViewSet):
    permission_classes = (AllowAny,)

    def get_all_locations(self, request, format=None):
        location_set = Location.objects.all()
        serializer = LocationSerializer(location_set, many=True)
        return JsonResponse({"locations": serializer.data}, status=status.HTTP_200_OK)

    def get_location(self, request, location_id, format=None):
        location_set = get_object_or_404(Location, pk=location_id)
        serializer = LocationSerializer(location_set, many=False)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)

# =============================================================
#                          FEEDS
# =============================================================


class Feeds(ViewSet):
    permission_classes = (AllowAny,)

    def get_event_feed(self, request, format=None):
        upcoming_events = Event.objects.filter(start_date__gte=date.today())
        serializer = EventSerializer(upcoming_events, many=True)
        return JsonResponse({"events": serializer.data}, status=status.HTTP_200_OK)

# =============================================================
#                          MEDIA
# =============================================================

# TODO: DEAL WITH THIS AFTER SCOTT IS DONE WITH HIS S3 FIX


class GetSignedRequest(APIView):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)

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


class ImageDetail(APIView):
    # TODO: alter classes to token and admin?
    authentication_classes = ()  # (TokenAuthentication, )
    permission_classes = ()  # (IsAuthenticated, )

    def get(self, request, img_id, format=None):
        media = Media.objects.filter(pk=img_id)[0].file.name
        name, extension = os.path.splitext(media)
        s3 = S3Connection(settings.AWS_ACCESS_KEY_ID,
                          settings.AWS_SECRET_ACCESS_KEY)
        s3bucket = s3.get_bucket(settings.AWS_STORAGE_BUCKET_NAME)
        s3key = s3bucket.get_key(media)
        response = HttpResponse(
            s3key.read(), status=status.HTTP_200_OK, content_type="image/" + extension
        )  # what if its not jpg
        response["Content-Disposition"] = "inline; filename=" + media
        return response


class UploadImage(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        return JsonResponse({
            "potato": "123"
        }, status=status.HTTP_200_OK)

# =============================================================
#                       VERSIONING
# =============================================================

class GetMinVersionView(APIView):

    permission_classes = ()

    def get(self, request, version, platform):
        minIosVersion = "3.3.5"
        minAndroidVersion = "3.6.7"
        versionSplits = version.split(".")
        plat = platform.lower()
        if plat != "android" and plat != "ios":
            return JsonResponse ({ 'passed': False })
        if plat == "android":
            minVersionSplits = minAndroidVersion.split(".")
        elif plat == "ios":
            minVersionSplits = minIosVersion.split(".")

        for i in range(0, len(minVersionSplits)):
            if int(versionSplits[i]) >= int(minVersionSplits[i]):
                return JsonResponse({ 'passed': True })

        return JsonResponse({ 'passed': False })


# =============================================================
#                        HELPERS
# =============================================================

def check_login_status(request):
    return JsonResponse({"status": request.user.is_authenticated})


def extractToken(header):
    return header[header.find(" ") + 1:]


def generateUserName():
    # HANDLE user.obects.latest is null case
    # Safe: pk < 2147483647 and max(len(username)) == 150 [16/9/2018]
    return "user{0}".format(User.objects.latest("pk").pk + 1)


def validate_email(email):
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email)


def validate_firebase(mobile_id):
    try:
        idinfo = id_token.verify_oauth2_token(mobile_id, requests.Request())
        return True, ""
    except Exception as e:
        return False, mobile_id

# TODO: FIGURE OUT WHAT THE BOTTOM 3 APIS DO


class UserList(generics.ListAPIView):
    queryset = User.objects.filter(is_staff=False)
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.filter(is_staff=False)
    serializer_class = UserSerializer


class Authentication(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


# ============================================
