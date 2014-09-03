from __future__ import print_function
from operator import itemgetter
from settings import API_ROOT_URL, API_KEY, MAXIMUM_API_CALLS

import json
import requests
import datetime


class FeedException(Exception):
    pass


class NoNewTracksException(Exception):
    pass


class UserFeed():

    api_root_url = API_ROOT_URL
    api_key = API_KEY

    def __init__(self, username):
        """
        Set up class and initiate api calls
        """
        self.username = username
        self.filename = "data/%s.txt" % username
        self.api_requests_left = MAXIMUM_API_CALLS
        self.get_feed()
        self.data = self.get_file()

    def get_file(self):
        """
        Get the file the program already created another time or create a new file for this user.
        Returns the data from this file.
        """
        with open(self.filename, 'a+') as f:
            data = []
            try:
                data = json.load(f)
            except ValueError:
                pass
        return data

    def write_to_file(self, data):
        """
        Truncate the file and write the new data
        """
        #Sort list by timestamp_played
        sorted_data = sorted(data, key=itemgetter('timestamp_played'), reverse=True)
        with open(self.filename, 'w+') as f:
            json.dump(sorted_data, f)

    def parse_feed(self, feed, remember_page):
        """
        Handle the data received from the last.fm api
        """
        existing_data = self.get_file()
        data = json.loads(feed)

        try:
            tracks = data['recenttracks']
        except KeyError:
            raise FeedException(data['message'])

        try:
            tracks['track']
        except KeyError:
            raise NoNewTracksException()

        for index, element in enumerate(tracks['track']):
            try:
                #skip if the track is playing now, the user could skip it
                element['date']['uts']
            except KeyError:
                continue

            pages_left = int(tracks['@attr']['totalPages']) - int(tracks['@attr']['page'])
            data_to_store = {
                'track': element['name'],
                'artist': element['artist']['#text'],
                'timestamp_played': element['date']['uts'],
                'start_from_page': None,
                'total_pages': None
            }

            if remember_page and index == 0 and pages_left > self.api_requests_left:
                #There are too many pages to request in the remaining amount of API calls
                data_to_store['start_from_page'] = int(tracks['@attr']['page']) + self.api_requests_left + 1,
                data_to_store['total_pages'] = int(tracks['@attr']['totalPages'])

            existing_data.append(data_to_store)

        self.write_to_file(existing_data)
        return tracks['@attr']['page'], tracks['@attr']['totalPages'],

    def update_file(self, line):
        """
        Update the line if we process leftover pages
        """
        data_in_file = self.get_file()

        position = [i for i, x in enumerate(data_in_file) if x == line][0]
        data_in_file.pop(position)

        #Calculate the new number of pages
        pages_left = line['total_pages'] - line['start_from_page']
        if pages_left > self.api_requests_left:
            line['start_from_page'] += self.api_requests_left
        else:
            line['start_from_page'] = None

        data_in_file.append(line)
        self.write_to_file(data_in_file)

    def get_feed(self, historic=None):
        """
        Decide which type of API calls we need to perform.
        """
        data = self.get_file()

        if len(data) == 0:
            self.make_api_url()
        else:
            if historic:
                #look for dictionaries with the key start_from_page
                sorted_data = sorted(data, key=itemgetter('start_from_page', 'timestamp_played'), reverse=True)

                if sorted_data[0]['start_from_page']:
                    self.update_file(sorted_data[0])
                    #Fetch the tracks that weren't saved in previous calls due to limitations
                    self.make_api_url(from_timestamp=sorted_data[0]['timestamp_played'],
                                      page=sorted_data[0]['start_from_page'])
                else:
                    #Start fetching oldest tracks
                    latest_entry = sorted_data[-1]
                    self.make_api_url(to_timestamp=latest_entry["timestamp_played"])
            else:
                #Look for new tracks first
                line = data[0]
                self.make_api_url(from_timestamp=line["timestamp_played"])

    def make_api_url(self, from_timestamp=None, to_timestamp=None, page=None):
        """
        Create the urls to make a request to the last.fm API
        """
        data_dictionary = {
            'method': 'user.getrecenttracks',
            'user': self.username,
            'api_key': self.api_key,
            'format': 'json',
        }
        if from_timestamp:
            data_dictionary['from'] = from_timestamp

        if to_timestamp:
            data_dictionary['to'] = to_timestamp

        if page:
            data_dictionary['page'] = page

        r = requests.get(self.api_root_url, params=data_dictionary)
        self.api_requests_left -= 1

        try:
            #Process the incoming data
            page, total_pages = self.parse_feed(r.text, from_timestamp)

            if page != total_pages and self.api_requests_left != 0:
                #We have multiple pages to take care of
                #Determine the maximum of pages we can process
                max_page = int(page) + self.api_requests_left

                #Check if we can process more pages then needed
                if max_page > int(total_pages):
                    max_page = int(total_pages)

                for current_page in range(int(page), max_page):
                    data_dictionary['page'] = current_page + 1
                    r = requests.get(self.api_root_url, params=data_dictionary)
                    self.api_requests_left -= 1
                    self.parse_feed(r.text, None)
        except NoNewTracksException:
            if from_timestamp:  # All historic tracks are fetched, stop business
                return True

        #If we have more api requests left, we should look for historic tracks
        if self.api_requests_left > 0:
            self.get_feed(historic=True)

    def favourite_artists(self, amount):
        """
        Determine the artists that were the most listened to
        The length is determined by the amount given
        """
        all_artists = [
            #[artist, count]
        ]

        for track in self.data:
            try:
                place_in_list = [x[0] for x in all_artists].index(track['artist'])
                all_artists[place_in_list][1] += 1
            except ValueError:
                all_artists.append([track['artist'], 1])
        top_artists = sorted(all_artists, key=itemgetter(1), reverse=True)

        return top_artists[:amount]

    def track_listens_per_day(self):
        """
        Determine the average amount of tracks listened to.
        Exclude days with 0
        """
        total_tracks = len(self.data)
        total_days = 0
        current_day = None

        for track in self.data:
            date_played = datetime.datetime.utcfromtimestamp(int(track['timestamp_played'])).strftime('%Y-%m-%d')
            if date_played != current_day:
                total_days += 1
                current_day = date_played

        return total_tracks / total_days

    def most_active_day(self):
        """
        Determine the day which has the most listened tracks.
        """
        weekdays = [
            ['Monday', 0],
            ['Tuesday', 0],
            ['Wednesday', 0],
            ['Thursday', 0],
            ['Friday', 0],
            ['Saturday', 0],
            ['Sunday', 0]
        ]

        for track in self.data:
            weekday = datetime.datetime.utcfromtimestamp(int(track['timestamp_played'])).weekday()
            weekdays[weekday][1] += 1

        top_days = sorted(weekdays, key=itemgetter(1), reverse=True)
        return top_days[0][0]
