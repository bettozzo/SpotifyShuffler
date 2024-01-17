from functions import mischiatorePlaylist as mis

def mischia_playlist(playlist, album_da_ignorare, artisti_da_ignorare, artisti_preferiti, playlists, spotify):
    return mis.shuffle_playlist(playlist, album_da_ignorare, artisti_da_ignorare, artisti_preferiti, playlists, spotify)

