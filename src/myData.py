import pandas as pd
import matplotlib.pyplot as plt

def get_user_top_ids(ids, sp):
    ids = []

    # User Top Tracks
    results = sp.current_user_top_tracks(limit=50, offset=0, time_range='medium_term')
    tracks = results['items']

    i = 0
    for i in range(len(tracks)):
        ids.append(tracks[i]['id'])


    # User Saved Tracks
    results = sp.current_user_saved_tracks(limit=50, offset=0)
    tracks = results['items']

    i = 0
    for i in range(len(tracks)):
        ids.append(tracks[i]['track']['id'])


    # User Top Artists
    results = sp.current_user_top_artists(limit=20, offset=0, time_range='medium_term')
    artists = []
    for result in results['items']:
        artists.append(result['id'])
    
    i = 0
    for i in range(len(artists)):
        tracks = sp.artist_top_tracks(artists[i], country='US')
        for track in tracks['tracks']:
            ids.append(track['id'])

    return ids


def get_playlist_tracks(ids, playlist, sp):
    tracks = sp.playlist_tracks(playlist, limit=100, offset=0)

    while tracks:
        for song in tracks['items']:
            ids.append(song['track']['id'])
    
        if tracks['next']:
            tracks = sp.next(tracks)
        else:
            break
    
    return ids


def get_features(features, like, dislike, sp):

    i = 0
    for i in range(len(like)):
        audios = sp.audio_features(like[i])

        for audio in audios:
            features.append(audio)
            features[-1]['target'] = 1

    i = 0
    for i in range(len(dislike)):
        audios = sp.audio_features(dislike[i])

        for audio in audios:
            features.append(audio)
            features[-1]['target'] = 0

    return pd.DataFrame(features)


def get_data(data, feature_names):
    i = 0
    for i in range(len(feature_names)):
        liked = data[data['target']==1][feature_names[i]]
        disliked = data[data['target']==0][feature_names[i]]
        plt.figure()
        liked.hist(alpha=0.7, bins=30, label='liked')
        disliked.hist(alpha=0.7, bins=30, label='disliked')

        title = 'Measurement of ' + feature_names[i]
        plt.title(title)
        plt.xlabel(feature_names[i])
        plt.ylabel('Number of Songs')
        plt.legend(loc='upper right')

        fig = 'data/' + feature_names[i] + '.png'
        plt.savefig(fig)

    data.to_csv('data/yourSpotifyData.csv', index=False, encoding='utf-8')

    