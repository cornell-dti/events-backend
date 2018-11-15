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
        fields = ('name', 'description', 'start_date', 'end_date', 'start_time', 'end_time', 'is_public') #'existing_location', 'new_location_placeid', 'new_location_building')

    existing_location = forms.IntegerField()
    new_location_building = forms.CharField()
    new_location_placeid = forms.CharField()

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        #self.fields['organizer'].queryset = Org.objects.filter(owner = user)


class LocationForm(forms.ModelForm):

    class Meta:
        model = Location
        fields = ('building', 'place_id')
