from urllib.parse import quote
import requests

from browser_interactions import play_song_on_spotify

def match_song(url: str, service: str = "spotify", region: str = "GB"):
    response = requests.get(
        f"https://api.song.link/v1-alpha.1/links?url={quote(url)}&userCountry={region}&songIfSingle=true"
    )
    entities_by_unique_id = response.json()["entitiesByUniqueId"]
    for service_key in entities_by_unique_id.keys():
        if service_key.startswith(f"{service.upper()}_SONG::"):
            return entities_by_unique_id[service_key]["id"]
    return None

if __name__ == "__main__":
    url = "https://www.youtube.com/watch?v=kVgKio0z1hY"
    id = match_song(url)
    if id != None:
        play_song_on_spotify(id)
