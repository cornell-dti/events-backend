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


MAX_NAME_LENGTH = 100
MAX_DESC_LENGTH = 500
MAX_TAG_LENGTH = 50
MAX_CONTACT_LENGTH = 100
MAX_WEBSITE_LENGTH = 100
MAX_TOKEN_LENGTH = 2056

class Event(models.Model):
    name = models.CharField(max_length = MAX_NAME_LENGTH)
    description = models.CharField(max_length = MAX_DESC_LENGTH)
    start_date = models.DateField()
    end_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    num_attendees = models.IntegerField(default=0)
    is_public = models.BooleanField(default=True)
    organizer = models.ForeignKey('Org', on_delete=models.CASCADE)
    location = models.ForeignKey('Location', on_delete=models.CASCADE)
    history = HistoricalRecords()

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length = MAX_TAG_LENGTH)

    def __str__(self):
        return self.name

class Event_Tags(models.Model):
    event_id = models.ForeignKey('Event', on_delete=models.CASCADE, related_name = "event_tags")
    tags_id = models.ForeignKey('Tag',on_delete=models.CASCADE)

    def __str__(self):
        return "{0} - {1}".format(self.event_id, self.tags_id)


class Org(models.Model):
    name = models.CharField(max_length = MAX_NAME_LENGTH)
    description = models.CharField(max_length = MAX_DESC_LENGTH)
    website = models.CharField(max_length=MAX_WEBSITE_LENGTH)
    photo = models.ForeignKey('Media',on_delete=models.CASCADE, blank=True, null=True)

    verified = models.BooleanField(default = False)
    history = HistoricalRecords()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name = 'org', on_delete=models.CASCADE) #user

    def __str__(self):
        return self.name

class Event_Org(models.Model):
    event_id = models.ForeignKey('Event', on_delete=models.CASCADE)
    org_id = models.ForeignKey('Org',on_delete=models.CASCADE)

    def __str__(self):
        return "{0} - {1}".format(self.org_id, self.event_id)

class Org_Tags(models.Model):
    org_id = models.ForeignKey('Org',on_delete=models.CASCADE)
    tags_id = models.ForeignKey('Tag',on_delete=models.CASCADE)

    def __str__(self):
        return "{0} - {1}".format(self.event_id, self.tags_id)

class Location(models.Model):
    building = models.CharField(max_length = MAX_NAME_LENGTH)
    place_id = models.CharField(max_length = MAX_NAME_LENGTH)

    def __str__(self):
        return self.building

class UserID(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    token = models.CharField(max_length = MAX_TOKEN_LENGTH)
    #TODO: can a token be stored as a string

class Attendance(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event_id = models.ForeignKey('Event', on_delete=models.CASCADE)

    def __str__(self):
        return "{0} - {1}".format(self.user_id, self.event_id)

class Media(models.Model):
    name = models.CharField(max_length = MAX_NAME_LENGTH)
    file = models.FileField(upload_to="cu_events_images", blank = False)
    uploaded_by = models.ForeignKey('Org',on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Event_Media(models.Model):
    event_id = models.ForeignKey('Event', on_delete=models.CASCADE, related_name = "event_media")
    media_id = models.ForeignKey('Media',on_delete=models.CASCADE)

class Org_Media(models.Model):
    org_id = models.ForeignKey('Org', on_delete=models.CASCADE)
    media_id = models.ForeignKey('Media',on_delete=models.CASCADE)

class Profile(models.Model):
    org_name = models.CharField(max_length=30, blank=True)
    name = models.CharField(max_length=30, blank=True)
    netid = models.CharField(max_length=30, blank=True)
    facebook = models.CharField(max_length=30, blank=True)
    website = models.CharField(max_length=30, blank=True)
    contact_us = models.BooleanField(default = False)
    verified = models.BooleanField(default = False)

class UserManager(BaseUserManager):

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class Organization(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def get_short_name(self):
        return self.email

    def __str__(self):
        return self.email
