# How to import localist data:

### Scraping and saving data to file
First, use the localist_fetch.py script to download the data into a json format.
Change the parameters within the script (may be changed to CLI args later) to determine the range of dates to scrape.
The script will save the json in its folder as event-{start_date}-{end_date}.json.

### Adding tags
Then, you want to manually add tags to each event.
Within the json structure, each tags will have an empty list called tags.
Populate these - for example, tags = ["Free-Food", "Other", "A&S"]
Tags themselves can be added by running "py .\events_backend\manage.py add_tags" from root.

To automatically add tags, run the inject_tags.py script.

### Google Maps place_id
(Optional) You can run the inject_placeid.py script to insert appropriate place_id values in json.
Make sure to set up the right arguments in the script, especially the Google Maps API key.

### Adding to database
Finally, you want to import the json into the database.
To do this, run "py .\events_backend\manage.py localist_parser [path-to-json]".
If you have a csv (from facebook instead of localist), run "py .\events_backend\manage.py csv_event_parser [path-to-csv]" instead.

## Removing duplicate events

### Django Command

Scraping will result in many separate event entries sharing the same names but occuring at different times.
We want to remove most of these duplicate events, given that they are not whitelisted for this kind of duplication (like movie events)
Run "py .\events_backend\manage.py remove_duplicate_events" to do this.

### Standalone Script

To remove duplicates from a json, use filter_duplicates.py.