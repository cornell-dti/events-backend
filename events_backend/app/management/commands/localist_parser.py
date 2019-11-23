import json
import re
from datetime import datetime

from app.models import Org, Event, Location, Media, Event_Media, Event_Org, Tag, Event_Tags
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand

SKIP_MISSING_ORG_INFO = False


def titlecase(s):
    return re.sub(r"[A-Za-z]+('[A-Za-z]+)?", lambda mo: mo.group(0).capitalize(), s)


class Command(BaseCommand):
    help = 'Parses events from json and add them to the database'

    def add_arguments(self, parser):
        parser.add_argument(
            'path', help='Indicates the path of json to be parsed')

    """
    Right now doesn't take any args
    What is a good way to pass in args?
    Strings representing start/end dates? (Ex: '2019-10-06')
    """

    def handle(self, *args, **kwargs):
        # Max pp is 100
        EVENTS_FILE_NAME = kwargs['path']

        data_count = 0
        success_data_count = 0
        fail_data_count = 0

        with open(EVENTS_FILE_NAME) as file:
            data = json.load(file)
            for event in data["events"]:
                try:
                    event = event['event']

                    event_name = event['title']
                    description = event['description_text']
                    location = event['location_name']
                    room = event['room_number']
                    latitude = event['geo']['latitude']
                    longitude = event['geo']['longitude']
                    tags = event['tags']
                    try:
                        place_id = event['place_id']
                    except KeyError:
                        place_id = -1

                    img_src = event['photo_url']
                    all_day = event['event_instances'][0]['event_instance']['all_day']

                    start = event['event_instances'][0]['event_instance']['start']
                    end = event['event_instances'][0]['event_instance']['end']

                    if start is not None and start[-3:] == ':00':
                        start = start[:-3] + '00'
                    if end is not None and end[-3:] == ':00':
                        end = end[:-3] + '00'

                    # How do we handle?
                    if all_day and end is None:
                        end = start

                    try:
                        org_name = event['filters']['departments'][0]['name']
                        contact_email = event['custom_fields']['contact_email']
                    except KeyError:
                        if SKIP_MISSING_ORG_INFO:
                            print("Missing org info, skipping")
                            data_count += 1
                            fail_data_count += 1
                            continue
                        else:
                            print("Missing org info, using default values")
                            org_name = "Cornell Organization"
                            contact_email = "donotdisplay@cornell.edu"

                    """
                    TODO: HOW TO MANUALLY ADD AN EVENT
                    """

                    if event_name == "" or event_name is None:
                        print("Missing name")
                        data_count += 1
                        fail_data_count += 1
                        continue

                    if description == "" or description is None:
                        print("Missing desc")
                        data_count += 1
                        fail_data_count += 1
                        continue

                    if (location == "" or location is None) and (room == "" or room is None):
                        print("Missing location or room")
                        data_count += 1
                        fail_data_count += 1
                        continue

                    if start == "" or start is None or end == "" or end is None:
                        print("Missing datetime")
                        data_count += 1
                        fail_data_count += 1
                        continue

                    if (latitude == "" or latitude is None or longitude == "" or longitude is None) and (
                            location == "" or location is None):
                        print("Missing location AND coordinates")
                        data_count += 1
                        fail_data_count += 1
                        continue

                    if org_name == "" or org_name is None:
                        print("Missing organizer name")
                        data_count += 1
                        fail_data_count += 1
                        continue

                    if room is None:
                        room = ''

                    iso_pattern = "%Y-%m-%dT%H:%M:%S%z"
                    start_obj = datetime.strptime(start, iso_pattern)
                    end_obj = datetime.strptime(end, iso_pattern)

                    start_date = start_obj.date()
                    start_time = start_obj.time()
                    end_date = end_obj.date()
                    end_time = end_obj.time()

                    # Recap
                    event_name = event_name
                    description = description
                    location = location
                    room = room
                    img_src = img_src
                    start_date = start_date
                    start_time = start_time
                    end_date = end_date
                    end_time = end_time
                    org_name = org_name
                    contact_email = contact_email
                    place_id = place_id
                    tags = tags

                    org_set = Org.objects.get_or_create(
                        name=org_name, bio="This is an organization manually created by DTI.",
                        email=contact_email)
                    location_set = Location.objects.get_or_create(
                        building=location,
                        room=room,
                        place_id=place_id)

                    event = Event.objects.get_or_create(
                        name=event_name, description=description, start_date=start_date,
                        end_date=end_date, start_time=start_time, end_time=end_time, num_attendees=0,
                        location=location_set[0], organizer=org_set[0])

                    if img_src == "":
                        media = Media.objects.create(uploaded_by=org_set[0])
                    else:
                        media = Media.objects.get_or_create(
                            link=img_src, uploaded_by=org_set[0])[0]

                    Event_Media.objects.get_or_create(
                        event=event[0], media=media)
                    Event_Org.objects.get_or_create(
                        event=event[0], org=org_set[0])

                    for t in tags:
                        if t == "":
                            continue
                        try:
                            tag = Tag.objects.get(name=titlecase(t))
                            Event_Tags.objects.get_or_create(
                                event=event[0], tags=tag)
                        except ObjectDoesNotExist:
                            print(
                                f'Tag {titlecase(t)} does not exist in database. Unable to associate event with specified tag.'
                            )
                    data_count += 1
                    success_data_count += 1
                except KeyError as e:
                    print("KeyError " + str(e))
                    data_count += 1
                    fail_data_count += 1
        print(f'Processed {data_count} lines of data. {success_data_count} success. {fail_data_count} failure.')
