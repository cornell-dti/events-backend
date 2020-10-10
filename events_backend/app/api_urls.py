# urls.py
# Arnav Ghosh, Jessica Zhao, Jill Wu, Adit Gupta
# 17th Sept. 2018

from django.conf.urls import url
from django.views.decorators.csrf import ensure_csrf_cookie
from . import views

urlpatterns = [
    # tokens
    url(r'^get_token/(?P<id_token>.*)/?$',
        views.Tokens.as_view({'get': 'get_token'}), name='Get-Token'),

    # login/signup/change login credentials
    url(r"^signup/?$", ensure_csrf_cookie(views.SignUp.as_view()), name="Sign-Up"),
    url(r"^login/?$", ensure_csrf_cookie(views.Login.as_view()), name="Login"),
    url(r"^logged_in/?$", views.check_login_status, name="Check-Login"),
    url(r"^change_password/?$",
        views.ChangeLoginCredentials.as_view({'post': 'change_password'}), name="Change-Password"),
    url(
        r"^change_login_email/?$",
        views.ChangeLoginCredentials.as_view({'post': 'change_login_email'}), name="Change-Org-Email"
    ),

    # profile
    url(r"^get_profile/(?P<org_id>[0-9]+)/?$",
        views.UserProfile.as_view({'get': 'get_profile'}), name="Get-Profile"),
    url(r"^get_profile/?$",
        views.UserProfile.as_view({'get': 'get_profile'}), name="Get-Profile"),
    url(r"^edit_profile/?$",
        views.UserProfile.as_view({'post': 'edit_profile'}), name="Edit-Profile"),

    # events
    url(r"^get_event/(?P<event_id>[0-9]+)/?$",
        views.OrgEvents.as_view({'get': 'get_event'}), name="Get-Org-Event"),
    url(r"^get_events/(?P<org_id>[0-9]+)/?$",
        views.OrgEvents.as_view({'get': 'get_events'}), name="Get-Org-Events"),
    url(r"^get_events/?$",
        views.OrgEvents.as_view({'get': 'get_events'}), name="Get-Events"),
    url(r"^add_event/?$",
        views.OrgEvents.as_view({'post': 'add_event'}), name="Add-Event"),
    url(r"^edit_event/?$",
        views.OrgEvents.as_view({'post': 'edit_event'}), name="Edit-Event"),
    url(r"^delete_event/(?P<event_id>[0-9]+)/?$",
        views.OrgEvents.as_view({'post': 'delete_event'}), name="Delete-Event"),
    url(r'^increment_attendance/(?P<event_id>[0-9]+)/?$',
        views.OrgEvents.as_view({'post': 'increment_attendance'}), name="Increment-Attendance"),
    url(r'^decrement_attendance/(?P<event_id>[0-9]+)/?$',
        views.OrgEvents.as_view({'post': 'decrement_attendance'}), name="Decrement-Attendance"),

    # tags
    url(r'^get_tag/(?P<tag_id>[0-9]+)/?$',
        views.Tags.as_view({'get': 'get_tag'}), name='Get-Tag'),
    url(r'^get_all_tags/?$',
        views.Tags.as_view({'get': 'get_all_tags'}), name='Get-All-Tags'),

    # locations
    url(r'^get_location/(?P<location_id>[0-9]+)/?$',
        views.Locations.as_view({'get': 'get_location'}), name='Get-Location'),
    url(r'^get_all_locations/?$',
        views.Locations.as_view({'get': 'get_all_locations'}), name='Get-All-Locations'),

    # feeds
    url(r'^get_event_feed/?$',
        views.Feeds.as_view({'get': 'get_event_feed'}), name='Get-Event-Feed'),
]
