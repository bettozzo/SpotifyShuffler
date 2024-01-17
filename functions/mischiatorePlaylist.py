from spotify import Spotify
import random
from datetime import datetime

def ignora_album(t, ignora):
    album:str = t['album']['title']
    for i in ignora:
        if album.lower() == i.lower():
            return False
    return True

def ignora_artisti(t, ignora):
    for a in t['artists']:
        for i in ignora:
            if str(a['name']).lower() == i.lower():
                return False
    return True

def get_tracks_from_playlist(target:str, playlists, album_da_ignorare, artisti_da_ignorare):
    playlist = {}
    target = target.lower()
    for p in playlists['playlists']:
        if p['title'].lower() == target or p['uri'].lower() == target:
            playlist = p
            break
    if playlist != {}:
        tracks = []
        for t in playlist['tracks']:
            if ignora_album(t, album_da_ignorare) and ignora_artisti(t, artisti_da_ignorare):
                tracks.append(t)
        return tracks
    print("Playlist da cui prelevare tracks non trovata. Title/uri: " + target)
    exit(1)


def shuffle_playlist(target, album_da_ignorare, artisti_da_ignorare, artisti_preferiti, playlists, spotify:Spotify):
    #STEP 1: assegno punteggio a tutte tracks (default:2)
    #STEP 2: prendo un track a caso
    #STEP 3: itero su artisti e aumento di 2 tutte le tracks che non hanno quell'artista
    #STEP 4: rimuovo traccia da quelle possibili
    #STEP 5: ripeto STEP 2 fino a fine playlist
    #STEP 6: caricare playlist su spotify

    playlist_duration = 0
    #STEP 0: carico traccie da playlist
    tracks = get_tracks_from_playlist(target, playlists, album_da_ignorare, artisti_da_ignorare)

    #STEP 1: assegno punteggio
    data = []
    result = []
    punteggi = []
    recently_played_uris = spotify.get_recently_played()
    for i, t in enumerate(tracks):
        playlist_duration += t['duration']
        punteggio = 2
        bonus = 1
        for af in artisti_preferiti:
            for a in t['artists']:
                if a['name'] == af:
                    bonus += 2
                    punteggio += 3
        for rp in recently_played_uris:
            if t['uri'] == rp:
                punteggio = -3
                break
        data.append({'traccia':t, 'punteggio':punteggio, 'bonus':bonus, "index_in_array": i})
        punteggi.append(punteggio)

    #STEP 5: loop
    while len(data) > 0:
        #STEP 2: traccia casuale
        traccia_scelta = random.choices(data, weights=punteggi, k=1)[0]
        index_traccia_scelta = traccia_scelta['index_in_array']
        traccia_scelta = traccia_scelta['traccia']
        result.append(traccia_scelta['uri'])

        #STEP 3: itero artisti
        for a_ts in traccia_scelta['artists']:
            for t in data:
                for a_t in t['traccia']['artists']:
                    if len(t['traccia']['artists']) == 1:
                        if a_t['uri'] != a_ts['uri']:
                            t['punteggio'] += 2*t['bonus']
                    else:
                        if a_t['uri'] != a_ts['uri']:
                            t['punteggio'] += 1*t['bonus']

        
        #STEP 4: rimuovo traccia
        new_data = []
        punteggi = []
        index = 0
        for i, track in enumerate(data):
            if i != int(index_traccia_scelta):
                new_data.append({'traccia':track['traccia'], 'punteggio':track['punteggio'], 'bonus':track['bonus'], "index_in_array": index})
                punteggi.append(track['punteggio'])
                index += 1
        data = new_data
    
    #STEP 6: Uploading playlist
    new_playlist = spotify.create_playlist("|Shuffled "+target, "Playlist creata automaticamente da un bellissimo programma nel giorno del Signore: "+datetime.now().strftime("%d/%m/%Y"))
    spotify.add_tracks((new_playlist['uri'].split(":"))[2], result)