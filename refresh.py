from dotenv import load_dotenv
import os
import requests

class Refresh:
    def __init__(self):
        load_dotenv()
        self.refresh_token = os.getenv('refresh_token')
        self.base_64 = os.getenv('base_64')
    
    def refresh(self):
        query = 'https://accounts.spotify.com/api/token'
        response = requests.post(query,
                                data={"grant_type":"refresh_token", "refresh_token": self.refresh_token},
                                headers={"Authorization": "Basic " + self.base_64})
        response_json = response.json()
        return response_json['access_token']