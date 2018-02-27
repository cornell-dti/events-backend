from django.db import models
from django.utils import timezone
import datetime

# Create your models here.
class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    start_date = models.DateField
    end_date = models.DateField
    start_time = models.DateTimeField
    end_time = models.DateTimeField
    num_attendees = models.IntegerField
    event_type = models.CharField(
        max_length=7,
        choices=(PUBLIC, PRIVATE),
        default=PUBLIC,
    )

class Tags(models.Model):
    name = models.CharField(max_length = 50)

class Event_Tags(models.Model):
    event_id = models.ForeignKey('Event', on_delete=CASCADE)
    tags_id = models.ForeignKey('Tags',on_delete=CASCADE)
