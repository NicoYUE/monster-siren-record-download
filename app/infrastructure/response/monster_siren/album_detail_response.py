from dataclasses import dataclass
from typing import List


@dataclass
class AlbumDetailResponse:
    album_id: str
    songs_id: List[str]
