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
from PIL import Image
import numpy as np
from unipath import Path
from colorthief import ColorThief

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
image_file_path = None

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
            if image_file_path:
                os.remove(image_file_path)
            artist_href = result["item"]["artists"][0]["href"]
            pattern = re.compile("artists/(.+)")
            match = re.search(pattern, artist_href)
            artist_code = match.group(1)
            artist_result = sp.artist(artist_code)
            #image_url = artist_result["images"][0]["url"]
            image_url = result["item"]["album"]["images"][0]["url"]
            #print(image_url)
            last_id = track_id

            # download image
            response = requests.get(image_url)
            bytestream = BytesIO(response.content)

            # resize image using pillow
            pil_image = Image.open(bytestream)
            pil_image.thumbnail([480, 480])
            cropped_pil_image = pil_image.crop((0, 80, 480, 400))
            cropped_pil_image.load()

            # convert to a numpy array

            pil_image_numpy_array = np.array(cropped_pil_image)

            # save to temporary file
            image_file_path = Path(__file__).ancestor(1).child(
                "{0}.jpeg".format(artist_code)
                )
            cropped_pil_image.save(image_file_path)

            # get dominant colors
            color_thief = ColorThief(image_file_path)
            dominant_color = color_thief.get_color(quality=1)
            #print(dominant_color)

            # display image in matplotlib
            #im = plt.imread(pil_image_numpy_array)
            if first_image:
                imshow_object = plt.imshow(pil_image_numpy_array)
            else:
                imshow_object.set_data(pil_image_numpy_array)
            plt.pause(0.001)
            plt.draw()

            # fullscreen image
            command = ["sudo", "fbi", "-T", "2", "-d", "/dev/fbi", "noverbose",
                "-a", image_file_path
                ]
else:
    print "Can't get token for", username
