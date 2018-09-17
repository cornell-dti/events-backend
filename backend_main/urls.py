# urls.py
# Arnav Ghosh, Jessica Zhao, Jill Wu, Adit Gupta
# 17th Sept. 2018

from django.conf.urls import url
from django.urls import path
from . import views

dateRegex = "[0-9]{4}[0-1][0-9][0-3][0-9]T[0-9]{6}"

urlpatterns = [
	#path('post/org', views.post_org, name='post_org'),
	#path('post/tag', views.post_tag, name='post_tag'),
	#path('post/org/<int:pk>/edit/', views.post_org_edit, name='post_edit'),
	#path('post/event/<int:pk>/edit/', views.post_event_edit, name='post_edit'),
	url(r'^event/(?P<event_id>[0-9]+)/$', views.EventDetail.as_view(), name='Event Details'),
	url(r'^org/(?P<org_id>[0-9]+)/$', views.OrgDetail.as_view(), name='Organizer Details'),
	url(r'^loc/(?P<location_id>[0-9]+)/$', views.LocationDetail.as_view(), name='Location Details'),
	url(r'^tag/(?P<tag_id>[0-9]+)/$', views.SingleTagDetail.as_view(), name='Single Tag Details'),
	url(r'^tag/all/$', views.AllTagDetail.as_view(), name='Single Tag Details'),
	url(r'^media/(?P<img_id>[0-9]+)/$',  views.ImageDetail.as_view(), name='Media Detail'),
	url(r'^feed/events/timestamp=(?P<in_timestamp>{0})&start=(?P<start_time>{0})&end=(?P<end_time>{0})/$'.format(dateRegex),
		views.EventFeed.as_view(),
		name='Updated Event Feed'),
	url(r'^feed/org/timestamp=(?P<in_timestamp>{0})/$'.format(dateRegex), views.OrgFeed.as_view(), name='Updated Organizer Feed'),
	url(r'^generate_token/(?P<mobile_id>.*)/$', views.ObtainToken.as_view(), name='Create Mobile Token'),
	url(r'^attendance/$', views.IncrementAttendance.as_view(), name="Update Attendance")

]
