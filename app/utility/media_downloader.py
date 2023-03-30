from requests import Session
from tqdm import tqdm

from utility.audio_metadata_utility import wav_2_flac


class MediaDownloader:
    session: Session

    def __init__(self, session: Session):
        self.session = session

    def download_audio(self, name: str, media_url: str, dest_dir: str):
        audio_stream = self.session.get(url=media_url, stream=True)
        output_path = dest_dir + name
        audio_type = audio_stream.headers["content-type"]

        if audio_type == "audio/mpeg":
            output_path += ".mp3"
        elif audio_type == "audio/wav":
            output_path += ".wav"
        else:
            print("ERROR: Currently unhandled audio type {} for {}".format(audio_type, name))

        # Download song
        total = int(audio_stream.headers.get('content-length', 0))
        with open(output_path, "wb") as f, tqdm(
                desc=name,
                total=total,
                unit="iB",
                unit_scale=True,
                unit_divisor=1024
        ) as bar:
            for data in audio_stream.iter_content(chunk_size=1024):
                size = f.write(data)
                bar.update(size)

        if audio_type == "audio/wav":
            return wav_2_flac(output_path)

        return output_path

    def download_image(self, name: str, media_url: str, dest_dir: str):
        image = self.session.get(media_url)
        output_path = dest_dir + name
        image_type = image.headers["content-type"]

        if image_type == "image/jpeg":
            output_path += ".jpg"
        elif image_type == "image/png":
            output_path += ".png"
        else:
            print("ERROR: Currently unhandled image type {} for {}".format(image_type, name))

        with open(output_path, "wb") as f:
            f.write(image.content)

        return output_path

    def download_lyric(self, name: str, media_url: str, dest_dir: str):
        lyric = self.session.get(media_url)
        output_path = dest_dir + name
        content_type = lyric.headers["content-type"]

        if content_type == "application/octet-stream":
            output_path += ".lrc"
        else:
            print("ERROR: Currently unhandled lyric type {} for {}".format(content_type, name))

        with open(output_path, "wb") as f:
            f.write(lyric.content)

        return output_path
