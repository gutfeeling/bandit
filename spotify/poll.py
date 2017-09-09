import sys
import os
import re
import time
#import urllib2
from io import BytesIO

from spotipy import Spotify
import spotipy.util as util
import requests
import matplotlib.pyplot as plt

class MySpotify(Spotify):

    def currently_playing_track(self):
        return self._get("me/player/currently-playing")

scope = 'user-read-currently-playing'
username = os.environ['SPOTIFY_USER_ID']

token = util.prompt_for_user_token(username, scope)

last_id = None

first_image = True
plt.ion()
plt.axis("off")
plt.show()

if token:
    while True:
        time.sleep(5)
        sp = MySpotify(auth=token)
        result = sp.currently_playing_track()
        is_playing = result["is_playing"]
        if not is_playing:
            continue
        track_id = result["item"]["id"]
        if track_id != last_id:
            artist_href = result["item"]["artists"][0]["href"]
            pattern = re.compile("artists/(.+)")
            match = re.search(pattern, artist_href)
            artist_code = match.group(1)
            artist_result = sp.artist(artist_code)
            image_url = artist_result["images"][0]["url"]
            print(image_url)
            last_id = track_id

            # display image in matplotlib
            response = requests.get(image_url)
            f = BytesIO(response.content)
            im = plt.imread(f, format = "jpeg")
            if first_image:
                imshow_object = plt.imshow(im)
            else:
                imshow_object.set_data(im)
            plt.pause(0.001)
            plt.draw()
else:
    print "Can't get token for", username
