from dataclasses import dataclass


@dataclass
class Metadata:
    title: str
    album_name: str
    artists: []
    cover_path: str
    lyric_path: str
