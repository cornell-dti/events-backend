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
	url(r'^feed/events/timestamp=(?P<timestamp>{0})&start=(?P<start_time>{0})&end=(?P<end_time>{0})/$'.format(dateRegex), 
		views.changesInEvents, 
		name='Updated Event Feed'),
	url(r'^feed/org/timestamp=(?P<timestamp>{0})/$'.format(dateRegex), views.changesInOrgs, name='Updated Organizer Feed')

	# url(r'^$', views.index, name='index'),
	# url(r'^feed/(?P<day>[1-9]|[12][0-9]|3[01])/$', views.feed, name='feed by date'),
	# url(r'^feed/(?P<day>[1-9]|[12][0-9]|3[01])/(?P<req_category>[a-zA-z]+)/$', views.feed, name='feed with category'),
	# url(r'^version/(?P<version>[0-9]+)$', views.versionedFeed, name='update version'),
	# url(r'^event/(?P<event_id>[0-9]+)/$', views.event_details, name='event details'),
	# url(r'^event/(?P<event_id>[0-9]+)/image$', views.eventImage, name='event image'),
	# url(r'^categories/$', views.categories, name='categories'),
	# url(r'^bulk_add_event/$', views.bulk_add, name='bulk add'),
	# url(r'^bulk_add_categories/$', views.upload_categories, name='bulk categories'),
	# url(r'^bulk_image/$', views.image_for_all, name='bulk image upload'),
	# url(r'^modify/(?P<siteName>\S+)/(?P<mode>[0-4])/(?P<siteValue>\S+)/$', views.modifyEvent, name = "Automatic Changes")
]