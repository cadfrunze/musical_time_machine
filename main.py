import requests as rq
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
load_dotenv()

id_client, secret_client, url = os.getenv("ID_CLIENT"), os.getenv("CLIENT_SECRET"), os.getenv("URL")



user_cmd: str = input("YYYY-MM-DD : ")
user_data: str = user_cmd.split()[0]
url_adress: str = f"https://www.billboard.com/charts/hot-100/{user_data}/"
header: dict[str, str] = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0"
    }

web_data: rq.Response = rq.get(url=url_adress, headers=header)
engine: BeautifulSoup = BeautifulSoup(markup=web_data.text, features="html.parser")
music_items: list[str] = [item.get_text().strip() for item in engine.select("li ul li h3", id="title-of-a-story")] 

with open("top_songs", "w") as fisier:
    for item in music_items:
        fisier.write(f"{item}\n")