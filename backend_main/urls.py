# urls.py
# Arnav Ghosh
# 18th July 2018

from django.conf.urls import url
from django.urls import path
from . import views

dateRegex = "[0-9]{4}[0-1][0-9][0-3][0-9]T[0-9]{6}"

urlpatterns = [
	path('post/org/', views.post_org, name='post_org'),
	path('post/org/<int:pk>/', views.post_detail_org, name='post_detail_org'),
	path('post/org/<int:pk>/edit/', views.post_edit_org, name='post_edit_org'),

	path('post/tag/', views.post_tag, name='post_tag'),
	path('post/tag/<int:pk>/', views.post_detail_tag, name='post_detail_tag'),
	path('post/event/', views.post_event, name='post_event'),
	path('post/event/<int:pk>/', views.post_detail_event, name='post_detail_event'),

	path('post/location/', views.post_location, name='post_location'),
	path('post/location/<int:pk>/', views.post_detail_location, name='post_detail_location'),


	# path('post/org/<int:pk>/edit/', views.post_org_edit, name='post_edit'),
	# path('post/event/<int:pk>/edit/', views.post_event_edit, name='post_edit'),
	
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