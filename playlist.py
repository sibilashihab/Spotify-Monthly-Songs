# Make sure your logged in
# Create a new playlist or open playlist if it already exists
# Open discover weekly playlist
# Copy discover weekly songs
# Paste into new playlist

import json
import requests
from secret import spotify_token, spotify_user_id, discover_id

class save:
    def __init__(self):
        self.spotify_user_id = spotify_user_id
        self.spotify_token = spotify_token
        self.discover_id = discover_id

    def find_songs(self):
        #loop through playlist and add songs to a list
        query = "https://api.spotify.com/v1/playlists/{}".format(discover_id)
        
        response = requests.get(query, 
                                headers = {"Content-Type": "application/json", 
                                           "Authorization": "Bearer {}".format(spotify_token)})
        
        response_json = response.json()
        print(response)

a = save()
a.find_songs()