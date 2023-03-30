import os
from typing import List

from requests import Session

from infrastructure.response.msr.album_detail_response import AlbumDetailResponse
from infrastructure.response.msr.album_response import AlbumResponse
from infrastructure.response.msr.song_response import SongResponse
from utility import str_utility

ALBUMS_URL = "https://monster-siren.hypergryph.com/api/albums"
SONG_DETAIL_URL = "https://monster-siren.hypergryph.com/api/song/{}"
ALBUM_DETAIL_URL = "https://monster-siren.hypergryph.com/api/album/{}/detail"


class MonsterSirenRepository:

    def __init__(self, session: Session):
        self.session = session

    def get_albums(self) -> List[AlbumResponse]:
        response = self.get_json_request(ALBUMS_URL)["data"]
        return [AlbumResponse(album_id=elem["cid"],
                              name=elem["name"],
                              cover_url=elem["coverUrl"]) for elem in response]

    def get_album_details(self, album_id: str) -> AlbumDetailResponse:
        response = self.get_json_request(ALBUM_DETAIL_URL.format(album_id))["data"]

        songs_id = [song["cid"] for song in response["songs"]]
        return AlbumDetailResponse(album_id=response["cid"],
                                   songs_id=songs_id)

    def get_song_details(self, song_id: str) -> SongResponse:
        response = self.get_json_request(SONG_DETAIL_URL.format(song_id))["data"]

        name = response["name"]
        if os.name == "nt":
            name = str_utility.windows_valid_name(name)

        return SongResponse(song_id=response["cid"],
                            name=name,
                            album_id=response["albumCid"],
                            source_url=response["sourceUrl"],
                            lyric_url=response["lyricUrl"],
                            artists=response["artists"])

    def get_json_request(self, url: str):
        return self.session.get(url, headers={'Accept': 'application/json'}).json()

