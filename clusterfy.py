import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
from sklearn.cluster import KMeans
import numpy as np
from tqdm import tqdm
import yaml
import os

with open("spotify_details.yml", 'r') as stream:  
    spotify_details = yaml.safe_load(stream)

print('0')
scope = "user-library-modify user-library-read playlist-modify-public"

os.environ["SPOTIPY_CLIENT_ID"] = spotify_details['client_id']
os.environ["SPOTIPY_CLIENT_SECRET"] = spotify_details['client_secret']
os.environ["SPOTIPY_REDIRECT_URI"] = spotify_details['redirect_uri']

username = spotify_details['username']

my_token = util.prompt_for_user_token(username,scope=scope, show_dialog=True)
sp = spotipy.Spotify(auth=my_token)

print(sp.me())

track_features = []
liked_tracks = []
for i in tqdm(range(5)):
    liked_tracks += sp.current_user_saved_tracks(offset=i*50, limit=50)['items']

for track in liked_tracks:
        track_id = track['track']['id']
        features = sp.audio_features(track_id)
        if features:
            track_features.append(features[0])

print('5')
# Extract relevant audio features for clustering
X = np.array([[
#    f['danceability'],
#    f['energy'],
#    f['valence'],
#    f['acousticness'],
#    f['instrumentalness'],
#    f['tempo'],
#    f['mode'],
#    f['key'],
#    f['speechiness']
] for f in track_features])

# Perform K-means clustering
k = 4 # Number of clusters/playlists
kmeans = KMeans(init="k-means++", n_init=1, max_iter=10000, n_clusters=k, random_state=42)
cluster_labels = kmeans.fit_predict(X)
print('7')
# Create playlists based on cluster labels
playlist_ids = []
for i in range(k):
    playlist_name = f"Tempo Cluster {i+1}"
    playlist = sp.user_playlist_create(user=username, name=playlist_name)
    playlist_ids.append(playlist['id'])
print('8')
# Add tracks to respective playlists based on cluster labels
for i, track in enumerate(liked_tracks):
    track_id = track['track']['id']
    sp.user_playlist_add_tracks(user=username, playlist_id=playlist_ids[cluster_labels[i]], tracks=[track_id])
