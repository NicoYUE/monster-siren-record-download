from dataclasses import dataclass


@dataclass
class MsrSong:
    song_id: str
    name: str
    album_name: str
    cover_url: str
    source_url: str
    lyric_url: str
    artists: []
