"""events_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from rest_framework.authtoken import views as authviews
from . import views

dateRegex = "[0-9]{4}[0-1][0-9][0-3][0-9]T[0-9]{6}"

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # TODO Should this be events_backend.app.api_urls?
    url(r'^api/', include('app.api_urls')),

    #path('post/org/', views.OrgFormView.as_view(), name='post_org'),
    #path('post/org/<int:pk>/', views.post_detail_org, name='post_detail_org'),
    #path('post/org/<int:pk>/edit/', views.post_edit_org, name='post_edit_org'),

    #path('post/tag/', views.TagFormView.as_view(), name='post_tag'),
    #path('post/tag/<int:pk>/', views.post_detail_tag, name='post_detail_tag'),

    #path('post/event/', views.EventFormView.as_view(), name='post_event'),
    #path('post/event/<int:pk>/', views.post_detail_event, name='post_detail_event'),

    #path('post/location/', views.LocationFormView.as_view(), name='post_location'),
    #path('post/location/<int:pk>/', views.post_detail_location, name='post_detail_location'),

    #url(r'^email/orgEmail=(?P<org_email>.*)&orgName=(?P<org_name>.*)&name=(?P<name>[a-zA-Z\s]+)&netID=(?P<net_id>[a-zA-Z0-9]+)&link=(?P<link>.*)$', views.EmailDetail.as_view(), name='Email Detail'),
    url(r'^event/(?P<event_id>[0-9]+)/$',
        views.EventDetail.as_view(), name='Event Details'),
    url(r'^org/(?P<org_id>[0-9]+)/$',
        views.OrgDetail.as_view(), name='Organizer Details'),
    url(r'^org/(?P<organizer_id>[0-9]+)/events/$',
        views.OrgEvents.as_view(), name='Organizer Events'),
    url(r'^loc/(?P<location_id>[0-9]+)/$',
        views.SingleLocationDetail.as_view(), name='Location Details'),
    url(r'^loc/all/$', views.AllLocationDetail.as_view(),
        name='All Location Details'),
    url(r'^tag/(?P<tag_id>[0-9]+)/$',
        views.SingleTagDetail.as_view(), name='Single Tag Details'),
    url(r'^tag/all/$',
        views.GetAllTags.as_view(), name='All Tag Details'),

    url(r'^media/(?P<img_id>[0-9]+)/$',
        views.ImageDetail.as_view(), name='Media Detail'),
    url(r'^feed/events/$', views.EventFeed.as_view(), name='Updated Events Feed'),
    url(r'^feed/org/timestamp=(?P<in_timestamp>{0})/$'.format(
        dateRegex), views.OrgFeed.as_view(), name='Updated Organizer Feed'),
    url(r'^generate_token/(?P<mobile_id>.*)/$',
        views.ObtainToken.as_view(), name='Create Mobile Token'),
    url(r'^reset_token/(?P<mobile_id>.*)/$',
        views.ResetToken.as_view(), name='Reset Mobile Token'),
    url(r'upload_image_s3/', views.UploadImage.as_view(),
        name='Upload Image to Amazon S3'),
    url(r'^attendance/increment/(?P<event_id>[0-9]+)/$',
        views.IncrementAttendance.as_view(), name="Increment Attendance"),
    url(r'^attendance/unincrement/(?P<event_id>[0-9]+)/$',
        views.UnincrementAttendance.as_view(), name="Unicrement Attendance"),
    url(r'^setMinVersion/(?P<version>.*)/$', views.SetMinVersionView.as_view()),
    url(r'^checkMinVersion/(?P<version>.*)/$',
        views.GetMinVersionView.as_view()),

    url(r'^users/$', views.UserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
    url(r'^api-auth/', authviews.obtain_auth_token),

    url(r'^logout/$', auth_views.LogoutView.as_view(next_page='/'), name='logout'),

    url(r'^apple-app-site-association', views.AppleAppSite.as_view(),
        name="Apple App Site Association"),

    url(r'^', TemplateView.as_view(template_name="main.html"))
]
