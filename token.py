#Script to get access token using authorization code flow

import requests
import base64

#Add your credentials here from spotify developer dashboard
CLIENT_ID = ""
CLIENT_SECRET = ""
REDIRECT_URI = "" #you can add any redirect uri preferably your https://spotify.com/
CODE = "" #authorization code obtained after user login

auth_header = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
headers = {"Authorization": f"Basic {auth_header}"}
data = {
    "grant_type": "authorization_code",
    "code": CODE,
    "redirect_uri": REDIRECT_URI
}

response = requests.post("https://accounts.spotify.com/api/token", headers=headers, data=data)
print(response.json())
