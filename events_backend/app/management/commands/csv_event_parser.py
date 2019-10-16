from django.core.management.base import BaseCommand, CommandError
import sys
from dateutil.parser import parse
from datetime import datetime, timedelta
import re
import os
import csv
from app.models import Org, Event, Location
from time import sleep


class Command(BaseCommand):
    help = 'Parses events from csv and add them to the database'

    def add_arguments(self, parser):
        parser.add_argument(
            'path', help='Indicates the path of csv to be parsed')

    def handle(self, *args, **kwargs):
        DEFAULT_PASSWORD = 'pbkdf2_sha256$120000$qFamKdatf0if$+aI5iQne/Z+zGJU9EfWcoaaBRUCie/8Rltkz7XRH3fQ='
        EVENTS_FILE_NAME = kwargs['path']

        ### COLUMNS, in order ###
        """
        web-scraper-order
        web-scraper-start-url
        date
        event
        location_and_time (format: Fri 7 PM · CUPB (Cornell University Program Board) · Ithaca, New York)
        URL
        URL-href
        Location (format: either null or the actual location)
        Time (format: Sunday, September 22, 2019 at 12 PM – 6 PM)
        Attendance (format: 31 Going · 237 Interested)
        img-src
        description
        host (· Hosted by Cornell ACSU - Association of Computer Science Undergraduates and Cornell IEEE-The Institute of Electrical and Electronics Engineers)
        tags (by id and comma separated, so 4,1,9)
        """
        ###########################

        with open(EVENTS_FILE_NAME, encoding="utf8", errors="ignore") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            first_row_processed = False
            data_count = 0
            success_data_count = 0
            fail_data_count = 0
            for row in csv_reader:
                # web_scraper_order = row[0]
                # web_scraper_start_url = row[1]
                date = row[2]
                event_name = row[3]
                # location_and_time = row[4]
                # url = row[5]
                # url_href = row[6] not sure how i can this
                location = row[7]
                time = row[8]  # retrieve time
                attendance = row[9]
                img_src = row[10]
                description = row[11]
                host = row[12]
                location_specific = row[13]  # good but not always reliable
                # tags = ''
                # Tags may be empty cells
                # if len(row) >= 15:
                # tags = row[13]
                if not first_row_processed:
                    first_row_processed = True
                    continue
                else:
                    """HOW TO MANUALLY ADD AN EVENT
                    0. Manually go through the host column and modify the hosts so that it's only one org
                    For example, it would be "Hosted by _____" instead of "Hosted dby _____ and _______"
                    This is becau   se we want one organization per Host column, and some org names have an "and" in it so
                    we can't just separate them by "and".
                    1. Manually add tags from the pre-defined set (by id)
                    2. Add an entry for each org into backend_main_user
                    3. Add an entry into backend_main_org for the org
                    4. Add an entry into backend_main_media
                    5. Add an entry into backend_main_event_media
                    """
                    if host == "" or host == "null":
                        data_count += 1
                        fail_data_count += 1
                        continue

                    if event_name == "" or event_name == "null":
                        data_count += 1
                        fail_data_count += 1
                        continue

                    if location == "null":
                        location = ""

                    if location_specific == "null":
                        location_specific = ""

                    if location == "" and location_specific == "":
                        data_count += 1
                        fail_data_count += 1
                        continue

                    start_datetime, end_datetime = re.findall(
                        "(?! ).*?\d+[\:\d\d]*\s[A|P]M", time)

                    start_time, end_time = re.findall(
                        "\d+[\:\d{2}]*\s[A|P]M", time)

                    try:
                        if ((parse(start_datetime) - parse(date + " " + start_time)).total_seconds() != 0):
                            start_datetime = date + " " + start_time
                    except:
                        start_datetime = date + " " + start_time

                    if end_datetime == end_time:
                        end_datetime = date + " " + end_time
                    else:
                        end_datetime = end_datetime

                    try:
                        if (parse(end_datetime) - parse(start_datetime)).total_seconds() < 0:
                            end_datetime = end_date
                    except:
                        continue

                    event_name = event_name
                    location = location
                    location_specific = location_specific
                    start_date = datetime.strftime(
                        parse(start_datetime), "%Y-%m-%d")
                    start_time = datetime.strftime(
                        parse(start_datetime), "%H:%M:%S")
                    end_date = datetime.strftime(
                        parse(end_datetime), "%Y-%m-%d")
                    end_time = datetime.strftime(
                        parse(end_datetime), "%H:%M:%S")
                    description = description

                    host = re.search(
                        "(?![Hosted by]).*", host).group()
                    attendance = attendance
                    img_src = img_src

                    data_count += 1
                    success_data_count += 1

                    org_set = Org.objects.create(
                        name=host, bio="This is an organization manually created by DTI.", email="dti-dummy@cornell.edu")
                    location_set = Location.objects.create(
                        building=location if location != "" else location_specific, room=location_specific, place_id="-1")

                    event = Event(
                        name=event_name, description=description, start_date=start_date,
                        end_date=end_date, start_time=start_time, end_time=end_time, location=location_set, organizer=org_set)
                    event.save()

            print(
                f'Processed {data_count} lines of data. {success_data_count} success. {fail_data_count} failure.')
