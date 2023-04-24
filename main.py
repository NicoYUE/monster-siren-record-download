from multiprocessing import Manager

from requests import Session

from cache.album_cache import AlbumCache
from domain.model.metadata import Metadata
from domain.monster_siren_service import MonsterSirenService
from infrastructure.monster_siren_repository import MonsterSirenRepository
from utility import os_utility, audio_metadata_utility
from utility.media_downloader import MediaDownloader


if __name__ == '__main__':
    BASE_DIRECTORY = "./MSR/"
    session: Session = Session()

    os_utility.make_dir_if_not_exist(BASE_DIRECTORY)

    msr_repository = MonsterSirenRepository(session)
    msr_service = MonsterSirenService(session, msr_repository)
    media_downloader = MediaDownloader(session)

    album_cache = AlbumCache()

    albums = msr_service.get_all_albums()

    for album in albums:
        album_dir = BASE_DIRECTORY + "{}/".format(album.name)
        #  TODO: make asynchronous ?

        if not album_cache.album_exists(album.album_id):
            os_utility.make_dir_if_not_exist(album_dir)
            cover_path = media_downloader.download_image(album.name, album.cover_url, album_dir)

        songs = msr_service.get_msr_album_songs(album)
        for song in songs:

            print("INFO: Verifying song: \"{}\"".format(song.name))
            # We can skip songs that already have been downloaded
            if album_cache.song_exists(album.album_id, song.song_id):
                print("INFO: Skipping")
                continue

            audio_path = media_downloader.download_audio(song.name, song.source_url, album_dir)

            lyric_path = None
            if song.lyric_url is not None:
                lyric_path = media_downloader.download_lyric(song.name, song.lyric_url, album_dir)

            metadata = Metadata(song.name, album.name, song.artists, cover_path, lyric_path)
            audio_metadata_utility.fill_audio_metadata(audio_path, metadata)

            # Cache song
            album_cache.cache(album.album_id, song.song_id)
