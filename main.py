import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import spotipy
import os

load_dotenv()

Client_ID =os.getenv('Client_ID')
Client_Secret =os.getenv('Client_Secret')
SCOPE='playlist-modify-public'

spotify_object=spotipy.Spotify(
        auth_manager=spotipy.oauth2.SpotifyOAuth(
        scope=SCOPE,
        redirect_uri="http://localhost:8888/callback",
        client_id=Client_ID,
        client_secret=Client_Secret,
        show_dialog=True,
        cache_path="token.txt"
    )
)
#Getting Top BillBoard Songs
date=input("Which year do you want to travel to Type the date in this format YYYY-MM-DD: ")
# response=requests.get(f"https://www.billboard.com/charts/india-songs-hotw/{date}")
response=requests.get(f"https://www.billboard.com/charts/hot-100/{date}")

soup=BeautifulSoup(response.text,"html.parser")
songs=soup.find_all(name="h3",class_="a-no-trucate")
songs_name=[song.getText().replace("\t","").replace("\n","") for song in songs]
# print(songs_name)

#Searching and storing uri in a list.
user_id=spotify_object.current_user()['id']
track_uri_list=[]
for song in songs_name:
    result=spotify_object.search(q=song,limit=1,type='track')
    track_uri=result['tracks']['items'][0]['uri']
    track_uri_list.append(track_uri)

#Creating a Playlist 
# spotify_object.user_playlist_create(user=user_id,name=f"Top Hindi songs of {date.split('-')[0]}")
spotify_object.user_playlist_create(user=user_id,name=f"Top 100 English songs of {date.split('-')[0]}")

#Getting Playlist id
playlist_result=spotify_object.user_playlists(user=user_id)
playlist=playlist_result['items'][0]['id']

#Adding Songs to the Playlist
spotify_object.user_playlist_add_tracks(user=user_id,playlist_id=playlist,tracks=track_uri_list)