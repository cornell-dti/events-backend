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

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include('app.api_urls')),

    url(r'^media/(?P<img_id>[0-9]+)/$',
        views.ImageDetail.as_view(), name='Media Detail'),
    url(r'upload_image_s3/', views.UploadImage.as_view(),
        name='Upload Image to Amazon S3'),

    url(r'^users/$', views.UserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
    url(r'^api-auth/', authviews.obtain_auth_token),

    url(r'^logout/$', auth_views.LogoutView.as_view(next_page='/'), name='logout'),

    url(r'^apple-app-site-association', views.AppleAppSite.as_view(),
        name="Apple App Site Association"),

    url(r'^', TemplateView.as_view(template_name="main.html"))
]
