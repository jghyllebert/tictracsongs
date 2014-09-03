import sys

from colorama import Fore, init as colorama_init
from settings import API_KEY, API_ROOT_URL, MAXIMUM_API_CALLS
from algorithm import UserFeed, FeedException


colorama_init()


class SetUpException(Exception):
    pass


def get_feed(username):

    u = UserFeed(username)
    try:
        message = ""
        message += 'You have listened to a total of %d tracks.\n' % len(u.data)
        message += 'Your top 5 favorite artists: %s.\n' % ', '.join(str(i[0]) for i in u.favourite_artists(5))
        message += 'You listen to an average of %d tracks a day.\n' % u.track_listens_per_day()
        message += 'Your most active day is %s.' % u.most_active_day()
        print(Fore.GREEN + message)
    except FeedException as e:
        print(Fore.RED + 'Error: %s' % e)


def main():
    try:
        if API_KEY == "":
            raise SetUpException('Error: Please provide a last.fm API key.')
        if API_ROOT_URL == "":
            raise SetUpException('Error: Please provide the root url for the last.fm API.\n(Normally: http://ws.audioscrobbler.com/2.0)')
        if not isinstance(MAXIMUM_API_CALLS, int):
            raise SetUpException('Error: Please enter a number for the maximum API calls.')

        get_feed(sys.argv[1])
    except IndexError:
        print(Fore.RED + 'Error: Please provide an username.')
    except SetUpException as e:
        print(Fore.RED + '%s' % e)


if __name__ == "__main__":
    main()