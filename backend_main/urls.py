# urls.py
# Arnav Ghosh, Jessica Zhao, Jill Wu, Adit Gupta
# 17th Sept. 2018

from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.conf.urls import include
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import TemplateView
from django.urls import path
from rest_framework.authtoken import views as authviews
from . import views

dateRegex = "[0-9]{4}[0-1][0-9][0-3][0-9]T[0-9]{6}"
spoof = "Clny9jLW4lf2gAvOZ27fJYnPJNyEPqKiMfmkAkFgXzksjoTEkeL9o5M4lHNbyrUCsVnglEv89pTcs1o787xt17KF6HZaHuqDMEjNPfpDdJBeB8nHbFLqJuqGTsEqT5NAai7UGJxgSPcszLTmpMT6PhRY7VATmEcbbqvf3McjsvfZ0Um9UHUVzCwpnj67n6rSbiy4kZm8"

urlpatterns = [
	path('post/org/', views.OrgFormView.as_view(), name='post_org'),
	path('post/org/<int:pk>/', views.post_detail_org, name='post_detail_org'),
	path('post/org/<int:pk>/edit/', views.post_edit_org, name='post_edit_org'),

	path('post/tag/', views.TagFormView.as_view(), name='post_tag'),
	path('post/tag/<int:pk>/', views.post_detail_tag, name='post_detail_tag'),

	path('post/event/', views.EventFormView.as_view(), name='post_event'),
	path('post/event/<int:pk>/', views.post_detail_event, name='post_detail_event'),

	path('post/location/', views.LocationFormView.as_view(), name='post_location'),
	path('post/location/<int:pk>/', views.post_detail_location, name='post_detail_location'),

	path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html', redirect_authenticated_user=True)),
	path('settings/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html', success_url='../profile')),
	path('accounts/', include('django.contrib.auth.urls')),

	url(r'^email/orgEmail=(?P<org_email>.*)&orgName=(?P<org_name>.*)&name=(?P<name>[a-zA-Z\s]+)&netID=(?P<net_id>[a-zA-Z0-9]+)&link=(?P<link>.*)$', views.EmailDetail.as_view(), name='Email Detail'),
	url(r'^event/(?P<event_id>[0-9]+)/$', views.EventDetail.as_view(), name='Event Details'),
	url(r'^org/(?P<org_id>[0-9]+)/$', views.OrgDetail.as_view(), name='Organizer Details'),
	url(r'^org/(?P<organizer_id>[0-9]+)/events/$', views.OrgEvents.as_view(), name='Organizer Events'),
	url(r'^loc/(?P<location_id>[0-9]+)/$', views.SingleLocationDetail.as_view(), name='Location Details'),
	url(r'^loc/all/$', views.AllLocationDetail.as_view(), name='All Location Details'),
	url(r'^tag/(?P<tag_id>[0-9]+)/$', views.SingleTagDetail.as_view(), name='Single Tag Details'),
	url(r'^tag/all/$', views.AllTagDetail.as_view(), name='Single Tag Details'),
	url(r'^media/(?P<img_id>[0-9]+)/$',  views.ImageDetail.as_view(), name='Media Detail'),
	url(r'^feed/events/$', views.EventFeed.as_view(), name='Updated Events Feed'), 
	url(r'^feed/org/timestamp=(?P<in_timestamp>{0})/$'.format(dateRegex), views.OrgFeed.as_view(), name='Updated Organizer Feed'),
	url(r'^generate_token/(?P<mobile_id>.*)/$', views.ObtainToken.as_view(), name='Create Mobile Token'),
	url(r'^reset_token/(?P<mobile_id>.*)/{0}/$'.format(spoof), views.ResetToken.as_view(), name='Reset Mobile Token'),
	url(r'^attendance/$', views.IncrementAttendance.as_view(), name="Update Attendance"),

	url(r'^users/$', views.UserList.as_view()),
	url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
	url(r'^api-auth/', authviews.obtain_auth_token),
	url(r'^signup/', ensure_csrf_cookie(views.signup), name="Sign-Up" ),
	url(r'^profile/', views.profile, name="Profile" ),
	url(r'^', TemplateView.as_view(template_name="main.html")) 
]
