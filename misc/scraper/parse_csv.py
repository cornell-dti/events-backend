import csv
import os

DEFAULT_PASSWORD = 'pbkdf2_sha256$120000$qFamKdatf0if$+aI5iQne/Z+zGJU9EfWcoaaBRUCie/8Rltkz7XRH3fQ='
EVENTS_FILE_NAME = 'fb_event (4).csv'

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

if __name__ == '__main__':
    with open(EVENTS_FILE_NAME, encoding="utf8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            web_scraper_order = row[0]
            web_scraper_start_url = row[1]
            date = row[2]
            event = row[3]
            location_and_time = row[4]
            url = row[5]
            url_href = row[6]
            location = row[7]
            time = row[8]
            attendance = row[9]
            img_src = row[10]
            description = row[11]
            host = row[12]
            tags = ''
            # Tags may be empty cells
            if len(row) >= 14:
                tags = row[13]
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                """HOW TO MANUALLY ADD AN EVENT
                0. Manually go through the host column and modify the hosts so that it's only one org
                For example, it would be "Hosted by _____" instead of "Hosted dby _____ and _______"
                This is because we want one organization per Host column, and some org names have an "and" in it so
                we can't just separate them by "and".
                1. Manually add tags from the pre-defined set (by id)
                2. Add an entry for each org into backend_main_user
                3. Add an entry into backend_main_org for the org
                4. Add an entry into backend_main_media
                5. Add an entry into backend_main_event_media
                """
                print(row)
                line_count += 1
        print(f'Processed {line_count} lines.')