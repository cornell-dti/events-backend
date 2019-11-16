# urls.py
# Arnav Ghosh, Jessica Zhao, Jill Wu, Adit Gupta
# 17th Sept. 2018

from django.conf.urls import url
from django.views.decorators.csrf import ensure_csrf_cookie
from . import views

urlpatterns = [
    # login/signup/change login credentials
    url(r"^signup/?$", ensure_csrf_cookie(views.SignUp.as_view()), name="Sign-Up"),
    url(r"^login/?$", ensure_csrf_cookie(views.Login.as_view()), name="Login"),
    url(r"^loggedin/?$", views.check_login_status, name="Check-Login"),
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
    url(r'^increment_attendance/(?P<event_id>[0-9]+)/$',
        views.OrgEvents.as_view({'post': 'increment_attendance'}), name="Increment-Attendance"),
    url(r'^decrement_attendance/(?P<event_id>[0-9]+)/$',
        views.OrgEvents.as_view({'post': 'decrement_attendance'}), name="Decrement-Attendance"),

    url(r"^sign_s3/?$", views.GetSignedRequest.as_view(), name="Get-Signed-Request"),
    url(r"^get_all_tags/?$", views.GetAllTags.as_view(), name="Get-Tags"),
]
