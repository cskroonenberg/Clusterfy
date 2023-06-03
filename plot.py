import matplotlib.pyplot as plt

def plot_playlist_histogram(sp, playlist_ids, title, metrics):
    playlists = {}
    for playlist_id in playlist_ids:
        playlists[playlist_id] = {}
        playlists[playlist_id]['items'] = sp.user_playlist_tracks(None, playlist_id, fields='items.track(id), name')['items']
        playlists[playlist_id]['name'] = sp.playlist(playlist_id, fields='name')['name']
        playlists[playlist_id]['track_ids'] = [item['track']['id'] for item in playlists[playlist_id]['items']]
        playlists[playlist_id]['audio_features'] = sp.audio_features(tracks=playlists[playlist_id]['track_ids'])

    for metric in metrics:
        legend = []
        for playlist_id in playlist_ids:
            single_features = [audio_feature[metric] for audio_feature in playlists[playlist_id]['audio_features']]
            plt.title(f"{title}: {metric}")
            plt.hist(single_features, bins=25, alpha=1/len(playlist_ids))
            legend.append(playlists[playlist_id]['name'])
        
        plt.legend(legend)
        plt.show()