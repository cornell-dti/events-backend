# serializers.py
# Arnav Ghosh
# 21st June 2018

from rest_framework import serializers
from .models import Event, Org, Location, Tag, Org_Tags, Media, Event_Tags, Event_Media
from django.contrib.auth.models import User
from django.conf import settings


class OrgSerializer(serializers.ModelSerializer):
    # email = serializers.SerializerMethodField()

    class Meta:
        model = Org
        fields = ("pk", "name", "email", "bio", "photo", "website", "tags")
        depth = 1

    def get_email(self, obj):
        try:
            return self.context["email"]
        except KeyError:
            return ""


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = (
            "pk",
            "organizer",
            "name",
            "description",
            "start_date",
            "end_date",
            "start_time",
            "end_time",
            "num_attendees",
            "is_public",
            "location",
            "tags",
            "media",
        )
        depth = 1

    def to_representation(self, instance):
        """Convert `username` to lowercase."""
        ret = super().to_representation(instance)
        for media in ret["media"]:
            media["link"] = (
                "https://"
                + settings.AWS_STORAGE_BUCKET_NAME
                + ".s3.amazonaws.com/"
                + media["link"]
            )
        return ret


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ("pk", "building", "room", "place_id")


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag

        fields = ("pk", "name")


class UpdatedEventsSerializer(serializers.Serializer):
    events = serializers.JSONField()  # pass in serialized events
    timestamp = serializers.DateTimeField()
    pages = serializers.IntegerField()

class UpdatedOrgSerializer(serializers.Serializer):
    orgs = serializers.JSONField()  # pass in serialized events
    timestamp = serializers.DateTimeField()


class UserSerializer(serializers.ModelSerializer):
    org = serializers.PrimaryKeyRelatedField(many=True, queryset=Org.objects.all())
    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = User
        fields = ("id", "username", "org", "owner")
