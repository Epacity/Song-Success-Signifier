import json
import random
import requests
import string
import urllib.parse

from bs4 import BeautifulSoup

from captcha_solver import *
from config import CLIENT_VERSION, PLAYLIST_QUERY_HASH, USER_AGENT
from typing import Optional


def generate_device_id() -> str:
    return "".join([
        random.choice(string.ascii_letters + string.digits) for _ in range(32)
    ]).lower()

def clean_lyrics(lyrics: str) -> str:
    to_remove = ["\u266A"]
    for symbol in to_remove:
        lyrics = lyrics.replace(symbol, "")

    while lyrics.endswith("\n"):
        lyrics = lyrics[:-1]

    return lyrics

class Account:
    def __init__(self, email: str, password: str, auth_token: str = "", client_id: str = ""):
        self.email = email
        self.password = password
        self.auth_token = auth_token
        self.client_id = client_id

        self.session = requests.Session()

        # Uncomment when using Charles Proxy
        # self.session.verify = False

        self.flow_ctx = ""
        self.client_token = ""


    def get_ctx(self) -> Optional[str]:
        url = "https://accounts.spotify.com/en/login?continue=https%3A%2F%2Fopen.spotify.com%2F"
        headers = {
            "Host": "accounts.spotify.com",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language":"en-US,en;q=0.9",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": USER_AGENT
        }
        try:
            response = self.session.get(url, headers=headers)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")
            ctx_tag = soup.find("meta", attrs={"id":"bootstrap-data"})
            bootstrap_data = ctx_tag.get("sp-bootstrap-data")
            if not bootstrap_data:
                return "Could not get CTX"

            self.flow_ctx = json.loads(bootstrap_data)["flowCtx"]
            return None

        except requests.HTTPError as error:
            return f"Bad status code: {error.response.status_code}"

        except Exception as error:
            return f"Unknown error: {error}"

    def login(self, recaptcha_token: str) -> Optional[str]:
        if not recaptcha_token:
            return "No reCaptcha V3 token"

        if not self.flow_ctx:
            return "No CTX token"

        csrf_token = self.session.cookies.get("sp_sso_csrf_token")
        if not csrf_token:
            return "No CSRF token"

        endpoint = "https://accounts.spotify.com/login/password"
        headers = {
            "Host": "accounts.spotify.com",
            "Accept": "application/json",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded",
            "Origin": "https://accounts.spotify.com",
            "Priority": "u=1, i",
            "Referer": "https://accounts.spotify.com/en/login?continue=https%3A%2F%2Fopen.spotify.com%2F",
            "User-Agent": USER_AGENT,
            "x-csrf-token": csrf_token,
        }
        payload = {
            "username": self.email,
            "password": self.password,
            "continue": f"https://open.spotify.com/?flow_ctx={self.flow_ctx}",
            "recaptchaToken": recaptcha_token,
            "flowCtx": self.flow_ctx
        }
        try:
            response = self.session.post(endpoint, headers=headers, data=payload)
            response.raise_for_status()

            response_data = response.json()
            if "result" in response_data.keys() and response_data["result"] == "ok":
                return None

            return "Login failed"

        except requests.HTTPError as error:
            if error.response.status_code == 400:
                error_data = error.response.json()
                return  f"Spotify error: {error_data['error']}"

            return f"Bad status code: {error.response.status_code}"

        except Exception as error:
            return f"Unknown error: {error}"

    def get_bearer_token(self) -> Optional[str]:
        url = f"https://open.spotify.com/?flow_ctx={self.flow_ctx}"
        headers = {
            "Host": "open.spotify.com",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "keep-alive",
            "Priority": "u=1, i",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": USER_AGENT
        }
        try:
            response = self.session.get(url, headers=headers)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")
            session_tag = soup.find("script", attrs={"id":"session"})
            session_data = json.loads(session_tag.text)

            self.auth_token = session_data["accessToken"]
            self.client_id = session_data["clientId"]
            return None

        except requests.HTTPError as error:
            return f"Bad status code: {error.response.status_code}"

        except Exception as error:
            return f"Unknown error: {error}"

    def get_client_token(self) -> Optional[str]:
        if not self.client_id:
            return "No client ID"

        endpoint = "https://clienttoken.spotify.com/v1/clienttoken"
        headers = {
            "Host": "clienttoken.spotify.com",
            "Accept": "application/json",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "keep-alive",
            "Content-Type": "application/json",
            "Origin": "https://open.spotify.com",
            "Priority": "u=1, i",
            "Referer": "https://open.spotify.com/",
            "User-Agent": USER_AGENT
        }
        payload = {
            "client_data": {
                "client_version": CLIENT_VERSION,
                "client_id": self.client_id,
                # in the future, this device data would be randomized ;)
                "js_sdk_data": {
                    "device_brand": "Apple",
                    "device_model": "unknown",
                    "os": "macos",
                    "os_version": "10.15.7",
                    "device_id": generate_device_id(),
                    "device_type": "computer"
                }
            }
        }
        try:
            response = self.session.post(endpoint, headers=headers, json=payload)
            response.raise_for_status()

            response_data = response.json()

            if response_data["response_type"] != "RESPONSE_GRANTED_TOKEN_RESPONSE":
                return "Could not generate client token"

            self.client_token = response_data["granted_token"]["token"]
            return None

        except requests.HTTPError as error:
            return f"Bad status code: {error.response.status_code}"

        except Exception as error:
            return f"Unknown error: {error}"


class SpotifyClient:
    def __init__(self, account: Account):
        self.account = account
        self.session = self.account.session

        self.api_headers = {
            "Host": "api.spotify.com",
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
            "Authorization": f"Bearer {self.account.auth_token}",
            "Client-Token": self.account.client_token,
            "Connection": "keep-alive",
            "Origin": "https://open.spotify.com",
            "Referer": "https://open.spotify.com/",
            "Priority": "u=1, i",
            "User-Agent": USER_AGENT
        }

        self.spclient_headers = {
            "Host": "spclient.wg.spotify.com",
            "Accept": "application/json",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en",
            "App-Platform": "WebPlayer",
            "Authorization": f"Bearer {self.account.auth_token}",
            "Client-Token": self.account.client_token,
            "Connection": "keep-alive",
            "Origin": "https://open.spotify.com",
            "Referer": "https://open.spotify.com/",
            "Priority": "u=1, i",
            "Spotify-App-Version": CLIENT_VERSION,
            "User-Agent": USER_AGENT
        }

    def get_tracks_from_playlist(self, playlist_id: str) -> (list[dict], Optional[str]):
        endpoint = "https://api-partner.spotify.com/pathfinder/v1/query"
        headers = self.spclient_headers.copy()
        headers["Host"] = "api-partner.spotify.com"
        params = {
            "operationName": "fetchPlaylistContentsWithGatedEntityRelations",
            "variables": '{"uri":"' + playlist_id + '","offset":0,"limit":100}',
            "extensions": '{"persistedQuery":{"version":1,"sha256Hash":"' + PLAYLIST_QUERY_HASH +  '"}}'
        }

        try:
            response = self.session.get(endpoint, headers=headers, params=params)
            response.raise_for_status()

            response_data = response.json()

            tracks = []
            for track in response_data["data"]["playlistV2"]["content"]["items"]:
                track_dict = {}
                track_data = track["itemV2"]["data"]
                track_dict["image"] = track_data["albumOfTrack"]["coverArt"]["sources"][0]["url"]
                track_dict["artist"] = track_data["artists"]["items"][0]["profile"]["name"]
                track_dict["length"] = track_data["trackDuration"]["totalMilliseconds"]
                track_dict["title"] = track_data["name"]
                track_dict["play_count"] = track_data["playcount"]
                track_dict["id"] = track_data["uri"]
                tracks.append(track_dict)

            return tracks, None

        except requests.HTTPError as error:
            return [], f"Bad status code: {error.response.status_code}"

        except Exception as error:
            return [], f"Unknown error: {error}"

    def get_song_lyrics(self, track_id: str, image_url: str) -> (str, Optional[str]):
        if ":" in track_id:
            track_id = track_id.split(":")[-1]

        endpoint = f"https://spclient.wg.spotify.com/color-lyrics/v2/track/{track_id}/image/{urllib.parse.quote_plus(image_url)}"
        params = {
            "format": "json",
            "vocalRemoval": "false",
            "market": "from_token"
        }
        try:
            response = self.session.get(endpoint, headers=self.spclient_headers, params=params)
            response.raise_for_status()

            response_data = response.json()
            lyrics_str = ""
            for lyric in response_data["lyrics"]["lines"]:
                lyrics_str += lyric["words"] + "\n"

            return lyrics_str, None

        except requests.HTTPError as error:
            if error.response.status_code == 404:
                return "", "Lyrics are not available"

            elif error.response.status_code == 408:
                return "", "Rate limited (408)"

            return "", f"Bad status code: {error.response.status_code}"

        except Exception as error:
            return "", f"Unknown error: {error}"
