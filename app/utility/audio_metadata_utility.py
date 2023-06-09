import os

import pylrc
from PIL import Image
from mutagen.easyid3 import EasyID3
from mutagen.flac import FLAC, Picture
from mutagen.id3 import ID3, APIC, SYLT, Encoding, TextFrame
from pydub import AudioSegment

from domain.model.metadata import Metadata

AudioSegment.ffmpeg = os.environ.get("FFMPEG")


def fill_audio_metadata(audio_path, metadata: Metadata):
    base, audio_type = os.path.splitext(audio_path)
    if audio_type == ".mp3":
        fill_mp3_metadata(audio_path, metadata)
    elif audio_type == ".flac":
        file = FLAC(audio_path)
        fill_flac_metadata(file, metadata)
    return


def fill_mp3_metadata(audio_path: str, metadata: Metadata):

    file = EasyID3(audio_path)
    file['title'] = metadata.title
    file['album'] = metadata.album_name
    file['artist'] = ''.join(metadata.artists)

    file.save()

    cover_path = metadata.cover_path
    lyric_path = metadata.lyric_path
    # Use ID3 for media metadata
    file = ID3(audio_path)

    with open(cover_path, "rb") as cover:
        file.add(APIC(
            encoding=3,
            mime=get_mime(cover_path),
            type=3, desc=u'Cover',
            data=cover.read()))

    # Read and add lyrics
    if lyric_path is not None:
        sylt = lyric_file_to_text(lyric_path)
        file.setall("SYLT", [SYLT(encoding=Encoding.UTF8,
                                  lang="eng",
                                  format=2,
                                  type=1,
                                  text=sylt)])
        os.remove(lyric_path)

    file.save(v2_version=3)


def fill_flac_metadata(file: FLAC, metadata: Metadata):
    file['title'] = metadata.title
    file['album'] = metadata.album_name
    file['artist'] = ''.join(metadata.artists)

    cover_path = metadata.cover_path
    lyric_path = metadata.lyric_path

    image = Picture()
    image.type = 3
    image.desc = "Cover"
    image.mime = get_mime(cover_path)

    with open(cover_path, "rb") as f:
        image.data = f.read()
    with Image.open(cover_path) as imagePil:
        image.width, image.height = imagePil.size
        image.depth = 24
    file.add_picture(image)
    # Read and add lyrics
    if lyric_path is not None:
        lyric = open(lyric_path, "r", encoding="utf-8").read()
        file['lyrics'] = lyric
    file.save()
    os.remove(lyric_path)


# Both WAV and FLAC are lossless audio format, the conversion has absolutely no quality impact
# (FLAC has the advantage to be able to hold metadata)
def wav_2_flac(audio_path: str):
    base, audio_type = os.path.splitext(audio_path)
    if audio_type == ".wav":
        flac_audio_path = base + ".flac"
        AudioSegment.from_wav(audio_path).export(flac_audio_path, format='flac')
        os.remove(audio_path)
        # reference new audio_path
        audio_path = flac_audio_path
    return audio_path


def wav_2_mp3(audio_path: str):
    base, audio_type = os.path.splitext(audio_path)
    if audio_type == ".wav":
        mp3_audio_path = base + ".mp3"
        AudioSegment.from_wav(audio_path).export(mp3_audio_path, format='mp3')
        os.remove(audio_path)
        # reference new audio_path
        audio_path = mp3_audio_path
    return audio_path


def lyric_file_to_text(filename):
    lrc_file = open(filename, 'r', encoding='utf-8')
    lrc_string = ''.join(lrc_file.readlines())
    lrc_file.close()
    subs = pylrc.parse(lrc_string)
    ret = []
    for sub in subs:
        time = int(sub.time * 1000)
        text = sub.text
        ret.append((text, time))
    return ret


def get_mime(image_path: str) -> str:
    ext = os.path.splitext(image_path)[1]
    if ext == ".jpg":
        return "image/jpeg"
    elif ext == ".png":
        return "image/png"
    else:
        print("ERROR: Currently unhandled image type {}".format(ext))
