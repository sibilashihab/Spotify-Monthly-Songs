# Spotify Monthly Songs

A tool that automatically collects your **liked songs from the past month** and adds them into a new Spotify playlist.  
If the playlist for the month already exists, it simply updates it with any new liked songs — all powered by **Python** and **GitHub Actions**.

---

## Features

- Automatically runs on the **last day of every month**
- Gathers your **liked songs** from the current month
- Creates a new monthly playlist (e.g. “Liked Songs — October 2025”)
- If the playlist already exists, it adds new songs instead of duplicating
- Fully automated via **GitHub Actions + Spotify API**

---

## Requirements

- Python 3.10+
- A Spotify Developer Account  
- The following GitHub **secrets** configured in your repository:
  - `SPOTIFY_REFRESH_TOKEN` — Token used to re-authenticate your Spotify account automatically
  - `SPOTIFY_BASE64` — Your Spotify API client credentials encoded in Base64 format
  - `SPOTIFY_USER_ID` — Your Spotify user ID

---

## Setup

### 1. Clone this repository
```bash
git clone https://github.com/sibilashihab/spotify-monthly-songs.git
cd spotify-monthly-songs
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### Setting Up GitHub Secrets

Go to:  **GitHub repo → Settings → Secrets and variables → Actions → New repository secret**
You’ll add the three secrets described below.

**1. `SPOTIFY_BASE64`**
Your Spotify Client ID and Client Secret combined and Base64 encoded. Spotify requires this to authenticate your app.

  How to get it:      
  - Go to the **Spotify Developer Dashboard**
  - Log in and click **Create App (or open an existing one)**.

Copy your:<br>
`Client ID`<br>
`Client Secret`

Combine them into one string:<br>
`client_id:client_secret`


Encode that string to Base64 using one of these methods:

 **Python:**
  ```bash
  python3 -c "import base64; print(base64.b64encode(b'YOUR_CLIENT_ID:YOUR_CLIENT_SECRET').decode())"
  ```

  **macOS/Linux Terminal:**
  ```bash
  echo -n "YOUR_CLIENT_ID:YOUR_CLIENT_SECRET" | base64
  ```

Copy the result and add it as a secret in GitHub:

`Name`: SPOTIFY_BASE64<br>
`Value`: \<your encoded string>

**2. `SPOTIFY_USER_ID`**


Your unique Spotify user ID — this tells the API which account to create playlists for.

How to get it:

- Visit your Spotify profile page:
**_https://open.spotify.com/user/yourusername_**

The part after /user/ is your ID.

Or use the Spotify Web API Console:
- Click “Get Token”
- Authorize your account
- Copy the "id" field from the JSON response.

Example:
```json
{
  "display_name": "Your Name",
  "id": "clientid"
}
```

Add this to GitHub:

`Name`: SPOTIFY_USER_ID<br>
`Value`: \<id>

**3. `SPOTIFY_REFRESH_TOKEN`**

A long-lived token that lets your script get new access tokens without logging in again.
You only need to generate this once.

## Workflow Overview

The GitHub Action runs automatically at 18:00 GST (14:00 UTC) on the last day of the month.

It:

- Checks if today is the last day of the month
- If true, runs `playlist.py`
- Creates or updates your monthly playlist with your liked songs

**Workflow file:**  
`.github/workflows/runplaylist.yml`

---

## How It Works

- The action runs a Python script (`playlist.py`) on schedule.
- It authenticates with Spotify using your refresh token.
- It finds or creates a playlist named after the current month.
- It fetches all your liked songs from that month and adds them.
- If the playlist already exists, only new songs are added.

---

## Example GitHub Action

This line controls when the action runs.  
The format is:  
`minute hour day_of_month month day_of_week` (UTC, 24-hour time)

```yaml
on:
  schedule:
    - cron: '59 19 * * *'  # Run daily at 23:59 GST (19:59 UTC)
```

The script ensures it only executes on the last day of each month.

## Author

Sibila Shihab
