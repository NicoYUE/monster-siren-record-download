from dataclasses import dataclass


@dataclass
class AlbumResponse:
    album_id: str
    name: str
    cover_url: str
