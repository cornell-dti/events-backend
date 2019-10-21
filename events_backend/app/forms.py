from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Tag, Event, Location, Org, User


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "password1", "password2")

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.username = self.cleaned_data["username"]
        user.password1 = self.cleaned_data["password1"]
        user.password2 = self.cleaned_data["password2"]
        if commit:
            user.save()
        return user


class OrgForm(forms.ModelForm):
    class Meta:
        model = Org
        fields = ("name",)


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = (
            "name",
            "description",
            "start_date",
            "end_date",
            "start_time",
            "end_time",
            "is_public",
            "organizer",
            "existing_location",
            "new_location_placeid",
            "new_location_building",
        )

    existing_location = forms.ModelChoiceField(
        queryset=Location.objects.all(), required=False
    )
    new_location_building = forms.CharField(required=False)
    new_location_placeid = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ("name",)


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ("building", "place_id")
        

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Org
        fields = ("name", "website", "bio")

        website = forms.CharField(required=False)
        bio = forms.CharField(required=False)

    def save(self, commit=True):
        user = super(ProfileForm, self).save(commit=False)
        user.name = self.cleaned_data["name"]
        user.website = self.cleaned_data["website"]
        user.bio = self.cleaned_data["bio"]
        if commit:
            user.save()
        return user
