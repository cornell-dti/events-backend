# admin.py
# Arnav Ghosh
# 16th July 2018

from django.contrib import admin
from .models import Org, Event, Location, Media

admin.site.register(Org)
admin.site.register(Event)
admin.site.register(Location)
admin.site.register(Media)