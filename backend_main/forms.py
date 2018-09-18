from django import forms

from .models import Org, Tag, Event, Location

class OrgForm(forms.ModelForm):

    class Meta:
        model = Org
        fields = ('name', 'description', 'contact', 'verified',)
        
class TagForm(forms.ModelForm):

    class Meta:
        model = Tag
        fields = ('name',)
        
class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = ('name', 'description', 'start_date', 'end_date', 'start_time', 'end_time', 'is_public', 'organizer', 'location')
        
class LocationForm(forms.ModelForm):

    class Meta:
        model = Location
        fields = ('building', 'room', 'place_id')