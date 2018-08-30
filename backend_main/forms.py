from django import forms

from .models import Org
from .models import Tag

class OrgForm(forms.ModelForm):

    class Meta:
        model = Org
        fields = ('name', 'description', 'contact', 'verified', 'history',)
        
class TagForm(forms.ModelForm):

    class Meta:
        model = Org
        fields = ('name',)