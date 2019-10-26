import json
import re
from datetime import datetime

from app.models import Org, Event, Location, Media, Event_Media, Event_Org, Tag, Event_Tags
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand


def titlecase(s):
    return re.sub(r"[A-Za-z]+('[A-Za-z]+)?", lambda mo: mo.group(0).capitalize(), s)


class Command(BaseCommand):
    help = 'Parses events from csv and add them to the database'

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
                    # start_date = event['first_date']
                    # end_date = event['last_date']
                    location = event['location_name']
                    room = event['room_number']
                    latitude = event['geo']['latitude']
                    longitude = event['geo']['longitude']
                    tags = event['tags']
                    try:
                        place_id = event['place_id']
                    except KeyError:
                        place_id = -1;

                    # street = event['geo']['street']
                    # city = event['geo']['city']
                    # state = event['geo']['state']
                    # country = event['geo']['country']
                    # zipCode = event['geo']['zip']
                    # address = '{}, {}, {}, {}, {}'.format(street, city, state, country, zipCode)

                    img_src = event['photo_url']
                    # private = event_data['private']
                    # url = event_data['url']
                    all_day = event['event_instances'][0]['event_instance']['all_day']

                    start = event['event_instances'][0]['event_instance']['start']
                    end = event['event_instances'][0]['event_instance']['end']

                    # How do we handle?
                    if all_day and end is None:
                        end = start

                    org_name = event['filters']['departments'][0]['name']

                    # contact_name = event['custom_fields']['contact_name']

                    contact_email = "donotdisplay@cornell.edu"
                    try:
                        contact_email = event['custom_fields']['contact_email']
                    except KeyError:
                        print("using dummy email")

                    # contact_phone = event['custom_fields']['contact_phone']

                    # for event_instance in event['event_instances']:
                    # do something with this
                    # put in list?
                    # start_time = event_instance['event_instance']['start']
                    # end_time = event_instance['event_instance']['end']

                    # for org in event['filters']['departments']:
                    # put in list?
                    # org_name = org['name']

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

                    # if (room == "" or room is None):
                    #     data_count += 1
                    #     fail_data_count += 1
                    #     continue

                    if (latitude == "" or latitude is None or longitude == "" or longitude is None) and (
                            location == "" or location is None):
                        print("Missing location AND coordinates")
                        data_count += 1
                        fail_data_count += 1
                        continue

                    # if (address == "" or address is None):
                    #     data_count += 1
                    #     fail_data_count += 1
                    #     continue

                    if (img_src == "" or img_src is None):
                        print("Missing image link")
                        data_count += 1
                        fail_data_count += 1
                        continue

                    if (org_name == "" or org_name is None):
                        print("Missing organizer name")
                        data_count += 1
                        fail_data_count += 1
                        continue

                    # if (contact_name == "" or contact_name is None):
                    #     data_count += 1
                    #     fail_data_count += 1
                    #     continue

                    if (contact_email == "" or contact_email is None):
                        # print("Missing organizer email")
                        contact_email = "donotdisplay@cornell.edu"
                        continue

                    # if (contact_phone == "" or contact_phone is None):
                    #     data_count += 1
                    #     fail_data_count += 1
                    #     continue

                    if room is None:
                        room = ''

                    iso_pattern = "%Y-%m-%dT%H:%M:%S%z"
                    start_obj = datetime.strptime(start, iso_pattern)
                    end_obj = datetime.strptime(end, iso_pattern)

                    latlng = {latitude, longitude}

                    start_date = start_obj.date()
                    start_time = start_obj.time()
                    end_date = end_obj.date()
                    end_time = end_obj.time()

                    # Recap
                    event_name = event_name
                    description = description
                    location = location
                    room = room
                    latlng = latlng
                    img_src = img_src
                    all_day = all_day
                    start_date = start_date
                    start_time = start_time
                    end_date = end_date
                    end_time = end_time
                    org_name = org_name
                    # contact_name = contact_name
                    contact_email = contact_email
                    # contact_phone = contact_phone
                    tags = tags

                    # other stuff
                    org_set = Org.objects.get_or_create(
                        name=org_name, bio="This is an organization manually created by DTI.",
                        email=contact_email)
                    location_set = Location.objects.get_or_create(
                        building=location,
                        room=room,
                        place_id=place_id)

                    # event = Event.objects.get_or_create(
                    #     name=event_name, description=description, start_date=start_date,
                    #     end_date=end_date, start_time=start_time, end_time=end_time,
                    #     num_attendees=attendance, location=location_set[0], organizer=org_set[0])

                    event = Event.objects.get_or_create(
                        name=event_name, description=description, start_date=start_date,
                        end_date=end_date, start_time=start_time, end_time=end_time, num_attendees=0,
                        location=location_set[0], organizer=org_set[0])

                    media = Media.objects.get_or_create(
                        link=img_src, uploaded_by=org_set[0])

                    Event_Media.objects.get_or_create(
                        event=event[0], media=media[0])
                    Event_Org.objects.get_or_create(
                        event=event[0], org=org_set[0])

                    for t in tags:
                        if t == "":
                            print(t)
                            continue
                        try:
                            tag = Tag.objects.get(name=titlecase(t))
                            print(tag)
                            Event_Tags.objects.get_or_create(
                                event=event[0], tags=tag)
                        except ObjectDoesNotExist:
                            print(
                                "Tag {} does not exist in database. Unable to associate event with specified tag.".format(
                                    titlecase(t)
                                )
                            )

                    data_count += 1
                    success_data_count += 1
                except KeyError as e:
                    print("KeyError " + str(e))
                    data_count += 1
                    fail_data_count += 1
                # except:
                #     e = sys.exc_info()[1]
                #     print("random error lol " + str(e))
                #     data_count += 1
                #     fail_data_count += 1
        print(f'Processed {data_count} lines of data. {success_data_count} success. {fail_data_count} failure.')
