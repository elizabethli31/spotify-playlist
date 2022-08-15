import tensorflow as tf
import keras
from keras.models import Sequential
from keras.layers.core import Dense
import pandas as pd
import sys
import json
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import spotipy.util as util

cid = '2693c65b89f3470c85d2295c2ffa9ef4'
secret = '6d7d982e8f9c4385ab1d177b0fa5ba93'
redirect_uri = 'https://127.0.0.1:8000/spotify/callback/'

os.environ['SPOTIPY_CLIENT_ID']= cid
os.environ['SPOTIPY_CLIENT_SECRET']= secret
os.environ['SPOTIPY_REDIRECT_URI']='https://127.0.0.1:8000/spotify/callback/'

username = ""
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret) 
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
scope = 'user-top-read playlist-modify-public'
token = util.prompt_for_user_token(username, scope)

user = sp.current_user()
print(json.dumps(user))

if token:
    sp = spotipy.Spotify(auth=token)
else:
    print("Can't get token for", username)

training_data = pd.read_csv('src/mySpotify2.csv')

features = ['danceability', 'energy', 'loudness', 'speechiness', 'acousticness',
            'instrumentalness', 'valence', 'tempo']

x_train = training_data[features]
y_train = training_data['target']

model = Sequential()
model.add(Dense(12, input_shape=(8,), activation='relu'))
model.add(Dense(8, activation='relu'))
model.add(Dense(1, activation='sigmoid'))

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

model.fit(x_train, y_train, epochs=150, batch_size=10)

_, accuracy = model.evaluate(x_train, y_train)

predictor = pd.read_csv('data/searchSpotify2.csv')
predictions = model.predict(predictor[features])

liked_ids = []
i = 0

for prediction in predictions:
    if(prediction>.5):
        liked_id = predictor.loc[i]['id']
        liked_ids.append(liked_id)
    i += 1

if len(sys.argv) > 1:
    playlist_title = sys.argv[1]

new_playlist = sp.user_playlist_create(user=user['id'], name=playlist_title, 
description="Songs you might like based on your search")

# playlists = sp.user_playlist()
k = 0
for k in range(0, len(liked_ids), 100):
    add = sp.user_playlist_add_tracks(user=user['id'], playlist_id=new_playlist['id'], tracks=liked_ids[k:k+100])

# print(liked)
