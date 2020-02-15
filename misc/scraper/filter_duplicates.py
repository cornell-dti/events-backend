import json

if __name__ == '__main__':

    ignore_present = True
    remove_invalid = False

    data_count = 0
    success_data_count = 0
    fail_data_count = 0

    EXT = ".json"
    FILE_NAME = "events_2019-10-01_2019-11-04"
    IN_FILE = FILE_NAME + EXT
    OUT_FILE = FILE_NAME + "_filtered" + EXT

    with open(IN_FILE) as f:
        data = json.load(f)
        titles = set()
        final_events = []
        for event_id in data["events"]:
            event = event_id["event"]
            if event["title"] is not None and event["title"] not in titles:
                if (event["url"] is not None and "cinema.cornell.edu" in event["url"]) or (
                        event["tags"] and "Cornell Cinema" in event["tags"]):
                    continue
                final_events.append(event)
                titles.add(event["title"])
        data["events"] = final_events
        with open(OUT_FILE, "w") as w:
            json.dump(data, w)
            w.close()
        f.close()
