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

urlpatterns = [
	url(r'^signup/$', ensure_csrf_cookie(views.SignUpView.as_view()), name="Sign-Up" ),
	url(r'^login/$', ensure_csrf_cookie(views.LoginView.as_view()), name="Login" ),
	url(r'^loggedin/$', views.check_login_status, name="Check-Login")
]
