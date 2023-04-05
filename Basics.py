from dotenv import load_dotenv
import os
import base64 
import requests


load_dotenv()

client_id=os.getenv("CLIENT_ID")
client_secret=os.getenv("CLIENT_SECRET")

print(client_id,client_secret)

def get_token():
    auth_string=client_id+":"+client_secret
    auth_bytes=auth_string.encode('utf-8')
    auth_base64=str(base64.b64encode(auth_bytes),'utf-8')

    url="https://accounts.spotify.com/api/token"
    headers={
        "Authorization":"Basic "+auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data={"grant_type":"client_credentials"}
    result=requests.post(url,headers=headers,data=data)
    json_result=result.json()
    token=json_result["access_token"]
    return token

def get_auth_header(token):
    return {"Authorization":"Bearer "+ token}

def search_for_artist(token,artist_name):
    url="https://api.spotify.com/v1/search"
    headers=get_auth_header(token)
    query=f"?q={artist_name}&type=artist&limit=1"

    query_url=url+query
    response=requests.get(query_url,headers=headers )
    result=response.json()["artists"]["items"]
    if len(result)==0:
        print("No artist with the name Exists...")
        return None

    return result[0]

def get_songs_by_artist(token,artist_id):
    url=f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers=get_auth_header(token)

    response=requests.get(url=url,headers=headers)
    # return response.json()["tracks"]
    return response.json()["tracks"]

token=get_token()
result=search_for_artist(token,"Billie Eilish")
artist_id=result["id"]
songs=get_songs_by_artist(token,artist_id)
print(songs)

for idx,song in enumerate(songs):
    print(f"{idx+1}. {song['name']}")

#---------------Docs----------------
# https://developer.spotify.com/documentation/web-api/reference/#/?security=oauth_2_0

#-------------Base URL--------------
# The base URI for all Web API requests is https://api.spotify.com/v1