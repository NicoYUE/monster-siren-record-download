from dataclasses import dataclass


@dataclass
class MsrAlbum:
    album_id: str
    name: str
    cover_url: str
