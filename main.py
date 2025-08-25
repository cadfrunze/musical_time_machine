from typing import Any
import requests as rq
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
load_dotenv()

id_client, secret_client, url, port = os.getenv("ID_CLIENT"), os.getenv("CLIENT_SECRET"), os.getenv("URL"), os.getenv("PORT")

sp: spotipy.Spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=id_client,
    client_secret=secret_client,
    redirect_uri=f"{url}:{port}",
    scope="playlist-modify-public"
))


user_cmd: str = input("YYYY-MM-DD : ")
user_data: str = user_cmd.split()[0]
url_adress: str = f"https://www.billboard.com/charts/hot-100/{user_data}/"
header: dict[str, str] = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0"
    }

web_data: rq.Response = rq.get(url=url_adress, headers=header)
engine: BeautifulSoup = BeautifulSoup(markup=web_data.text, features="html.parser")
music_items: list[str] = [item.get_text().strip() for item in engine.select("li ul li h3", id="title-of-a-story")] 

# with open("top_music.txt", "w") as fisier:
#     for item in music_items:
#         fisier.write(f"{item}\n")

user_id = sp.current_user()['id']
playlist = sp.user_playlist_create(user=user_id, name=f"{user_data}")
playlist_id = playlist['id']
tracks_list: list[Any] = []

for titlu in music_items:
    res = sp.search(q=titlu, type="track", limit=1)
    track = res['tracks']['items']
    if track:
        tracks_list.append(track[0]['uri'])

sp.playlist_add_items(playlist_id=playlist_id, items=tracks_list)