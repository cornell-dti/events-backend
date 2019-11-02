import boto3
from django.conf import settings

from app.models import Event
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Uploads media to s3 if not there already'

    def handle(self, *args, **kwargs):
        for name in Event.objects.exclude(event_tags__tags_id=88).values_list('name', flat=True).distinct():
            Event.objects.filter(
                pk__in=Event.objects.filter(name=name).values_list('id', flat=True).order_by('start_date')[1:]).delete()
