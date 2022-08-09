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


results = sp.current_user_top_tracks(limit=50, offset=0, time_range='medium_term')
top_tracks = results['items']
top_ids = []
i = 0
for i in range(50):
    top_ids.append(top_tracks[i]['id'])

features = []
j = 0
for j in range(50):
    audio = sp.audio_features(top_ids[j])
    for song in audio:
        features.append(song)
        features[-1]['target'] = 1

songs_data = pd.DataFrame(features)
filename = 'data/mySpotify.csv'
songs_data.to_csv(filename, index=False, encoding='utf-8')

features_names = ['danceability', 'energy', 'loudness', 'speechiness', 'acousticness',
                  'instrumentalness', 'valence', 'tempo']
k = 0
for k in range(8):
    plt.figure()
    plt.hist(songs_data[features_names[k]])
    title = 'Measurement of ' + features_names[k]
    plt.title(title)
    plt.xlabel(features_names[k])
    plt.ylabel('Number of Songs')
    fig = 'data/' + features_names[k] + '.png'
    plt.savefig(fig)


