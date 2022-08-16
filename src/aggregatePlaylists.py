import pandas as pd

def get_tracks_by_keyword(keyword, ids, sp, my_id):
    results = sp.search(keyword, limit=5, offset=0, type='playlist')
    items = results['playlists']['items']

    for item in items:
        user_id = item['owner']['id']

        if user_id == my_id:
            continue
        
        playlist_id= item['id']
        tracks = sp.user_playlist_tracks(user_id, playlist_id)

        for track in tracks['items']:
            try:
                ids.append(track['track']['id'])
            except:
                pass

    return ids

def get_keyword_search_features(features, ids, sp):
    i = 0
    for i in range(len(ids)):
        audios = sp.audio_features(ids[i])
        for audio in audios:
            if audio:
                features.append(audio)

    return pd.DataFrame(features)

