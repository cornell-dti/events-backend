# serializers.py
# Arnav Ghosh
# 21st June 2018

from rest_framework import serializers
from .models import Org, Event, Location

class EventSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Event
        fields = ('pk', 'name', 'description', 'start_date', 'end_date', 
        	'start_time', 'end_time', 'num_attendees', 'is_public', 'organizer')
        
class LocationSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = Location
		fields = ('pk', 'building','room', 'place_id')

class OrgSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = Org
		fields = ('pk', 'name','description', 'contact', 'verified')

class UpdatedEventsSerializer(serializers.Serializer):
	updated = serializers.JSONField() #pass in serialized events
	deleted = serializers.ListField()
	timestamp = serializers.DateTimeField()

class UpdatedOrgSerializer(serializers.Serializer):
	updated = serializers.JSONField() #pass in serialized events
	deleted = serializers.ListField()
	timestamp = serializers.DateTimeField()