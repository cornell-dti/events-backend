# serializers.py
# Arnav Ghosh
# 21st June 2018

from rest_framework import serializers

from .models import Event, Org, Location, Tag, Org_Tags, Event_Tags, Event_Media
from django.contrib.auth.models import User

class OrgSerializer(serializers.ModelSerializer):
	org_tags = serializers.PrimaryKeyRelatedField(queryset = Org_Tags.objects.all(), many=True)
    
	class Meta:
		model = Org
		fields = ('pk', 'name', 'email', 'bio', 'photo', 'website', 'tags', 'is_staff', 'org_tags', 'is_active')
		
class EventSerializer(serializers.ModelSerializer):
    event_tags = serializers.PrimaryKeyRelatedField(queryset = Event_Tags.objects.all(), many=True)
    event_media = serializers.PrimaryKeyRelatedField(queryset = Event_Media.objects.all(), many=True)
    organizer = OrgSerializer()

    class Meta:
        model = Event
        fields = ('pk', 'organizer', 'name', 'description', 'start_date', 'end_date', 
        	'start_time', 'end_time', 'num_attendees', 'is_public', 'location', 'event_tags', 'event_media')
        depth = 1
        
class LocationSerializer(serializers.ModelSerializer):

	class Meta:
		model = Location
		fields = ('pk', 'building','room', 'place_id')

class TagSerializer(serializers.ModelSerializer):

	class Meta:
		model = Tag
		fields = ("pk", "name")

class UpdatedEventsSerializer(serializers.Serializer):
	updated = serializers.JSONField() #pass in serialized events
	deleted = serializers.ListField()
	timestamp = serializers.DateTimeField()

class UpdatedOrgSerializer(serializers.Serializer):
	updated = serializers.JSONField() #pass in serialized events
	deleted = serializers.ListField()
	timestamp = serializers.DateTimeField()

class UserSerializer(serializers.ModelSerializer):
	org = serializers.PrimaryKeyRelatedField(many=True, queryset=Org.objects.all())
	owner = serializers.ReadOnlyField(source='owner.username')

	class Meta:
		model = User
		fields = ('id', 'username', 'org', 'owner')
