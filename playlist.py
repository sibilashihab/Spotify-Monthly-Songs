# Make sure your logged in
        #changing plan since since spotify api doesn't allow you to access playlists owned by spotify and added restrictions lol
# Open liked songs
# Loop through songs and and add it to list with id and added date
# Separate it based on month and year added 
# create a new playlist
# add to new playlist based on each month

import json
import requests
from datetime import datetime
from secret import spotify_token, spotify_user_id, discover_temp_id

class save:
    def __init__(self):
        self.spotify_user_id = spotify_user_id
        self.spotify_token = spotify_token
        self.discover_temp_id = discover_temp_id

    def findSongs(self):
        #loop through first 50 liked songs

        query = "https://api.spotify.com/v1/me/tracks?limit=50"
        
        response = requests.get(query, 
                                headers = {"Content-Type": "application/json", 
                                           "Authorization": "Bearer {}".format(self.spotify_token)})
        
        data = response.json()["items"]
        tracks =[]
        for i in data:
            trackdata= {
                "date": datetime.strptime(i["added_at"][:7], "%Y-%m").strftime("%B %Y"), #slice only year and month and convert month to string
                "uri":  i["track"]["uri"], #track uri
                "song": i["track"]["name"] #song name
            }
            tracks.append(trackdata)

        return tracks
    
    def createPlaylist(self, tracks):
        #Check if playlist exists already if not add songs
        query = "https://api.spotify.com/v1/users/{}/playlists".format(self.spotify_user_id)

        response = requests.get(query, 
                                headers = {"Authorization": "Bearer {}".format(self.spotify_token)})
        
        playlists = response.json()["items"]
        
        current_month = datetime.strptime(datetime.now().strftime("%Y-%m"), "%Y-%m").strftime("%B %Y") #converting to right format

        for i in playlists:
            if i["name"] == current_month:
                print("Playlist Already exists")
                return     
            
        newurl = "https://api.spotify.com/v1/users/{}/playlists".format(self.spotify_user_id)

        payload = {
        "name": current_month,
        "description": "{} monthly playlist".format(current_month),
        "public": False
        }    

        create_response = requests.post(newurl, headers={
        "Authorization": "Bearer {}".format(self.spotify_token),
        "Content-Type": "application/json"
        }, json=payload)

        if create_response.status_code == 201:
            print(f"Playlist created for {current_month}")
        else:
            print("Failed to create playlist:", create_response.json())

a = save()
likedsongs = a.findSongs()
a.createPlaylist(likedsongs)