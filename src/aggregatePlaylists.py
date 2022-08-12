import sys
import json
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import spotipy.util as util
import pandas as pd
import matplotlib.pyplot as plt


cid = '2693c65b89f3470c85d2295c2ffa9ef4'
secret = '6d7d982e8f9c4385ab1d177b0fa5ba93'
redirect_uri = 'https://127.0.0.1:8000/spotify/callback/'

os.environ['SPOTIPY_CLIENT_ID']= cid
os.environ['SPOTIPY_CLIENT_SECRET']= secret
os.environ['SPOTIPY_REDIRECT_URI']='https://127.0.0.1:8000/spotify/callback/'

username = ""
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret) 
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
scope = 'user-top-read'
token = util.prompt_for_user_token(username, scope)

if token:
    sp = spotipy.Spotify(auth=token)
else:
    print("Can't get token for", username)


if (len(sys.argv) > 1):
    key_word = sys.argv[1]
else:
    print("No keyword given")

results = sp.search(key_word, limit=5, offset=0, type='playlist')
playlist=results['playlists']
track_ids = []

for item in playlist['items']:

    user_id = item['owner']['id']
    playlist_id = item['id']
    tracks = sp.user_playlist_tracks(user_id, playlist_id)

    for track in tracks['items']:

        try:

            track_ids.append(track['track']['id'])

        except:

            pass

features = []
i = 0
for i in range(len(track_ids)):
    audio = sp.audio_features(track_ids[i])
    for song in audio:
        if (song):
            features.append(song)

songs_data = pd.DataFrame(features)
filename = 'data/searchSpotify2.csv'
songs_data.to_csv(filename, index=False, encoding='utf-8')
