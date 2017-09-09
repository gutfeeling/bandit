import sys
import os
import re

from spotipy import Spotify
import spotipy.util as util
import requests

class MySpotify(Spotify):

    def currently_playing_track(self):
        return self._get("me/player/currently-playing")

scope = 'user-read-currently-playing'
username = os.environ['SPOTIFY_USER_ID']

token = util.prompt_for_user_token(username, scope)

if token:
    sp = MySpotify(auth=token)
    result = sp.currently_playing_track()
    artist_href = result["item"]["artists"][0]["href"]
    pattern = re.compile("artists/(.+)")
    match = re.search(pattern, artist_href)
    artist_code = match.group(1)
    artist_result = sp.artist(artist_code)
    image_url = artist_result["images"][0]
    print(image_url)
else:
    print "Can't get token for", username
