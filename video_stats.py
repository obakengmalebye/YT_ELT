import json
import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
CHANNEL_HANDLE = "MrBeast"
MAX_RESULTS = 50


def get_playlist_id():
    try:
        url = "https://youtube.googleapis.com/youtube/v3/channels"

        params = {
            "part": "contentDetails",
            "forHandle": CHANNEL_HANDLE,
            "key": API_KEY,
        }

        response = requests.get(url, params=params)
        response.raise_for_status()

        data = response.json()

        channel_items = data["items"][0]
        playlist_id = channel_items["contentDetails"]["relatedPlaylists"]["uploads"]

        return playlist_id

    except requests.exceptions.RequestException as e:
        raise e


def get_video_ids(playlist_id):
    video_ids = []
    page_token = None

    while True:
        url = "https://youtube.googleapis.com/youtube/v3/playlistItems"

        params = {
            "part": "contentDetails",
            "playlistId": playlist_id,
            "maxResults": MAX_RESULTS,
            "key": API_KEY,
        }

        if page_token:
            params["pageToken"] = page_token

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()

            data = response.json()

            for item in data["items"]:
                video_ids.append(item["contentDetails"]["videoId"])

            page_token = data.get("nextPageToken")

            if not page_token:
                break

        except requests.exceptions.RequestException as e:
            raise e

    return video_ids


if __name__ == "__main__":
    playlist_id = get_playlist_id()
    #print("Playlist ID:", playlist_id)

    video_ids = get_video_ids(playlist_id)
    #print("Total Videos:", len(video_ids))
    #print(video_ids[:10])