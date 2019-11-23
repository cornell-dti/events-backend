import json

import requests
from geopy.distance import geodesic

MAX_EVENT_PER_PAGE = 100
SCRAPER_START_DATE = "2019-11-21"
SCRAPER_END_DATE = "2019-12-06"
ITHACA_COORDS = (42.4534492, -76.4735027)
MAX_DIST_MILES = 7
IGNORE_WORDS = ['faculty', "staff", "instructor", "phd", "postdoc", "grad", "resident", "member", "rose"]


def is_nearby_event(lat, lon):
    return geodesic(ITHACA_COORDS, (lat, lon)).miles <= MAX_DIST_MILES


def is_valid_event(event_id):
    try:
        event = event_id['event']

        event_name = event['title']
        description = event['description_text']
        location = event['location_name']
        room = event['room_number']
        latitude = event['geo']['latitude']
        longitude = event['geo']['longitude']

        keywords = []
        try:
            keywords = event['keywords']
        except KeyError:
            pass

        groups = []
        try:
            groups = event['groups']
        except KeyError:
            pass

        departments = []
        try:
            departments = event['filters']['departments']
        except KeyError:
            pass

        try:
            open_to = event["custom_fields"]["open_to"].lower()
            if any(word.lower() in open_to for word in IGNORE_WORDS):
                return False
        except KeyError:
            pass

        img_src = event['photo_url']
        all_day = event['event_instances'][0]['event_instance']['all_day']

        start = event['event_instances'][0]['event_instance']['start']
        end = event['event_instances'][0]['event_instance']['end']

        # How do we handle?
        if all_day and end is None:
            end = start

        if event_name == "" or event_name is None:
            print("Missing name")
            return False

        if description == "" or description is None:
            print("Missing desc")
            return False

        if (location == "" or location is None) and (room == "" or room is None):
            print("Missing location or room")
            return False

        if start == "" or start is None or end == "" or end is None:
            print("Missing datetime")
            return False

        if latitude == "" or latitude is None or longitude == "" or longitude is None:
            if location == "" or location is None:
                print("Missing location AND coordinates")
                return False
        elif not is_nearby_event(latitude, longitude):
            print("Event too far away")
            return False

        if img_src == "" or img_src is None:
            print("Missing image link")
            return False

        if "CCE" in keywords or "CCE" in groups or any(x['name'].startswith("CCE") for x in departments):
            print("Ignoring CCE events")
            return False
    except:
        return False
    return True


if __name__ == '__main__':

    URL = f"https://events.cornell.edu/api/2/events?start={SCRAPER_START_DATE}&end={SCRAPER_END_DATE}&pp={MAX_EVENT_PER_PAGE}"

    URL_ADDON = "&page="

    data_count = 0
    success_data_count = 0
    fail_data_count = 0

    FILE_NAME = f"events_{SCRAPER_START_DATE}_{SCRAPER_END_DATE}.json"

    with open(FILE_NAME, 'w') as f:
        data = requests.get(URL).json()
        page = 1
        max_page = data['page']['total']
        for event in data["events"]:
            event['event']['tags'] = []
        while page < max_page:
            extra = requests.get(URL + URL_ADDON + str(page)).json()
            for event in extra["events"]:
                event['event']['tags'] = []
            data['events'].extend(extra['events'])
            page += 1
        data["events"] = [x for x in data["events"] if is_valid_event(x)]
        json.dump(data, f)
