import json

import googlemaps

if __name__ == '__main__':

    ignore_present = True

    data_count = 0
    success_data_count = 0
    fail_data_count = 0

    EXT = ".json"
    FILE_NAME = "events_2019-10-19_2019-10-20"
    IN_FILE = FILE_NAME + EXT
    OUT_FILE = FILE_NAME + "_place_id" + EXT

    gmaps = googlemaps.Client(key='API Key')
    with open(IN_FILE) as f:
        data = json.load(f)
        for event_id in data["events"]:
            api_result = -1;
            try:
                event = event_id['event']

                location = event['location_name']
                room = event['room_number']
                latitude = event['geo']['latitude']
                longitude = event['geo']['longitude']

                # Skip over if there is already a place_id entry
                if ignore_present:
                    try:
                        if event['place_id'] != -1:
                            print("Place ID already present")
                            data_count += 1
                            fail_data_count += 1
                            continue
                    except:
                        api_result = -1

                if latitude == "" or latitude is None or longitude == "" or longitude is None:
                    print("Missing coordinates")
                    data_count += 1
                    fail_data_count += 1
                    continue

                reverse = gmaps.reverse_geocode((latitude, longitude))
                api_result = reverse[0]['place_id']

                data_count += 1
                success_data_count += 1
            except:
                # data["events"].remove(event_id)
                data_count += 1
                fail_data_count += 1
            event['place_id'] = api_result
        with open(OUT_FILE, "w") as w:
            json.dump(data, w)
            w.close()
        f.close()
