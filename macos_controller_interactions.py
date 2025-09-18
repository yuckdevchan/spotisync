import requests

def spotify_play_song(id: str):
    requests.get(f"http://localhost:8801/playTrack/spotify:track:{id}")

def spotify_pause():
    requests.get(f"http://localhost:8801/pause")

def spotify_play():
    requests.get(f"http://localhost:8801/play")
