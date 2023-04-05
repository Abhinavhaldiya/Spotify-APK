import spotipy
from dotenv import load_dotenv
import os
import requests
import pprint

load_dotenv()

client_id=os.getenv("CLIENT_ID")
client_secret=os.getenv("CLIENT_SECRET")

sp = spotipy.Spotify(
    auth_manager=spotipy.oauth2.SpotifyOAuth(
        scope="user-library-read",
        redirect_uri="http://localhost:8888/callback",
        client_id=client_id,
        client_secret=client_secret,
        show_dialog=True,
        cache_path="token.txt"
    )
)
track_id=sp.search(q='Lovely',limit=1,type='track')['tracks']['items'][0]['id']

user_id = sp.current_user()["id"]
results=sp.current_user_saved_tracks()
# print(results)
for idx,item in enumerate(results['items']):
    track=item['track']
    print(f"{idx+1}. {track['artists'][0]['name']}")


# songs=sp.artist_top_tracks(artist_id=, country='India')
# artist_id("Billie Ellish")