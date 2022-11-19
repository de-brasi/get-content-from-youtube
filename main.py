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
VALID_TYPES = ("all content", "audio")     # TODO: handle only video


def get_audio_by_url(users_url_: str, destination_directory_: str) -> int:
    try:
        video = pytube.YouTube(users_url_)
        video_streams = video.streams.filter(file_extension="mp4").filter(type="audio")
        streams_sorted_by_abr = video_streams.order_by('abr')[::-1]
        if streams_sorted_by_abr:
            streams_sorted_by_abr[0].download(destination_directory_)
            return SUCCESS
    except ...:
        pass

    return FAILURE


def get_video_by_url(users_url_: str, destination_directory_: str) -> int:
    try:
        video = pytube.YouTube(users_url_)
        video_streams = video.streams.filter(file_extension="mp4")
        streams_sorted_by_resolution = video_streams.order_by('resolution')[::-1]
        highest_res = video.streams.get_highest_resolution()
        if streams_sorted_by_resolution:
            streams_sorted_by_resolution[0].download(destination_directory_)
            return SUCCESS
    except ...:
        pass

    return FAILURE


def generalized_get_content(users_url_: str, content_type_: str, destination_directory_: str) -> int:
    assert content_type_ in VALID_TYPES
    content_criteria = {
        "all content": {"file_extension filter": ("mp4", ), "order by fields": ("resolution", )},
        "audio": {"file_extension filter": ("mp4", "audio"), "order by fields": ("abr",)}
    }
    try:
        content = pytube.YouTube(users_url_)
        content_streams = content

        for criteria_ in content_criteria.get(content_type_).get("file_extension filter"):
            content_streams = content.streams.filter(file_extension=criteria_)

        for criteria_ in content_criteria.get(content_type_).get("order by fields"):
            content_streams = content_streams.order_by(criteria_)

        content_streams = content_streams[::-1]

        if content_streams:
            content_streams[0].download(destination_directory_)
            return SUCCESS
    except ...:
        pass

    return FAILURE


if __name__ == '__main__':
    print("Get URL of YouTube video: ")
    url_ = input()
    while not validators.url(url_):
        print("Invalid URL. Get me new: ")
        url_ = input()
    # get_audio_by_url(url_, STORAGE_DIR_PATH)
    get_video_by_url(url_, STORAGE_DIR_PATH)
    # generalized_get_content(url_, "all content", STORAGE_DIR_PATH)
# TODO: catch answer (failure or not) from get_video_by_url
