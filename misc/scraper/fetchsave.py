import json

import requests

solditems = requests.get('https://github.com/timeline.json')  # (your url)
data = solditems.json()
with open('data.json', 'w') as f:
    json.dump(data, f)

if __name__ == '__main__':
    MAX_EVENT_PER_PAGE = 100
    SCRAPER_START_DATE = "2019-10-06"
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
        json.dump(data, f)
