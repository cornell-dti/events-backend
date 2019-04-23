# serializers.py
# Arnav Ghosh
# 21st June 2018

from rest_framework import serializers

from .models import Event, Org, Location, Tag, Org_Tags, Media, Event_Tags, Event_Media
from django.contrib.auth.models import User


class EventSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(queryset = Event_Tags.objects.all(), many=True)
    
    class Meta:
        model = Event
        #exclude = ('history',)
        fields = ('pk', 'name', 'description', 'start_date', 'end_date', 
        	'start_time', 'end_time', 'num_attendees', 'is_public', 'organizer', 'location', 'tags', 'media')
        depth = 1
        
class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Location
        fields = ('pk', 'building', 'room', 'place_id')


class OrgSerializer(serializers.ModelSerializer):
	org_tags = serializers.PrimaryKeyRelatedField(queryset = Org_Tags.objects.all(), many=True)

	class Meta:
		model = Org
		fields = ('pk', 'name', 'email', 'bio', 'photo', 'website', 'tags', 'is_staff', 'org_tags', 'is_active')


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ("id", "name")


class UpdatedEventsSerializer(serializers.Serializer):
    updated = serializers.JSONField()  # pass in serialized events
    deleted = serializers.ListField()
    timestamp = serializers.DateTimeField()


class UpdatedOrgSerializer(serializers.Serializer):
    updated = serializers.JSONField()  # pass in serialized events
    deleted = serializers.ListField()
    timestamp = serializers.DateTimeField()


class UserSerializer(serializers.ModelSerializer):
    org = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Org.objects.all())
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = User
        fields = ('id', 'username', 'org', 'owner')
