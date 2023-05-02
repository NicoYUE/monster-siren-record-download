from dataclasses import dataclass


@dataclass
class SongResponse:
    song_id: str
    name: str
    album_id: str
    source_url: str
    lyric_url: str
    artists: []
