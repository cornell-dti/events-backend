# urls.py
# Arnav Ghosh, Jessica Zhao, Jill Wu, Adit Gupta
# 17th Sept. 2018

from django.conf.urls import url
from django.views.decorators.csrf import ensure_csrf_cookie
from . import views

urlpatterns = [
    # login/signup
    url(r"^signup/$", ensure_csrf_cookie(views.SignUp.as_view()), name="Sign-Up"),
    url(r"^login/$", ensure_csrf_cookie(views.Login.as_view()), name="Login"),
    url(r"^loggedin/$", views.check_login_status, name="Check-Login"),
    # profile
    url(r"^profile/$", views.UserProfile.as_view(), name="Profile"),
    url(r"^change_password/$", views.ChangePassword.as_view(), name="Change-Password"),
    url(
        r"^change_org_email/$", views.ChangeOrgEmail.as_view(), name="Change-Org-Email"
    ),
    # events
    url(
        r"^add_or_edit_event/$",
        views.AddOrEditEvent.as_view(),
        name="Add-Or-Edit-Event",
    ),
    url(
        r"^delete_event/(?P<event_id>[0-9]+)/$",
        views.DeleteEvents.as_view(),
        name="Delete-Event",
    ),
    url(r"^get_events/(?P<page>[0-9]+)/$", views.GetEvents.as_view(), name="Get-Events"),
    url(r"^sign_s3/$", views.GetSignedRequest.as_view(), name="Get-Signed-Request"),
    url(r"^get_all_tags/$", views.GetAllTags.as_view(), name="Get-Tags"),
]
