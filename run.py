from dotenv import load_dotenv
from pathlib import Path
from spotify_client import SpotifyClient


def run():
    load_dotenv(dotenv_path=Path("credentials/.env"))

    spotify_client_instance = SpotifyClient()
    spotify_client_instance.get_spotify_access_token()
    spotify_client_instance.get_spotify_authorization_token()


if __name__ == "__main__":
    run()
