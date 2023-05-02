from typing import List

from requests import Session

from domain.model.msr_album import MsrAlbum
from domain.model.msr_song import MsrSong
from infrastructure.monster_siren_repository import MonsterSirenRepository
from infrastructure.response.monster_siren.album_detail_response import AlbumDetailResponse
from infrastructure.response.monster_siren.song_response import SongResponse


class MonsterSirenService:

    def __init__(self, session: Session, monster_siren_repository: MonsterSirenRepository):
        self.session = session
        self.monster_siren_repository = MonsterSirenRepository(self.session)

    def get_all_albums(self) -> List[MsrAlbum]:
        return [MsrAlbum(album_id=album_response.album_id,
                         name=album_response.name,
                         cover_url=album_response.cover_url)
                for album_response in self.monster_siren_repository.get_albums()]

    def get_msr_album_songs(self, album: MsrAlbum) -> List[MsrSong]:
        songs = []
        album_detail: AlbumDetailResponse = self.monster_siren_repository.get_album_details(album.album_id)

        for song_id in album_detail.songs_id:
            songs.append(self.get_msr_song(album, song_id))
        return songs

    def get_msr_song(self, album: MsrAlbum, song_id: str) -> MsrSong:
        song: SongResponse = self.monster_siren_repository.get_song_details(song_id)
        return MsrSong(song_id=song_id,
                       name=song.name,
                       album_name=album.name,
                       cover_url=album.cover_url,
                       source_url=song.source_url,
                       lyric_url=song.lyric_url,
                       artists=song.artists)

        # def get_all_msr_songs(self) -> List[MsrSong]:
        #     songs = []
        #     albums: List[AlbumResponse] = self.monster_siren_repository.get_albums()
        #
        #     for album in albums:
        #         album_detail = self.monster_siren_repository.get_album_details(album.album_id)
        #
        #         for song_id in album_detail.songs_id:
        #             songs.append(self.get_msr_song(album, song_id))
        #     return songs

