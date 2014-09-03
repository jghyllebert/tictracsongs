tictracsongs
============

Installation
------------

Create a folder on your computer. If you haven't, open up Terminal and browse to your folder.

Set up a a virtual environment using

    virtualenv .

In case you don't have virtualenv installed, run ``sudo pip install virtualenv``.
Activate virtualenv with the command ``source bin/activate``

Clone this repository using ``git clone https://github.com/jghyllebert/tictracsongs.git``

Install the requirements:

    pip install -r tictracsongs/requirements.txt

Provide an last.fm API key in ``settings.py``

Run the script ``python activity.py lastfm_username``

Dependencies
------------
* requests (2.4.0) - http://docs.python-requests.org/en/latest/
* colorama (0.3.1) - https://pypi.python.org/pypi/colorama