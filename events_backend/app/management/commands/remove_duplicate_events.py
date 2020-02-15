import boto3
from django.conf import settings

from app.models import Event
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Remove duplicate events that share the same name'

    def handle(self, *args, **kwargs):
        ## Ignore events tagged as 'movie'
        ignore = [88]
        for name in Event.objects.exclude(event_tags__tags_id__in=ignore).values_list('name', flat=True).distinct():
            Event.objects.filter(
                pk__in=Event.objects.filter(name=name).values_list('id', flat=True).order_by('start_date')[1:]).delete()
