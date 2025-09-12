import requests
import json
from secret import refresh_token, base_64

class Refresh:
    def __init__(self):
        self.refresh_token = refresh_token
        self.base_64 = base_64

    def refresh(self):

        query = "https://accounts.spotify.com/api/token"

        response = requests.post(query,
                                data={"grant_type":"refresh_token", 
                                       "refresh_token": self.refresh_token                         
                                       },
                                headers={"Content-Type":"application/x-www-form-urlencoded", "Authorization": "Basic " + self.base_64})
        
        try:
            responsejson = response.json()
        except json.JSONDecodeError:
            print("Failed JSON decoding:", response.text)
            return None

        if response.status_code != 200:
            print("Failed to refresh token. Status code:", response.status_code)
            print("Response:", json.dumps(responsejson))
            return None

        print("Successful token refresh")
        return responsejson["access_token"]

a = Refresh
