"""
Django command to help scrape API for tracks data
"""
import json
import time
from datetime import datetime

from django.core.management.base import BaseCommand
import requests
from requests_oauthlib import OAuth1

from beats.settings.env import (
    OAUTH_CONSUMER_KEY, OAUTH_CONSUMER_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET
)


class Command(BaseCommand):
    """
    Scrapes tracks off an API from Beatports with argument number of pages
    E.g. `python manage.py scrape tracks 3` to get 3 pages of tracks data
    """
    help = 'Scrapes tracks off an API'

    def add_arguments(self, parser):
        parser.add_argument("pages", type=int)

    def handle(self, *args, **options):
        print("Scrape Tracks Command Called")
        scraped_results_file = 'scraped_tracks.json'  # where to store json data
        pages_argument = options.get("pages", 1)  # Default 1 page
        utc_epoch = int(datetime.utcnow().timestamp())
        print("Started Scraping at time: ", utc_epoch)

        auth = OAuth1(
            OAUTH_CONSUMER_KEY, OAUTH_CONSUMER_SECRET,
            OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
        tracks_url = 'https://oauth-api.beatport.com/catalog/3/tracks?page='

        # Go through API pages and store results to json file
        with open(scraped_results_file, 'w') as outfile:
            for page in range(1, pages_argument+1):
                tracks_url_page = tracks_url + str(page)
                response = requests.get(tracks_url_page, auth=auth)
                json_data = json.loads(response.text)
                json.dump(json_data, outfile)
                time.sleep(5)  # don't slam server w/ requests
        print("Completed scraping tracks, results are in: " + scraped_results_file)
        