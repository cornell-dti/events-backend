# admin.py
# Arnav Ghosh
# 16th July 2018

from django.contrib import admin
from .models import Attendance, Event, Location, Media, Org, Tag, UserID
#from rest_framework.authtoken.admin import Tokenadmin
#from rest_framework.authtoken.admin import Token

admin.site.register(Org)
admin.site.register(Event)
admin.site.register(Location)
admin.site.register(Media)
admin.site.register(Tag)
admin.site.register(Attendance)
admin.site.register(UserID)
#admin.site.register(Token, TokenAdmin)

#admin.site.unregister(Token) #First unregister the old class
#admin.site.register(Token, AuthTokenAdmin) #Then register the new class

# @admin.register(Token)
# class TokenAdmin(admin.ModelAdmin):
#     list_display = ('key', 'user', 'created')
#     fields = ('user',)
#     ordering = ('-created',)
