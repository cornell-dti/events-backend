from django import forms

from .models import Org, Tag, Event, Location

class OrgForm(forms.ModelForm):

    class Meta:
        model = Org
        fields = ('name', 'description',)

class TagForm(forms.ModelForm):

    class Meta:
        model = Tag
        fields = ('name',)

class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = ('name', 'description', 'start_date', 'end_date', 'start_time', 'end_time', 'is_public', 'organizer', 'location')

    def __init__(self, user, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields['organizer'].queryset = Org.objects.filter(owner_id=user)

class LocationForm(forms.ModelForm):

    class Meta:
        model = Location
        fields = ('building', 'place_id')
