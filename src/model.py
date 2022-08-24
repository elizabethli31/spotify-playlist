from keras.layers import Dropout
from keras.models import Sequential
from keras.layers.core import Dense
import sys
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
from myData import *
from aggregatePlaylists import *

def make_model(data, feature_names):
    x_train = data[feature_names]
    y_train = data['target']

    model = Sequential([
        Dense(64, activation='tanh', input_shape=(8,), kernel_regularizer='l1'),
        Dense(32, activation='relu', kernel_regularizer='l1'),
        Dense(16, activation='relu', kernel_regularizer='l1'),
        Dense(8, activation='relu', kernel_regularizer='l1'),
        Dense(1, activation='sigmoid')
    ])

    model.compile(loss='binary_crossentropy',
                  optimizer='adam', metrics=['accuracy'])

    model.fit(x_train, y_train, epochs=150, batch_size=10)

    _, accuracy = model.evaluate(x_train, y_train)

    return model


def make_predictions(model, predictor, feature_names):
    predictions = model.predict(predictor[feature_names])

    return predictions


def make_playlist(predictions, predictor, sp, user_id, playlist_title):
    liked_ids = []
    i = 0

    for prediction in predictions:
        if(prediction > .5):
            liked_id = predictor.loc[i]['id']
            liked_ids.append(liked_id)
        i += 1

    new_playlist = sp.user_playlist_create(user=user_id, name=playlist_title,
                                           description="Songs you might like based on your search")

    k = 0
    for k in range(0, len(liked_ids), 100):
        sp.user_playlist_add_tracks(
            user=user_id, playlist_id=new_playlist['id'], tracks=liked_ids[k:k+100])


if __name__ == '__main__':
    if len(sys.argv) != 6:
        print("Missing arguments")
        sys.exit()

    username = sys.argv[1]
    keyword = sys.argv[2]
    dislike_playlist = sys.argv[3]
    playlist_title = sys.argv[4]
    dat = sys.argv[5]

    auth_manager = SpotifyClientCredentials()
    sp = spotipy.Spotify(auth_manager=auth_manager)
    scope = 'user-library-read user-top-read playlist-modify-public'
    token = util.prompt_for_user_token(username, scope)

    if token:
        sp = spotipy.Spotify(auth=token)
    else:
        print("Can't get token for", username)

    like_ids = []
    like_ids = get_user_top_ids(like_ids, sp)

    dislike_ids = []
    dislike_ids = get_playlist_tracks(dislike_ids, dislike_playlist, sp)

    features = []
    training_data = get_features(features, like_ids, dislike_ids, sp)

    feature_names = ['danceability', 'energy', 'loudness', 'speechiness', 'acousticness',
                     'instrumentalness', 'valence', 'tempo']

    if dat:
        get_data(training_data, feature_names)

    search_ids = []
    search_ids = get_tracks_by_keyword(keyword, search_ids, sp, username)

    search_features = []
    search_data = get_keyword_search_features(search_features, search_ids, sp)

    model = make_model(training_data, feature_names)
    predictions = make_predictions(model, search_data, feature_names)
    make_playlist(predictions, search_data, sp, username, playlist_title)
