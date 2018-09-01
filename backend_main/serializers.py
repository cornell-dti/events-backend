# serializers.py
# Arnav Ghosh
# 21st June 2018

from rest_framework import serializers
from .models import Org, Event, Location, Tag, Event_Tags
from django.contrib.auth.models import User


class EventSerializer(serializers.ModelSerializer):
    event_tags = serializers.PrimaryKeyRelatedField(queryset = Event_Tags.objects.all(), many=True)
    
    class Meta:
        model = Event
        #exclude = ('history',)
        fields = ('pk', 'name', 'description', 'start_date', 'end_date', 
        	'start_time', 'end_time', 'num_attendees', 'is_public', 'organizer', 'location', 'event_tags')
        
class LocationSerializer(serializers.ModelSerializer):

	class Meta:
		model = Location
		fields = ('pk', 'building','room', 'place_id')

class OrgSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = Org
		fields = ('pk', 'name','description', 'contact', 'verified')

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
