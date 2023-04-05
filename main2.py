import spotipy
from dotenv import load_dotenv
import os
import requests
import json

load_dotenv()

client_id=os.getenv("CLIENT_ID")
client_secret=os.getenv("CLIENT_SECRET")
SCOPE="playlist-modify-public"
sp = spotipy.Spotify(
    auth_manager=spotipy.oauth2.SpotifyOAuth(
        scope=SCOPE,
        redirect_uri="http://localhost:8888/callback",
        client_id=client_id,
        client_secret=client_secret,
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]

#Creating a new playlist
# sp.user_playlist_create(user=user_id,name='Top BillBoard Songs' ,public=True,description='Playlist having top BillBoard songs')

#Adding a song to Playlist
result=sp.search(q='Lovely',limit=1,type='track')
# print(json.dumps(result,sort_keys=4,indent=4))
track_uri=result['tracks']['items'][0]['uri']
print(track_uri)

tracks=[track_uri]
preplaylist=sp.user_playlists(user=user_id)
# print(json.dumps(playlist,sort_keys=4,indent=4))

playlist=preplaylist['items'][0]['id']
print(playlist)

sp.user_playlist_add_tracks(user_id,playlist_id=playlist,tracks=tracks)
