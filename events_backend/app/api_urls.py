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
    url(r"^get_profile/(?P<org_id>[0-9]+)/$",
        views.UserProfile.as_view({'get': 'get_profile'}), name="Get-Profile"),
    url(r"^get_profile/$",
        views.UserProfile.as_view({'get': 'get_profile'}), name="Get-Profile"),
    url(r"^edit_profile/$",
        views.UserProfile.as_view({'post': 'edit_profile'}), name="Edit-Profile"),
    url(r"^change_password/$",
        views.UserProfile.as_view({'post': 'change_password'}), name="Change-Password"),
    url(
        r"^change_org_email/$",
        views.UserProfile.as_view({'post': 'change_org_email'}), name="Change-Org-Email"
    ),
    # events
    url(
        r"^org_events/$",
        views.OrgEvents.as_view(),
        name="Org-Events",
    ),
    url(r"^sign_s3/$", views.GetSignedRequest.as_view(), name="Get-Signed-Request"),
    url(r"^get_all_tags/$", views.GetAllTags.as_view(), name="Get-Tags"),
]
