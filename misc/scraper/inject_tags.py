import json

if __name__ == '__main__':

    ignore_present = True
    remove_invalid = False

    data_count = 0
    success_data_count = 0
    fail_data_count = 0

    EXT = ".json"
    FILE_NAME = "events_2019-10-27_2019-11-04"
    IN_FILE = FILE_NAME + EXT
    OUT_FILE = FILE_NAME + "_tags" + EXT

    mapping = {
        "departments": {
            "Athletics": ["Athletic"],
            "Department of Music": ["Music"],
            "Johnson Museum of Art": ["Art"],
            "Government": ["Government"],
            "Mario Einaudi Center for International Studies": ["Government", "International"],
            "Cornell Cinema": ["Cornell Cinema"],
            "Department of Performing and Media Arts": ["Art", "Theater", "Dance"],
            "Campus Sustainability Office": ["Sustainability"],
            "Global Cornell": ["International"],
            "Cornell China Center": ["International"]
        },
        "groups": {
            "Small Farms Program: Adirondacks": ["CALS"],
            "Games Club": ["Social", "Gaming"],
            "CUJazz": ["Music", "Jazz", "Theater", "Art"],
            "Cornell Cinema": ["Cornell Cinema"],
            "Cornell Minds Matter": ["Mental-Health"],
            "Class Councils": ["Government", "Student-Government"],
            "Cornell Contemporary China Initiative": ["International"],
            "Campus Sustainability Office": ["Sustainability"],
        },
        "keywords": {
            "Games": ["Social", "Gaming"],
            "gaming": ["Social", "Gaming"],
            "china": ["International"],
            "board games": ["Social", "Gaming"],
            "CUOrgans": ["Theater", "Music"],
            "Cornell Cinema": ["Cornell Cinema"]
        }
    }

    with open(IN_FILE) as f:
        data = json.load(f)
        for event_id in data["events"]:
            try:
                event = event_id['event']

                tags = event['tags']

                if tags == "" or tags is None:
                    tags = {}
                    continue

                if 'groups' in event:
                    for group in event['groups']:
                        match = mapping.get("groups").get(group['name'])
                        if match is not None:
                            tags.extend(mapping.get("groups").get(group['name']))

                if 'keywords' in event:
                    for keyword in event['keywords']:
                        match = mapping.get("keywords").get(keyword)
                        if match is not None:
                            tags.extend(match)

                if 'filters' in event and 'departments' in event['filters']:
                    for department in event['filters']['departments']:
                        match = mapping.get("departments").get(department['name'])
                        if match is not None:
                            tags.extend(match)

                event['tags'] = list(set(tags))

                data_count += 1
                success_data_count += 1
            except ChildProcessError:
                data_count += 1
                fail_data_count += 1
        with open(OUT_FILE, "w") as w:
            json.dump(data, w)
            w.close()
        f.close()
