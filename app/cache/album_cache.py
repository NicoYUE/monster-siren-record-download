import os.path
import pickle
from typing import Set, Dict

CACHE_DEFAULT_PATH = "./.songs_cache.pkl"


class AlbumCache:
    album_cache_map: Dict[str, Set[str]] = {}

    def __init__(self):
        # Create file if not exist
        if not os.path.exists(CACHE_DEFAULT_PATH):
            with open(CACHE_DEFAULT_PATH, "wb") as file:
                file.write(pickle.dumps(self.album_cache_map))

        with open(CACHE_DEFAULT_PATH, "rb") as file:
            try:
                self.album_cache_map = pickle.load(file)
            except EOFError:
                pass

    def cache(self, album: str, title: str):
        if album not in self.album_cache_map:
            self.album_cache_map[album] = set()

        value_set = self.album_cache_map[album]
        value_set.add(title)

        with open(CACHE_DEFAULT_PATH, "wb") as file:
            file.write(pickle.dumps(self.album_cache_map))

    def album_exists(self, album: str) -> bool:
        return album in self.album_cache_map

    def song_exists(self, album: str, title: str) -> bool:
        if album not in self.album_cache_map:
            return False

        return title in self.album_cache_map[album]
