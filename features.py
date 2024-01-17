from functions import mischiatorePlaylist as mis
from functions import remove_same_playlist as remSame
from functions import gruppiManager as gruppi


def mischia_playlist(playlist, album_da_ignorare, artisti_da_ignorare, artisti_preferiti, playlists, spotify):
    return mis.shuffle_playlist(playlist, album_da_ignorare, artisti_da_ignorare, artisti_preferiti, playlists, spotify)

def remove_same_name(spotify, playlist):
    return remSame.remove_same_name_playlists(spotify, playlist)

def gruppi_manager():
    return gruppi.manager()
