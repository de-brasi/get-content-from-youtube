"""
1) Get audio from YouTube video.
2) Slice one audio by part with time points.
"""

import pytube
import pathlib
import validators

SUCCESS = 1
FAILURE = 0
CUR_PATH = str(pathlib.Path().resolve())
STORAGE_DIR_NAME = "content_storage"
STORAGE_DIR_PATH = CUR_PATH + '/' + STORAGE_DIR_NAME


def get_audio_by_url(users_url: str) -> int:
    video = pytube.YouTube(users_url)
    video_streams = video.streams.filter(file_extension="mp4").filter(type="audio")
    streams_sorted_by_abr = video_streams.order_by('abr')[::-1]
    if streams_sorted_by_abr:
        try:
            streams_sorted_by_abr[0].download(STORAGE_DIR_PATH)
            return SUCCESS
        except ...:
            pass
    return FAILURE


if __name__ == '__main__':
    print("Get URL of video: ")
    url_ = input()
    while not validators.url(url_):
        print("Invalid URL. Get me new: ")
        url_ = input()
    get_audio_by_url(url_)
