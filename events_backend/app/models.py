# models.py
# Arnav Ghosh, Jessica Zhao, Jill Wu, Adit Gupta
# 17th Sept. 2018

import datetime
from django.db import models
from django.conf import settings
from django.utils import timezone
from simple_history.models import HistoricalRecords
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments import highlight

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

MAX_NAME_LENGTH = 100
MAX_DESC_LENGTH = 500
MAX_TAG_LENGTH = 50
MAX_CONTACT_LENGTH = 100
MAX_WEBSITE_LENGTH = 100
MAX_TOKEN_LENGTH = 2056
MAX_ROOM_LENGTH = 100


class UserManager(BaseUserManager):
    class Meta:
        app_label = 'app'

    def _create_user(self, username, password, **extra_fields):
        """
        Creates and saves a User with the given username and password.
        """
        if not username:
            raise ValueError("The username must be set")
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    class Meta:
        app_label = 'app'

    username = models.TextField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "username"

    def get_short_name(self):
        return self.username

    def __str__(self):
        return self.username

class Mobile_User(models.Model):
    class Meta:
        app_label = 'app'

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    mobile_id = models.CharField(max_length=MAX_TOKEN_LENGTH)


class Org(models.Model):
    class Meta:
        app_label = 'app'

    owner = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)

    name = models.CharField(max_length=30)
    bio = models.CharField(max_length=MAX_DESC_LENGTH, default="", blank=True)
    website = models.CharField(
        max_length=MAX_WEBSITE_LENGTH, default="", blank=True)
    email = models.CharField(
        max_length=MAX_WEBSITE_LENGTH, default="", blank=True)

    history = HistoricalRecords()

    tags = models.ManyToManyField("Tag", through="Org_Tags")
    photo = models.ManyToManyField("Media", through="Org_Media")


class Org_Tags(models.Model):
    class Meta:
        app_label = 'app'

    org_id = models.ForeignKey(
        "Org", on_delete=models.CASCADE, related_name="org_tags")
    tags_id = models.ForeignKey("Tag", on_delete=models.CASCADE)

    def __str__(self):
        return "{0} - {1}".format(self.org_id, self.tags_id)

class Verified_Emails(models.Model):
    class Meta:
            app_label = 'app'

    email = models.EmailField(unique=True)


# class Org(models.Model):
#     name = models.CharField(max_length=MAX_NAME_LENGTH)
#     description = models.CharField(max_length=MAX_DESC_LENGTH)
#     website = models.CharField(max_length=MAX_WEBSITE_LENGTH)
#     photo = models.ForeignKey(
#         'Media', on_delete=models.CASCADE, blank=True, null=True)
#     contact = models.CharField(max_length=MAX_CONTACT_LENGTH)

#     verified = models.BooleanField(default=False)
#     history = HistoricalRecords()
#     owner = models.ForeignKey(
#         'auth.User', related_name='org', on_delete=models.CASCADE)  # user

#     def __str__(self):
#         return self.name


class Event(models.Model):
    class Meta:
        app_label = 'app'

    name = models.CharField(max_length=MAX_NAME_LENGTH)
    description = models.CharField(max_length=MAX_DESC_LENGTH)
    start_date = models.DateField()
    end_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    num_attendees = models.IntegerField(default=0)
    is_public = models.BooleanField(default=True)
    organizer = models.ForeignKey("Org", on_delete=models.CASCADE)
    location = models.ForeignKey("Location", on_delete=models.CASCADE)
    history = HistoricalRecords()

    tags = models.ManyToManyField("Tag", through="Event_Tags")
    media = models.ManyToManyField("Media", through="Event_Media")

    def __str__(self):
        return self.name


class Location(models.Model):
    class Meta:
        app_label = 'app'

    room = models.CharField(max_length = MAX_NAME_LENGTH)
    building = models.CharField(max_length = MAX_NAME_LENGTH)
    place_id = models.CharField(max_length = MAX_NAME_LENGTH)

    def __str__(self):
        return self.building


class Attendance(models.Model):
    class Meta:
        app_label = 'app'

    user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event_id = models.ForeignKey("Event", on_delete=models.CASCADE)

    def __str__(self):
        return "{0} - {1}".format(self.user_id, self.event_id)


class Event_Org(models.Model):
    class Meta:
        app_label = 'app'

    event_id = models.ForeignKey("Event", on_delete=models.CASCADE)
    org_id = models.ForeignKey("Org", on_delete=models.CASCADE)

    def __str__(self):
        return "{0} - {1}".format(self.org_id, self.event_id)


class Event_Tags(models.Model):
    class Meta:
        app_label = 'app'

    event_id = models.ForeignKey("Event", on_delete=models.CASCADE)
    tags_id = models.ForeignKey("Tag", on_delete=models.CASCADE)

    def __str__(self):
        return "{0} - {1}".format(self.event_id, self.tags_id)


class Event_Media(models.Model):
    class Meta:
        app_label = "app"

    event = models.ForeignKey("Event", on_delete=models.CASCADE)
    media = models.ForeignKey("Media", on_delete=models.CASCADE)


class Org_Media(models.Model):
    class Meta:
        app_label = 'app'

    org = models.ForeignKey("Org", on_delete=models.CASCADE)
    media = models.ForeignKey("Media", on_delete=models.CASCADE)


class Tag(models.Model):
    class Meta:
        app_label = 'app'

    name = models.CharField(max_length=MAX_TAG_LENGTH)

    def __str__(self):
        return self.name


class Media(models.Model):
    class Meta:
        app_label = 'app'

    link = models.TextField()
    uploaded_by = models.ForeignKey("Org", on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.link
# class Org_Media(models.Model):
#
#    class Meta:
#        app_label = 'app'
#
#    #org_id = models.ForeignKey('Org', on_delete=models.CASCADE, related_name = "org_media")
#    media_id = models.ForeignKey('Media',on_delete=models.CASCADE)

# class Profile(models.Model):
#    org_name = models.CharField(max_length=30, blank=True)
#    name = models.CharField(max_length=30, blank=True)
#    netid = models.CharField(max_length=30, blank=True)
#    facebook = models.CharField(max_length=30, blank=True)
#    website = models.CharField(max_length=30, blank=True)
#    contact_us = models.BooleanField(default = False)
#    verified = models.BooleanField(default = False)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
