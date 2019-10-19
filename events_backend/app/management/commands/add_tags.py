import csv
import json
import os
import re
import sys
from datetime import datetime
from time import sleep

import requests
from app.models import Tag
from dateutil.parser import parse
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Parses events from csv and add them to the database'

    # def add_arguments(self, parser):
    #     parser.add_argument(
    #         'path', help='Indicates the path of json to be parsed')

    """
    Right now doesn't take any args
    What is a good way to pass in args?
    Strings representing start/end dates? (Ex: '2019-10-06')
    """

    def handle(self, *args, **kwargs):
        # Max pp is 100
        tags = ['academic',
                'professional',
                'entrepreneurship',
                'engineering',
                'hotel',
                'ILR',
                'hum-ec',
                'aap',
                'cals',
                'a&s',
                'design',
                'business',
                'acapella',
                'jazz',
                'free-food',
                'government',
                'art',
                'tech',
                'philanthropy',
                'networking',
                'speaker',
                'alumni',
                'comedy',
                'astronomy',
                'biology',
                'music',
                'language',
                'theater',
                'dance',
                'consulting',
                'investing',
                'political',
                'religion',
                'greek-life',
                'environment',
                'outdoors',
                'varsity-sports',
                'sports',
                'concert',
                'health',
                'cultural',
                'project-team',
                'finance',
                'graduate',
                'law',
                'fashion',
                'sustainability',
                'education',
                'medical',
                'publication',
                'student-government',
                'debate',
                'gaming',
                'kid-friendly',
                'nightlife',
                'leadership',
                'international',
                'info-session',
                'interview-prep',
                'recruitment',
                'mental-health',
                'workshop',
                'fundraiser',
                'career-fair',
                'hackathon',
                'lecture',
                'exhibition',
                'bake-sale',
                'corporate',
                'mentorship',
                ]
        for tag in tags:
            Tag.objects.create(name=tag)