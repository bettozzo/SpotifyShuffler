import requests
import json
from refresh import Refresh
from dotenv import load_dotenv
import os
import time

class Spotify:
    def __init__(self):
        self.spotify_token = ""
        self.call_refresh()


    def call_refresh(self):
        refreshCaller = Refresh()
        self.spotify_token = refreshCaller.refresh()

    def filter_tracks(self, tracks):
        data = []
        if tracks != []:
            for t in tracks['items']:
                artists = []
                for artist in t['track']['artists']:
                    artists.append({"name":artist['name'],
                                    "uri":artist['uri']})
                data.append({"title":t['track']['name'],
                            "uri":t['track']['uri'],
                            "duration":t['track']['duration_ms'],
                            "artists": artists,
                            "album":{"title":t['track']['album']['name'],
                                    "uri":t['track']['album']['uri']}
                            })
        return data

        
    def get_tracks(self, playlist_id, playlist_name, offset):
        URL = "https://api.spotify.com/v1/playlists/{}/tracks?offset={}".format(playlist_id, offset)
        response = requests.get(
            URL,
            headers={
                "Authorization": "Bearer {}".format(self.spotify_token)
            }
        )
        
        tracks = response.json()
        filteredTracks = self.filter_tracks(tracks)
        return filteredTracks

    def get_playlists(self, getAllTracks = True):
        URL = "https://api.spotify.com/v1/me/playlists"
        response = requests.get(
            URL,
            headers={
                "Authorization": "Bearer {}".format(self.spotify_token)
            }
        )
        json_resp = response.json()
        playlists = []
        hidden_playlists = []
        for data in json_resp['items']:
            if data['name'][0] != '|':
                playlists.append({"nome": data['name'],
                                "uri": data['uri'],
                                "collaborative": data['collaborative'],
                                "total_tracks": data['tracks']['total']})
            else:
                hidden_playlists.append({"nome": data['name'],
                                "uri": data['uri'],
                                "collaborative": data['collaborative'],
                                "total_tracks": data['tracks']['total']})



        if not getAllTracks:
            return playlists+hidden_playlists

        result = []
        for playlist in playlists:
            print("Loading data from the playlist: " + playlist['nome']+ "...")
            duration = 0
            result_tracks = []
            tracks = self.get_tracks((playlist['uri'].split(":"))[2], playlist['nome'], 0)
            counter = 0
            while len(tracks) != 0:
                for track in tracks:
                    result_tracks.append(track)
                    duration += track['duration']
                counter += 100
                tracks = self.get_tracks((playlist['uri'].split(":"))[2], playlist['nome'], counter)
            result.append({"title":playlist['nome'],
                            "uri":playlist['uri'],
                            "collaborative": playlist['collaborative'],
                            "duration":duration,
                            "total_tracks":playlist['total_tracks'],
                            "tracks":result_tracks
                            })
        return {"timestamp_last_update": int(time.time()),
                "playlists": result
                }

    def delete_playlist(self, playlist_id):
        query = "https://api.spotify.com/v1/playlists/{}/followers".format(playlist_id)
        requests.delete(
            query,
            headers={
                "Authorization": "Bearer {}".format(self.spotify_token)
            }
        )

    def create_playlist(self, nome, description):

        print("Creating playlist " + nome + "... ")
        load_dotenv()
        url = "https://api.spotify.com/v1/users/{}/playlists".format(os.getenv('user_id'))
        response = requests.post(
            url,
            headers={
                'Content-Type': 'application/json',
                "Authorization": "Bearer {}".format(self.spotify_token)
            },
            json={
                "name": nome,
                "description": description
            }
        )
        json_resp = response.json()
        return json_resp

    def add_tracks(self, playlist_id, tracks):
        url = "https://api.spotify.com/v1/playlists/{}/tracks".format(playlist_id)
        tmp = [tracks[x:x+100] for x in range(0, len(tracks), 100)]
        for t in tmp:
            response = requests.post(
                url,
                headers={
                    "Authorization": "Bearer {}".format(self.spotify_token)
                },
                json={
                    "uris":t
                }
            )
        json_resp = response.json()
        return json_resp

    def getTracksInJSON(self):
        print("I dati risultano essere almeno di 24 ore fa, quindi li vado a ricaricare")
        result = self.get_playlists()
        with open('./jsons/data.json', 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=4)

    
    def fetch_data(self):
        file = open('./jsons/data.json', encoding="utf8")
        data = json.load(file)
        file.close()
        if time.time() - data['timestamp_last_update'] >= 24*3600:   #dati più vecchi di 24h
            self.getTracksInJSON()
        f = open('./jsons/data.json', encoding="utf8")
        playlists = json.load(f)
        f.close()
        return playlists

    def get_playlist_uri(self, playlist_nome, moreThanOne = False):
        playlists = self.get_playlists(False)
        result = []
        for p in playlists:
            if p['nome'] == playlist_nome:
                result.append(p['uri'])
        if not moreThanOne and len(result) > 1:
            print("MORE THAN 1 PLAYLIST WITH NAME: " + playlist_nome)
            exit(1)
        if moreThanOne:
            return result
        return result[0]
    
    def get_recently_played(self):
        url = "https://api.spotify.com/v1/me/player/recently-played"
        response = requests.get(
            url,
            headers={
                'Content-Type': 'application/json',
                "Authorization": "Bearer {}".format(self.spotify_token)
            }
        )
        result = []
        for t in self.filter_tracks(response.json()):
            result.append(t['uri'])
        return result