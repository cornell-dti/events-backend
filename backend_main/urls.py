# urls.py
# Arnav Ghosh
# 18th July 2018

from django.conf.urls import url
from . import views

dateRegex = "[0-9]{4}[0-1][0-9][0-3][0-9]T[0-9]{6}"

urlpatterns = [
	url(r'^event/(?P<event_id>[0-9]+)/$', views.eventDetail, name='Event Details'),
	url(r'^org/(?P<org_id>[0-9]+)/$', views.orgDetail, name='Organizer Details'),
	url(r'^loc/(?P<location_id>[0-9]+)/$', views.locationDetail, name='Location Details'),
	url(r'^tag/(?P<tag_id>[0-9]+)/$', views.singleTag, name='Single Tag Details'),
	url(r'^tag/all/$', views.allTags, name='Single Tag Details'),
	url(r'^feed/events/timestamp=(?P<in_timestamp>{0})&start=(?P<start_time>{0})&end=(?P<end_time>{0})/$'.format(dateRegex), 
		views.changesInEvents, 
		name='Updated Event Feed'),
	url(r'^feed/org/timestamp=(?P<in_timestamp>{0})/$'.format(dateRegex), views.changesInOrgs, name='Updated Organizer Feed')
]