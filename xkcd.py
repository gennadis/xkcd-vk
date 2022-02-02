import os
from typing import Optional, Union
from urllib.parse import urljoin, unquote, urlsplit


import requests


COMICS_JSON_URL = "https://xkcd.com/{}/info.0.json"


def get_comics_json(comics_id: int) -> Optional[dict]:
    response = requests.get(COMICS_JSON_URL.format(comics_id))
    response.raise_for_status()

    return response.json()


def get_filename(url: str) -> str:
    url_unqoted = unquote(url)
    _, _, path, _, _ = urlsplit(url_unqoted)
    _, filename = os.path.split(path)

    return filename


def fetch_comics_image(comics_id: int) -> Optional[str]:
    comics_json = get_comics_json(comics_id)
    image_url = comics_json["img"]
    filename = get_filename(image_url)

    response = requests.get(image_url)
    response.raise_for_status()

    with open(filename, "wb") as file:
        file.write(response.content)

    return filename


def main():
    fetch_comics_image(353)


if __name__ == "__main__":
    main()
