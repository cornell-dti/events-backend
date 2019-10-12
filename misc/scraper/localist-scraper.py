import requests
import datetime

class Event:
    def __init__(self, description, ):
        self 


### COLUMNS, in order ###
"""
Data (there is even more):
name: ['title']
description: ['description_text']
start_date: ['first_date']
end_date: ['last_date']
start_time(s): ['event_instances'][?]['event_instance']['start']
end_time(s) (if needed): ['event_instances'][?]['event_instance']['end']
private (boolean): ['private']
location (Ex: "Human Ecology Building (HEB)"): ['location_name']
room (Ex: "Level T Display Cases"): ['room_number']


NOTE: Orgs are tricky
There is a list of departments associated with the event, but there is no email
given. Each department has an internal ID which we can look into. 
There is also a field for contact info with a person's name, email, phone
number, but no organization name.
org_name(s): ['filters']['departments'][?]['name']
contact_name: ['custom_fields']['contact_name']
contact_email: ['custom_fields']['contact_email']
contact_phone: ['custom_fields']['contact_phone']
"""
###########################

if __name__ == '__main__':
        
    URL = "https://events.cornell.edu/api/2/events?start=2019-10-06&end=2019-10-31&pp=100"
    URL_ADDON = "&page="

    data_count = 0
    success_data_count = 0
    fail_data_count = 0

    page = 1
    maxPage = 1
    while page <= maxPage:
        page += 1
        with requests.get(URL+URL_ADDON+str(page)) as data:
            maxPage = data.json()['page']['total']
            for event in data.json()["events"]:
                try:
                    event = event['event']

                    name = event['title']
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
                    #private = event_data['private']
                    #url = event_data['url']
                    all_day = event['event_instances'][0]['event_instance']['all_day']

                    start = event['event_instances'][0]['event_instance']['start']
                    end = event['event_instances'][0]['event_instance']['end']
                    
                    #How do we handle?
                    if all_day and end is None:
                        end = start

                    org_name = event['filters']['departments'][0]['name']

                    # contact_name = event['custom_fields']['contact_name']
                    contact_email = event['custom_fields']['contact_email']
                    # contact_phone = event['custom_fields']['contact_phone']
                    
                    #for event_instance in event['event_instances']:
                        #do something with this
                        #put in list?
                        #start_time = event_instance['event_instance']['start']
                        #end_time = event_instance['event_instance']['end']

                    #for org in event['filters']['departments']:
                        #put in list?
                        #org_name = org['name']
                    
                
                    """
                    TODO: HOW TO MANUALLY ADD AN EVENT
                    """

                    if name == "" or name is None:
                        print("Missing name")
                        data_count += 1
                        fail_data_count += 1
                        continue

                    if description == "" or description is None:
                        print("Missing desc")
                        data_count += 1
                        fail_data_count += 1
                        continue

                    if (location == "" or location is None):
                        print("Missing location")
                        data_count += 1
                        fail_data_count += 1
                        continue

                    # if (room == "" or room is None):
                    #     data_count += 1
                    #     fail_data_count += 1
                    #     continue

                    if (latitude == "" or latitude is None or longitude == "" or longitude is None):
                        print("Missing coordinates")
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
                        print("Missing organizer email")
                        data_count += 1
                        fail_data_count += 1
                        continue

                    # if (contact_phone == "" or contact_phone is None):
                    #     data_count += 1
                    #     fail_data_count += 1
                    #     continue

                    iso_pattern = "%Y-%m-%dT%H:%M:%S%z"
                    start_obj = datetime.datetime.strptime(start, iso_pattern)
                    end_obj = datetime.datetime.strptime(end, iso_pattern)

                    start_date = start_obj.date()
                    start_time = start_obj.time()
                    end_date = end_obj.date()
                    end_time = end_obj.time()

                    #Recap
                    name = name
                    description = description
                    location = location
                    room = room
                    img_src = img_src
                    all_day = all_day
                    start_date = start_date
                    start_time = start_time
                    end_date = end_date
                    end_time = end_time
                    org_name = org_name
                    contact_name = contact_name
                    contact_email = contact_email
                    contact_phone = contact_phone

                    data_count += 1
                    success_data_count += 1
                except KeyError as e:
                    print("Missing " + str(e))
                    data_count += 1
                    fail_data_count += 1
                except:
                    print("random error lol")
                    data_count += 1
                    fail_data_count += 1
    print(f'Processed {data_count} lines of data. {success_data_count} success. {fail_data_count} failure.')