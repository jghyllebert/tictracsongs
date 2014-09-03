from unittest import TestCase
from algorithm import UserFeed


class AlgorithmTest(TestCase):
    def setUp(self):
        self.userfeed = UserFeed('jghyllebert')
        #override the dataset with known values
        self.userfeed.data = [
            #13 tracks listened to on tuesday
            {"track": "Pony", "total_pages": None, "start_from_page": None, "timestamp_played": "1409700869",
             "artist": "Deluxe"},
            {"track": "Bom Bom", "total_pages": None, "start_from_page": None, "timestamp_played": "1409700694",
             "artist": "Sam and the Womp"},
            {"track": "puttin' on the ritz - club des belugas remix", "total_pages": None, "start_from_page": None,
             "timestamp_played": "1409700447", "artist": "Fred Astaire"},
            {"track": "Crazy in Love - Radio Edit", "total_pages": None, "start_from_page": None,
             "timestamp_played": "1409700211", "artist": "Swing Republic"},
            {"track": "Lose Yourself", "start_from_page": None, "total_pages": None, "timestamp_played": "1409699983",
             "artist": "Astrazz"},
            {"track": "Lose Yourself", "start_from_page": None, "total_pages": None, "timestamp_played": "1409699983",
             "artist": "Astrazz"},
            {"track": "Lose Yourself", "start_from_page": None, "total_pages": None, "timestamp_played": "1409699983",
             "artist": "Astrazz"},
            {"track": "Dig It (Feat. Myra Taylor) - Minimatic Remix", "total_pages": None, "start_from_page": None,
             "timestamp_played": "1409699735", "artist": "His Rockets"},
            {"track": "Dig It (Feat. Myra Taylor) - Minimatic Remix", "total_pages": None, "start_from_page": None,
             "timestamp_played": "1409699735", "artist": "His Rockets"},
            {"track": "Happy Swingin - Original Mix", "total_pages": None, "start_from_page": None,
             "timestamp_played": "1409699397", "artist": "Shemian"},
            {"track": "Happy Swingin - Original Mix", "total_pages": None, "start_from_page": None,
             "timestamp_played": "1409699397", "artist": "Shemian"},
            {"track": "Happy Swingin - Original Mix", "total_pages": None, "start_from_page": None,
             "timestamp_played": "1409699397", "artist": "Shemian"},
            {"track": "Happy Swingin - Original Mix", "total_pages": None, "start_from_page": None,
             "timestamp_played": "1409699397", "artist": "Shemian"},
            #14 tracks listened to on monday
            {"track": "Pas touch\u00e9", "total_pages": None, "start_from_page": None, "timestamp_played": "1409605756",
             "artist": "Maitre Gims"},
            {"track": "Laisse tomber", "total_pages": None, "start_from_page": None, "timestamp_played": "1409605492",
             "artist": "Maitre Gims"},
            {"track": "CLOSE YOUR EYES", "total_pages": None, "start_from_page": None, "timestamp_played": "1409605332",
             "artist": "Maitre Gims"},
            {"track": "bella", "total_pages": None, "start_from_page": None, "timestamp_played": "1409605105",
             "artist": "Maitre Gims"},
            {"track": "De Marseille \u00e0 Paris", "total_pages": None, "start_from_page": None,
             "timestamp_played": "1409604832", "artist": "Maitre Gims"},
            {"track": "Epuis\u00e9", "total_pages": None, "start_from_page": None, "timestamp_played": "1409604605",
             "artist": "Maitre Gims"},
            {"track": "freedom", "start_from_page": None, "total_pages": None, "timestamp_played": "1409604381",
             "artist": "Maitre Gims"},
            {"track": "Intro", "start_from_page": None, "total_pages": None, "timestamp_played": "1409604212",
             "artist": "Maitre Gims"}, {"track": "What!? - Modek Remix", "start_from_page": None, "total_pages": None,
                                        "timestamp_played": "1409603831", "artist": "VNNR"},
            {"track": "What!? (Dr Lektroluv's Milano Edit)", "start_from_page": None, "total_pages": None,
             "timestamp_played": "1409603561", "artist": "VNNR"},
            {"track": "What!? (Nickel Remix)", "start_from_page": None, "total_pages": None,
             "timestamp_played": "1409603227", "artist": "VNNR"},
            {"track": "What!?", "start_from_page": None, "total_pages": None, "timestamp_played": "1409602995",
             "artist": "VNNR"},
            {"track": "What!?", "start_from_page": None, "total_pages": None, "timestamp_played": "1409602995",
             "artist": "VNNR"},
            {"track": "What!?", "start_from_page": None, "total_pages": None, "timestamp_played": "1409602995",
             "artist": "VNNR"}
        ]

    def test_create_or_get_file(self):
        """
        Function should return a list with the values of the file
        """
        self.assertTrue(isinstance(self.userfeed.get_file(), list))

    def test_calculate_favourite_artists(self):
        self.assertEqual(self.userfeed.favourite_artists(5), [['Maitre Gims', 8], ['VNNR', 6], ['Shemian', 4],['Astrazz', 3], ['His Rockets', 2]])

    def test_calculate_track_listens_per_day(self):
        self.assertEqual(self.userfeed.track_listens_per_day(), 13)

    def test_calculate_most_active_day(self):
        self.assertEqual(self.userfeed.most_active_day(), 'Monday')