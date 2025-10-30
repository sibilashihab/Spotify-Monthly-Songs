import json
import os
import requests
from datetime import datetime
from refresh import Refresh

class save:
    def __init__(self):
        self.spotify_user_id = os.environ.get("SPOTIFY_USER_ID")
        self.spotify_token = ""

    def findSongs(self):

        def fetchTracks(url):
            response = requests.get(url,
                                headers = {"Content-Type": "application/json",
                                           "Authorization": "Bearer {}".format(self.spotify_token)})

            if response.status_code != 200:
                print("Failed to fetch tracks", response.json())
                return []

            data = response.json()["items"]
            tracks =[]
            seen_uris = set()  # track uris already added
            for i in data:
                track_info = i["track"] if "track" in i else i
                track_uri = track_info["uri"]

                if track_uri in seen_uris:
                        continue  # skip duplicates within the same api call
                seen_uris.add(track_uri)

                trackdata= {
                    "date": datetime.strptime(i["added_at"][:7], "%Y-%m").strftime("%B %Y") if i.get("added_at") else datetime.now().strftime("%B %Y"), #slice only year and month and convert month to string
                    "uri": track_uri, #track uri
                    "song": track_info["name"] #song name
                }
                tracks.append(trackdata)
            return tracks

        liked_url = "https://api.spotify.com/v1/me/tracks?limit=50" #loop through first 50 liked songs
        top_url = "https://api.spotify.com/v1/me/top/tracks?time_range=short_term&limit=5" #find users top songs in the past month

        liked_tracks = fetchTracks(liked_url)
        top_tracks = fetchTracks(top_url)


        all_tracks = []
        seen = set()
        for track in liked_tracks + top_tracks:
            if track["uri"] not in seen: #avoid duplicates between liked and top tracks
                seen.add(track["uri"])
                all_tracks.append(track)

        return all_tracks


    def createPlaylist(self):
        #Check if playlist exists already if not add songs
        query = "https://api.spotify.com/v1/users/{}/playlists".format(self.spotify_user_id)

        response = requests.get(query,
                                headers = {"Authorization": "Bearer {}".format(self.spotify_token)})

        if response.status_code != 200:
            print("Failed to check user playlists", response.json())
            return

        playlists = response.json()["items"]

        current_month = datetime.strptime(datetime.now().strftime("%Y-%m"), "%Y-%m").strftime("%B %Y") #converting to right format

        for i in playlists:
            if i["name"] == current_month:
                print("Playlist Already exists")
                return i["id"], current_month

        newurl = "https://api.spotify.com/v1/users/{}/playlists".format(self.spotify_user_id)

        payload = {
        "name": current_month,
        "description": "{} monthly playlist".format(current_month),
        "public": False,
        "collaborative": False ############ playlist is being publicly created for some reason
        }

        create_response = requests.post(newurl, headers={
        "Authorization": "Bearer {}".format(self.spotify_token),
        "Content-Type": "application/json"
        }, json=payload)

        if create_response.status_code == 201:
            print("Playlist created for {}".format(current_month))
            playlist_id = create_response.json()["id"] #getting playlist id to add songs into it
            return playlist_id, current_month
        else:
            print("Failed to create playlist:", create_response.json())
            return None

    def addSongs(self, newplaylistid, likedsongs, currentmonth):
        #adding songs to the created playlist
        #get playlist first

        newsongs = "https://api.spotify.com/v1/playlists/{}/tracks".format(newplaylistid)

        response = requests.get(newsongs,
                                headers = {"Authorization": "Bearer {}".format(self.spotify_token)})

        if response.status_code != 200:
            print("Failed to get playlist", response.json())
            return

        songs = response.json()["items"]
        existingsongs=[]
        for i in songs:
            existingsongs.append(i["track"]["uri"]) #getting songs already in the playlist to avoid duplicates

        if response.status_code != 200:
            print("Failed to get playlist", response.json())
            return

        uris = [] #list to store all songs of the month
        for song in likedsongs:
            if song["date"] == currentmonth and song["uri"] not in existingsongs:
                uris.append(song["uri"]) #getting uris from dictionary of liked tracks if it was added this month

        if not uris:
            print("No songs to add for this month.")
            return

        payload = {"uris": uris}

        create_response = requests.post(newsongs, headers={
                "Authorization": "Bearer {}".format(self.spotify_token),
                "Content-Type": "application/json"
                }, json=payload)

        if create_response.status_code != 201:
            print("Failed to add tracks to playlist", create_response.json())
            return

        else:
            print("Tracks added!")

    def callRefresh(self):
        print("Refreshing token")
        refresh_caller = Refresh()
        token = refresh_caller.refresh()

        if not token:
            print("Failed to refresh token. Exiting program.")
            exit(1)  # exit if token is invalid
        else:
            self.spotify_token = token

def main():
    a = save()
    a.callRefresh()
    likedsongs = a.findSongs()
    newplaylistid, currentmonth = a.createPlaylist()
    if newplaylistid:
        a.addSongs(newplaylistid, likedsongs, currentmonth)
    else:
        print("Cannot create or get playlist. Skipping song addition.")

if __name__ == "__main__":
    main()
