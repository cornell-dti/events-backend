import json

import requests

if __name__ == '__main__':
    MAX_EVENT_PER_PAGE = 100
    SCRAPER_START_DATE = "2019-10-30"
    SCRAPER_END_DATE = "2019-10-31"

    URL = "https://events.cornell.edu/api/2/events?start={0}&end={1}&pp={2}".format(SCRAPER_START_DATE,
                                                                                    SCRAPER_END_DATE,
                                                                                    MAX_EVENT_PER_PAGE)
    URL_ADDON = "&page="

    data_count = 0
    success_data_count = 0
    fail_data_count = 0

    page = 1
    maxPage = 0

    FILE_NAME = "events_{0}_{1}.json".format(SCRAPER_START_DATE,
                                             SCRAPER_END_DATE)

    with open(FILE_NAME, 'w') as f:
        data = requests.get(URL).json()
        maxPage = data['page']['total']
        for event in data["events"]:
            event['event']['tags'] = []
        while page < maxPage:
            extra = requests.get(URL + URL_ADDON + str(page)).json()
            for event in extra["events"]:
                event['event']['tags'] = []
            data['events'].extend(extra['events'])
            page += 1
        for event_id in data["events"]:
            try:
                event = event_id['event']

                event_name = event['title']
                description = event['description_text']
                # start_date = event['first_date']
                # end_date = event['last_date']
                location = event['location_name']
                room = event['room_number']
                latitude = event['geo']['latitude']
                longitude = event['geo']['longitude']

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

                data_count += 1
                success_data_count += 1
            except:
                data["events"].remove(event_id)
                data_count += 1
                fail_data_count += 1
        json.dump(data, f)
