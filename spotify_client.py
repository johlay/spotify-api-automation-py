import base64
import json
import os
import requests
import six
import urllib
import webbrowser
from requests.auth import HTTPBasicAuth
from urllib import parse


class SpotifyClient(object):
    def __init__(self):
        self.spotify_user_id = os.getenv("SPOTIFY_USER_ID")
        self.spotify_client_id = os.getenv("SPOTIFY_API_CLIENT_ID")
        self.spotify_client_secret = os.getenv("SPOTIFY_API_CLIENT_SECRET")
        self.spotify_access_token = ""
        self.spotify_authorization_token = ""

    def get_spotify_authorization_token(self):
        """Request User Authorization"""

        query_parameters = {
            "client_id": self.spotify_client_id,
            "response_type": "code",
            "redirect_uri": "https://developer.spotify.com/",
            "scope": "playlist-modify-public playlist-modify-private"
        }

        query = "https://accounts.spotify.com/authorize?" + \
            urllib.parse.urlencode(query_parameters)

        webbrowser.open(query)
        response_url = input("Enter the URL that you were redirected to: ")

        request_body = {
            "grant_type": "authorization_code",
            "code": parse.parse_qs(parse.urlsplit(response_url).query)["code"][0],
            "redirect_uri": query_parameters["redirect_uri"]
        }

        auth_header = base64.b64encode(six.text_type(
            self.spotify_client_id + ":" + self.spotify_client_secret).encode("ascii")).decode("ascii")

        response_auth_token = requests.post(
            url="https://accounts.spotify.com/api/token",
            data=request_body,
            headers={
                "Authorization": "Basic {}".format(auth_header),
                "Content-Type": "application/x-www-form-urlencoded"
            },
            json=True
        )

        response_auth_token_json = response_auth_token.json()

        self.spotify_authorization_token = response_auth_token_json["access_token"]

        return response_auth_token.status_code

    def get_spotify_access_token(self):
        """Request an access token"""
        scope = "playlist-modify-public playlist-modify-private"

        request_body = {
            "grant_type": "client_credentials",
            "scope": scope
        }
        query = "https://accounts.spotify.com/api/token"

        response = requests.post(
            auth=HTTPBasicAuth(self.spotify_client_id,
                               self.spotify_client_secret),
            url=query,
            data=request_body,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )

        response_json = response.json()
        access_token = response_json["access_token"]

        self.spotify_access_token = access_token
