import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import copy
import json

# Top 100 Songs of 1960 - Billboard Year End Charts
playlists = {1960: 'https://open.spotify.com/playlist/0nfHJsAnubkIUXrazaqHL9'}

myClientId = 'yourClientID'
myClientSecret = 'yourClientSecret'

client_credentials_manager = SpotifyClientCredentials(client_id=myClientId, client_secret=myClientSecret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

playlist_data = []
keys = list(playlists.keys())

for x in range(0, len(keys)):
    playlist_data.append((keys[x], sp.playlist_items(playlists[keys[x]], fields='items(track(name,id,popularity,artists))')))

for k in range(0, len(playlist_data)):
    tmp = []
    for n in range(0, len(playlist_data[k][1]['items'])):
        try:
            tmp.append({'id': playlist_data[k][1]['items'][n]['track']['id'],
                        'name': playlist_data[k][1]['items'][n]['track']['name'],
                        'popularity': playlist_data[k][1]['items'][n]['track']['popularity'],
                        'artists': playlist_data[k][1]['items'][n]['track']['artists'],
                        'features': sp.audio_features(playlist_data[k][1]['items'][n]['track']['id'])[0]})
            print(n + 1, 'tracks appended. Current: ', tmp[-1]['name'])
        except ValueError:
            print("An exception occurred. Song is probably unavailable in your region", ValueError)

    with open('data\\playlist-' + str(playlist_data[k][0]) + '.json', 'w', encoding='utf-8') as f:
        json.dump({'year': playlist_data[k][0], 'data': copy.copy(tmp)}, f, ensure_ascii=False, indent=3)

    # year += 1
