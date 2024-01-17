from spotify import Spotify

def remove_same_name_playlists(spotify:Spotify, playlist_nome):
    targets = spotify.get_playlist_uri(playlist_nome, True)
    for t in targets:
        spotify.delete_playlist((t.split(":"))[2])